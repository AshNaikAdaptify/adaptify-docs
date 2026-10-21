---
title: Rating tables
audience: internal  # final audience: external (flips in a release PR)
goals:
  - Add a rating table and set up its columns
  - Fill a table from a CSV file
video: ""
---

# Rating tables

Rating tables hold your rates and factors, such as base rates, territory factors or age of home factors. Each column is linked to a field in the rating structure, so Adaptify knows what to look up and where to put the result.

Open the rater and choose the **Tables** tab. The **Rating tables** panel lists the tables. Use **Search tables** to find one, then select it to view it. Input and output columns are marked with different icons.

## The Manage menu

Select **Manage** next to **Rating tables** to:

- **Add new table**, **Import table**, **Import tables**, **Import tables from manuals** or **Export all tables**.
- Under **Actions for selected table**: **Export table**, **Copy table**, **Edit table details** or **Delete table**. Select a table first.

![The Manage menu on the Tables tab](../assets/rating/manage-menu.webp)

## Add a table

1. Select **Manage** → **Add new table**.
2. Enter the **Name** and, if you like, a **Description**.
3. Choose the **Type**: **None or unspecified**, **Premiums**, **Loss costs**, **Factors** or **Relativities**.
4. Enter the **Rule number**, if there is one.
5. Select **Add table**. The new, empty table opens.

![The Add new table dialog with Name, Description, Type and Rule number](../assets/rating/add-new-table-live.webp)

## Set up the columns

1. In the empty table, select **+ Add column**.
2. In **Edit Column**, enter the column's **Name**.
3. Choose the **Column Type**: **Input** for a value you look up by, such as Zip code, or **Output** for the value you get back, such as Territory.
4. For an input column, choose the **Column Conditions**: **Equals**, **Greater Than**, **Greater Than or Equal To**, **Less Than**, **Less Than or Equal To** or **Interpolate**.
5. Under **Select Path**, search for and pick the structure field this column maps to. It fills in the **Risk Item Field**, for example Policy.Location.Zip code, and shows its **Data Type**.
6. Select **Save**. Add the next column the same way, then select **Save Changes**.

![The Edit Column panel with Name, Column Type, Column Conditions, Data Type, Risk Item Field and the Select Path tree](../assets/rating/edit-column.webp)

## Fill in the table

You can type values straight into the cells while you edit the table. For a large table, it's quicker to use a file:

1. Select **Manage** → **Export table**. You get a CSV file with the column headers.
2. Fill in the rows in Excel and save it as CSV.
3. Select **Manage** → **Import table**, then choose your CSV file.

## Add the table to a calculation

A table is only used once a calculation uses it. Add each new table to your [Calculations](calculations.md), or it won't be part of the rate order or your tests.
