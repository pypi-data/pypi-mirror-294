import logging
from datetime import datetime
import pandas as pd
from .client import SmartsheetAPIClient
from .grids import SmartsheetGrid, GridRepository, METADATA_FIELDS
logging.basicConfig(format='%(asctime)s : %(levelname)-8s : %(name)s : %(message)s',
					datefmt='%Y-%m-%d %I:%M%p',
					level=logging.INFO)
logger = logging.getLogger(__name__)


class SmartsheetEngine:
	"""A high-level abstraction that simplifies Smartsheet API workflows

	Public Methods
	--------------
	- get_home_contents()
	- get_sheet(sheet_name)
	- append_sheet_rows(sheet_name, df)
	- update_sheet_rows(sheet_name, df)
	- delete_sheet_rows(sheet_name, df)
	- update_column_picklist(sheet_name, column_name, dropdown_options)
	- lock_column(sheet_name, column_name)
	- hide_column(sheet_name, column_name)
	- unlock_column(sheet_name, column_name)
	- unhide_column(sheet_name, column_name)
	"""

	def __init__(self, api_key: str = None):
		self.api = SmartsheetAPIClient(api_key=api_key)
		self.repo = GridRepository()
		self.get_home_contents()

	def get_home_contents(self):
		"""Get a listing of the user's Smartsheet Home contents via the API, and build SmartsheetGrid objects to represent each one
		"""

		self.home_contents = self.api.smart.Home.list_all_contents(include='source').to_dict()

		# Get Sheets in user's Sheets folder
		for sheet in self.home_contents['sheets']:
			self.repo.add_grid(SmartsheetGrid(sheet_id=sheet['id'],
											  sheet_name=sheet['name'],
											  access_level=sheet['accessLevel'],
											  created_at=datetime.strptime(sheet['createdAt'], '%Y-%m-%dT%H:%M:%S%zZ'),
											  modified_at=datetime.strptime(sheet['modifiedAt'], '%Y-%m-%dT%H:%M:%S%zZ')))

		# Get Sheets in Folders
		self._find_sheets_in_folders(self.home_contents['folders'])

		# Get Sheets in Workspaces
		for workspace in self.home_contents['workspaces']:
			#logger.debug(f'Found workspace: {workspace["name"]}: keys={workspace.keys()}')
			if 'sheets' in workspace:
				for sheet in workspace['sheets']:
					self.repo.add_grid(SmartsheetGrid(sheet_id=sheet['id'],
													  sheet_name=sheet['name'],
													  access_level=sheet['accessLevel'],
													  created_at=datetime.strptime(sheet['createdAt'], '%Y-%m-%dT%H:%M:%S%zZ'),
													  modified_at=datetime.strptime(sheet['modifiedAt'], '%Y-%m-%dT%H:%M:%S%zZ'),
													  workspace_id=workspace['id'],
													  workspace_name=workspace['name'],
													  is_in_workspace=True))

			if 'folders' in workspace:
				self._find_sheets_in_folders(workspace,
											 workspace_id=workspace['id'],
											 workspace_name=workspace['name'])

		logger.info(f'Built an index of {len(self.repo.grids)} available Sheets')

	def _find_sheets_in_folders(
		self,
		folders: dict,
		workspace_id: int = None,
		workspace_name: str = None
	) -> dict:
		"""Get all sheets in the user's Smartsheet Folder(s), recursively

		:param folders: The dictionary to traverse recursively, looking for folders
		:param workspace_id: The workspace ID to include in the SmartsheetGrid object, if the folders are in a workspace 
		:param workspace_name: The workspace Name to include in the SmartsheetGrid object, if the folders are in a workspace
		:returns: A Smartsheet API response dictionary that may contain a list of folders
		"""

		if isinstance(folders, dict):
			for k, v in folders.items():
				if k == 'folders':
					for folder in v:
						if 'sheets' in folder:
							for sheet in folder['sheets']:
								self.repo.add_grid(SmartsheetGrid(sheet_id=sheet['id'],
																  sheet_name=sheet['name'],
																  access_level=sheet['accessLevel'],
																  created_at=datetime.strptime(sheet['createdAt'], '%Y-%m-%dT%H:%M:%S%zZ'),
																  modified_at=datetime.strptime(sheet['modifiedAt'], '%Y-%m-%dT%H:%M:%S%zZ'),
																  folder_id=folder['id'],
																  folder_name=folder['name'],
																  workspace_id=workspace_id,
																  workspace_name=workspace_name,
																  is_in_folder=True,
																  is_in_workspace=any([workspace_id, workspace_name])))
					self._find_sheets_in_folders(v)

	def get_sheet(self, sheet_name: str) -> bool:
		"""Get the full data from the API for the given Sheet ID, and save it to the SmartsheetGrid object
		
		:param grid: Get the current Sheet contents for this SmartsheetGrid object
		:returns: True if the `id` in the given grid exists, False if the `id` does not exist
		"""

		grid = self.repo.get_grid_by_name(sheet_name)
		grid.sheet_obj = self.api.smartsheet_get_sheet(grid.sheet_id)
		grid.column_map = {col.title: col.id for col in grid.sheet_obj.columns}
		grid.sheet_df = self._build_dataframe(sheet_name)
		self.repo.update_grid(grid)
		logger.info(f'{sheet_name} ({grid.sheet_id}): Got Sheet with {len(grid.sheet_df.index)} rows')
		return grid

	def _build_dataframe(self, sheet_name: str) -> pd.DataFrame:
		"""Convert a Sheet object to a DataFrame, and return a copy of the DF"""
		
		grid = self.repo.get_grid_by_name(sheet_name)
		column_map = grid.column_map
		sheet_obj = grid.sheet_obj
		sheet_records = []
		for row in sheet_obj.rows:
			# These fields prefixed with _ss are metadata needed for processing when
			# updating, adding, or removing rows
			row_record = {field:None for field in METADATA_FIELDS}
			row_record['_ss_row_id'] = row.id
			for col in column_map.keys():
				row_record.update({col: row.get_column(column_map[col]).value})
			sheet_records.append(row_record)
		return pd.DataFrame.from_dict(sheet_records)

	def append_sheet_rows(
		self,
		sheet_name: str,
		df: pd.DataFrame,
		include_cols: list = None,
		exclude_cols: list = None
	):
		"""Append dataframe rows to a Smartsheet, retrying the request if needed, and capture the response for debugging
		
		:param grid: Append Rows to this Sheet
		:param df: Append the series in this dataframe to the Sheet
		:param include_cols: Only append the values in these columns (default: whatever fields exist in both df and grid.sheet_df)
		:param exclude_cols: Don't append the values from any of these columns
		"""

		grid = self.repo.get_grid_by_name(sheet_name)
		rows = self.api.gen_rows_to_append(grid, df, include_cols, exclude_cols)
		self.api.smartsheet_add_rows(grid.sheet_id, rows)
		logger.info(f'{grid.sheet_name} ({grid.sheet_id}): Added {len(rows)} rows')

	def update_sheet_rows(
		self,
		sheet_name: str,
		df: pd.DataFrame,
		include_cols: list = None,
		exclude_cols: list = None
	):
		"""Update Rows in a Smartsheet

		:param sheet_name: Update Rows on this Sheet
		:param df: Update the Sheet with this dataframe
		:param include_cols: Only update the values in these columns (default: whatever fields exist in both df and grid.sheet_df)
		:param exclude_cols: Don't update the values from any of these columns
		"""

		grid = self.repo.get_grid_by_name(sheet_name)
		rows = self.api.gen_rows_to_update(grid, df, include_cols, exclude_cols)
		self.api.smartsheet_update_rows(grid.sheet_id, rows)
		logger.info(f'{grid.sheet_name} ({grid.sheet_id}): Updated {len(rows)} rows')

	def delete_sheet_rows(
		self,
		sheet_name: str,
		df: pd.DataFrame
	):
		"""Delete Rows in a Smartsheet

		:param grid: Delete Rows from this Sheet
		:param df: Get the list of Row IDs to delete from this dataframe
		:returns: A list of Row IDs
		"""

		grid = self.repo.get_grid_by_name(sheet_name)
		rows = self.api.gen_rows_to_delete(grid, df)
		self.api.smartsheet_delete_rows(grid.sheet_id, rows)
		logger.info(f'{grid.sheet_name} ({grid.sheet_id}): Deleted {len(rows)} rows')

	def update_column_picklist(
		self,
		sheet_name: str,
		column_name: str,
		dropdown_options: list
	):
		"""Update picklist values for columns in the given SmartsheetGrid
		
		:param grid: The SmartsheetGrid for the Smartsheet you want to update
		:param column_name: The name of the column to update the picklist on
		:param dropdown_options: The new values for the column picklist
		"""
		grid = self.repo.get_grid_by_name(sheet_name)
		setting = {'type': 'PICKLIST', 'options': dropdown_options}
		self._toggle_column_setting(grid, column_name, setting)
		logger.info(f'{grid.sheet_name} ({grid.sheet_id}): {column_name}: Changed the dropdown values to {dropdown_options}')

	def lock_column(self, sheet_name: str, column_name: str):
		"""Lock a column in a Smartsheet
		
		:param grid: The SmartsheetGrid for the Smartsheet you want to update
		:param column_name: The name of the column to lock
		"""
		grid = self.repo.get_grid_by_name(sheet_name)
		self._toggle_column_setting(grid, column_name, {'locked': True})
		logger.info(f'{grid.sheet_name} ({grid.sheet_id}): {column_name}: Locked column')

	def hide_column(self, sheet_name: str, column_name: str):
		"""Hide a column in a Smartsheet
		
		:param grid: The SmartsheetGrid for the Smartsheet you want to update
		:param column_name: The name of the column to hide
		"""
		grid = self.repo.get_grid_by_name(sheet_name)
		self._toggle_column_setting(grid, column_name, {'hidden': True})
		logger.info(f'{grid.sheet_name} ({grid.sheet_id}): {column_name}: Hid column')

	def unlock_column(self, sheet_name: str, column_name: str):
		"""Unlock a column in a Smartsheet
		
		:param grid: The SmartsheetGrid for the Smartsheet you want to update
		:param column_name: The name of the column to lock
		"""
		grid = self.repo.get_grid_by_name(sheet_name)
		self._toggle_column_setting(grid, column_name, {'locked': False})
		logger.info(f'{grid.sheet_name} ({grid.sheet_id}): {column_name}: Unlocked column')

	def unhide_column(self, sheet_name: str, column_name: str):
		"""Unhide a column in a Smartsheet
		
		:param grid: The SmartsheetGrid for the Smartsheet you want to update
		:param column_name: The name of the column to unhide
		"""
		grid = self.repo.get_grid_by_name(sheet_name)
		self._toggle_column_setting(grid, column_name, {'hidden': False})
		logger.info(f'{grid.sheet_name} ({grid.sheet_id}): {column_name}: Unhid column')
	
	def _toggle_column_setting(
		self,
		grid: SmartsheetGrid,
		column_name: str,
		setting: dict
	):
		if column_name not in grid.column_map:
			raise ValueError(f'Column "{column_name}" does not exist in the "{grid.sheet_name}" Smartsheet')
		
		self.api.smartsheet_update_column(grid.sheet_id,
										  grid.column_map[column_name],
										  self.api.smart.models.Column(setting))
