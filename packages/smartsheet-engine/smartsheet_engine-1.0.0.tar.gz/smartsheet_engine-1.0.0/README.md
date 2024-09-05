# Smartsheet Engine
A Python library that simplifies Smartsheet API workflows

## Table of Contents
- [Smartsheet Engine](#smartsheet-engine)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
    - [Coming Soon](#coming-soon)
  - [Roadmap](#roadmap)
  - [Installation](#installation)
    - [From PyPI](#from-pypi)
    - [From GitHub](#from-github)
    - [From the Alteryx Python Tool](#from-the-alteryx-python-tool)
  - [Usage](#usage)
  - [How-to Guides](#how-to-guides)
    - [Create, Read, Update, and Delete Smartsheet Data](#create-read-update-and-delete-smartsheet-data)
      - [Get a Smartsheet as a Dataframe](#get-a-smartsheet-as-a-dataframe)
      - [Append a Dataframe to a Smartsheet](#append-a-dataframe-to-a-smartsheet)
      - [Update a Smartsheet From a Dataframe](#update-a-smartsheet-from-a-dataframe)
      - [Delete Smartsheet Rows](#delete-smartsheet-rows)
      - [Provision Smartsheets in Bulk](#provision-smartsheets-in-bulk)
    - [Analyze Smartsheet Data](#analyze-smartsheet-data)
      - [Compare Two Dataframes and Identify Row Changes](#compare-two-dataframes-and-identify-row-changes)
      - [Compare Two Dataframes and Identify Column Changes](#compare-two-dataframes-and-identify-column-changes)
      - [Compare Two Dataframes and Identify Cell Value Changes](#compare-two-dataframes-and-identify-cell-value-changes)
    - [Modify Smartsheet Object Properties](#modify-smartsheet-object-properties)
      - [Update Column Formula](#update-column-formula)
      - [Update Column Dropdown Options](#update-column-dropdown-options)
      - [Lock or Unlock a Column](#lock-or-unlock-a-column)
      - [Hide or Unhide a Column](#hide-or-unhide-a-column)
      - [Share a Smartsheet](#share-a-smartsheet)
      - [Update a Shared User's Sheet Permissions](#update-a-shared-users-sheet-permissions)
  - [Documentation](#documentation)
    - [System Design](#system-design)
      - [Architecture](#architecture)
  - [Acknowledgements](#acknowledgements)
    - [Contributors](#contributors)
  - [License](#license)
  - [Contributing](#contributing)

## Features
- **Create, Read, Update, and Delete Smartsheet Data**
  - Get a Smartsheet as a Dataframe
  - Append a Dataframe to a Smartsheet
  - Update a Smartsheet From a Dataframe
  - Delete Smartsheet Rows
- **Modify Smartsheet Object Properties**
  - Update Column Dropdown Options
  - Lock or Unlock a Column
  - Hide or Unhide a Column
### Coming Soon
- **Create, Read, Update, and Delete Smartsheet Data**
  - Provision Smartsheets in Bulk
- **Analyze Smartsheet Data**
  - Compare Two Dataframes and Identify Row Changes
  - Compare Two Dataframes and Identify Column Changes
  - Compare Two Dataframes and Identify Cell Value Changes
- **Modify Smartsheet Object Properties**
  - Update Column Formula
  - Share a Smartsheet
  - Update a Shared User's Sheet Permissions

## Roadmap
See the [roadmap](ROADMAP.md) for the master list of work items to be done and features coming soon

## Installation
1. Download and install [Python](https://www.python.org/downloads/) if needed
2. Install `smartsheet-engine`
### From PyPI
```
pip install smartsheet-engine
```
### From GitHub
```
git clone https://github.com/1npo/smartsheet-engine.git
cd smartsheet-engine
pip install .
```
### From the [Alteryx Python Tool](https://knowledge.alteryx.com/index/s/article/How-To-Use-Alteryx-installPackages-in-Python-tool-1583461465434)
```
Alteryx.installPackage(package="smartsheet-engine")
```

## Usage
>[!WARNING]
> **This library is under active development and currently in beta. Please use it with care.**

To use `smartsheet-engine` in your Notebook or script:

1. Get your Smartsheet API key and save it to a variable, such as `smartsheet_api_key`
2. Import the `SmartsheetEngine` class
3. Initialize a `SmartsheetEngine` object with your API key
4. Use the engine as needed in your workflow (see [How-To Guides](#how-to-guides) for examples)

```python
from smartsheet_engine import SmartsheetEngine

S = SmartsheetEngine(api_key=smartsheet_api_key)
```

> [!CAUTION]
> Don't hardcode your API key into your script or Notebook widget. Put it in a secret store or an environment variable instead.

> [!TIP]
> You don't need to provide an `api_key` when you initialize a `SmartsheetEngine` object if your API key is already saved in the `SMARTSHEET_ACCESS_TOKEN` environment variable.

## How-to Guides
### Create, Read, Update, and Delete Smartsheet Data
#### Get a Smartsheet as a Dataframe
Get the contents of the Smartsheet named `finished_test_grid` and print the dataframe:

```python
df = S.get_sheet('finished_test_grid').sheet_df
print(df)
```
```text
         _ss_row_id  number   rating
0   123734752464772     1.0   Lowest
1  7876435046272900     2.0      Low
2  2246935512059780     3.0   Medium
3  2463203892629380     4.0     High
4  6966803519999876     5.0  Highest
```

> [!NOTE]
> `SmartsheetEngine` converts a Sheet object to a dataframe when you call `S.get_sheet()`, then it adds the Smartsheet Row ID to a special `_ss_row_id` column in that dataframe. This is how it maps dataframe rows to Smartsheet rows.

#### Append a Dataframe to a Smartsheet
Append 2 rows from a dataframe to the Smartsheet named `test_grid`:

```python
df = pd.DataFrame({
    'number':       [4, 5],
    'rating':       [None, None],
    'missing_col':  ['data', 'ignored'],
})
S.append_sheet_rows('test_grid', df)
```

<table>
  <tr>
    <th>Before Appending</th>
    <th>After Appending</th>
  <tr>
    <td><img src='https://github.com/1npo/smartsheet-engine/blob/main/img/append_rows_before.png', alt='Before appending rows'></td>
    <td><img src='https://github.com/1npo/smartsheet-engine/blob/main/img/append_rows_after.png', alt='After appending rows'></td>
  </tr>
</table>

> [!NOTE]
> Column values from a dataframe will only be updated or appended to a Smartsheet if those columns exist in the Smartsheet. If any dataframe column name doesn't exist in the Smartsheet, that column will be ignored.
> 
> You can choose to only update/append certain columns, or NOT to update/append certain columns, by using the `include_cols` and `exclude_cols` arguments.
> 
> For example, in this how-to guide, this:
>
> ```python
> S.append_sheet_rows('test_grid', df, include_cols=['number'])
> ```
>
> And this:
>
> ```python
> S.append_sheet_rows('test_grid', df, exclude_cols=['rating'])
> ```
>
> Are equivalent to:
>
> ```python
> S.append_sheet_rows('test_grid', df)
> ```

#### Update a Smartsheet From a Dataframe
Get a dataframe of the Smartsheet named `test_grid`, change the dropdown options for the `rating` column, and then update the column:

```python
import numpy as np

df = S.get_sheet('test_grid').sheet_df

S.update_column_picklist('test_grid', 'rating', ['Lowest', 'Low', 'Medium', 'High', 'Highest'])

conditions = [
    df['number'] == 1,
    df['number'] == 2,
    df['number'] == 3,
    df['number'] == 4,
    df['number'] == 5,
]
choices = [
    'Lowest',
    'Low',
    'Medium',
    'High',
    'Highest',
]
df['rating'] = np.select(conditions, choices)

S.update_sheet_rows('test_grid', df)
```

<table>
  <tr>
    <th>Before Updating</th>
    <th>After Updating</th>
  <tr>
    <td><img src='https://github.com/1npo/smartsheet-engine/blob/main/img/update_rows_before.png', alt='Before updating rows'></td>
    <td><img src='https://github.com/1npo/smartsheet-engine/blob/main/img/update_rows_after.png', alt='After updating rows'></td>
  </tr>
</table>

#### Delete Smartsheet Rows
> [!CAUTION]
> Before you run `S.delete_sheet_rows(sheet_name, df)`, make sure that `df` only includes the rows you want to delete from the Smartsheet. Because when you run that function, every Smartsheet row that has an ID listed in `df._ss_row_id` **will be deleted from the Smartsheet**.

Get a dataframe of the Smartshet named `test_grid`, select only the rows that have the number 2 or 3 in the number column, and then delete them:

```python
df = S.get_sheet('test_grid').sheet_df

df = df[df['number'].isin([2,3])]

S.delete_sheet_rows('test_grid', df)
```

<table>
  <tr>
    <th>Before Deleting</th>
    <th>After Deleting</th>
  <tr>
    <td><img src='https://github.com/1npo/smartsheet-engine/blob/main/img/delete_rows_before.png', alt='Before deleting rows'></td>
    <td><img src='https://github.com/1npo/smartsheet-engine/blob/main/img/delete_rows_after.png', alt='After deleting rows'></td>
  </tr>
</table>

#### Provision Smartsheets in Bulk
> [!NOTE]
>
> Coming soon!

### Analyze Smartsheet Data
#### Compare Two Dataframes and Identify Row Changes
> [!NOTE]
>
> Coming soon!

#### Compare Two Dataframes and Identify Column Changes
> [!NOTE]
>
> Coming soon!

#### Compare Two Dataframes and Identify Cell Value Changes
> [!NOTE]
>
> Coming soon!

### Modify Smartsheet Object Properties
#### Update Column Formula
> [!NOTE]
>
> Coming soon!

#### Update Column Dropdown Options
Change the dropdown options for the `rating` column to `Low, Medium, and High` on the Smartsheet named `test_grid`:

```python
S.update_column_picklist('test_grid', 'rating', ['Low', 'Medium', 'High'])
```

#### Lock or Unlock a Column
Locks and then unlock the `rating` column on the Smartsheet named `test_grid`:

```python
S.lock_column('test_grid', 'rating')
S.unlock_column('test_grid', 'rating')
```

#### Hide or Unhide a Column
Hide and then unhide the `rating` column on the Smartsheet named `test_grid`:

```python
S.hide_column('test_grid', 'rating')
S.unhide_column('test_grid', 'rating')
```

#### Share a Smartsheet
> [!NOTE]
>
> Coming soon!

#### Update a Shared User's Sheet Permissions
> [!NOTE]
>
> Coming soon!

## Documentation
> [!NOTE]
> This documentation will be expanded and eventually migrated into Sphinx docs that will be hosted on [GitHub Pages](https://pages.github.com/).

### System Design
#### Architecture
<div align='center'>
<img src='https://github.com/1npo/smartsheet-engine/blob/main/img/smartsheet_engine_architecture.png' alt='smartsheet-engine system architecture diagram'>
</div>

## Acknowledgements
- The architecture diagram was made with [Lucidchart](http://lucidchart.com/)
- 
### Contributors
Thanks and kudos to any contributors will go here

## License
`smartsheet-engine` is made available under the [MIT License](LICENSE)

## Contributing
See [CONTRIBUTING](CONTRIBUTING.md) for instructions on how to contribute to `smartsheet-engine`