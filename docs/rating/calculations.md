---
title: Calculations
audience: internal  # final audience: external (flips in a release PR)
goals:
  - Find a calculation flow for a risk item
  - Build calculation steps and branches
video: ""
---

# Calculations

Calculations turn your table values and rating inputs into premium. Each calculation is a flow you draw on a canvas, step by step.

## Find a calculation

1. Open the rater and choose the **Calculations** tab. The **Risk Item Calculation** view opens; there's also a **Coverages** view.
2. Choose the **Risk Item**, such as **Policy** or **Location**.
3. Choose the **Risk Item Calculation**. Its flow appears on the canvas.

From here you can **Delete**, **Copy** or **Edit** the calculation, or start another one with **+ Create New**.

![A calculation flow on the Calculations tab: START, a Calculation node, a table node and END](../assets/rating/calculation-canvas.webp)

## What's on the canvas

Every flow runs from **START** to **END**. In between, you link these nodes with arrows:

- **Table:** looks up a rating table.
- **Calculation:** a set of math steps.
- **Branch:** a condition that sends the flow one way or another, such as checking for a wind exclusion. Each path can have a label.

Select **Edit** to change the flow. Add nodes from the palette on the left, link them, then select **Save Changes**, or **Cancel** to discard your changes.

## Configure a calculation

Open a **Calculation** node to configure it.

1. Enter a **Name**.
2. Under **Add Functions**, choose a function. It's added to **Steps**. Functions include **+**, **-**, **\***, **/**, **ROUND**, **ROUND_UP**, **DAYS_BETWEEN**, **MONTHS_BETWEEN**, **YEARS_BETWEEN**, **YEAR**, **IF**, **FOR_EACH** and **TABLE_LOOKUP**.
3. Fill in each part of the step. For each one, choose a **Binding Type**:
    - **Step:** the result of an earlier step.
    - **Path:** a field from the rating structure, picked from **Select Path**.
    - **Value:** a number you type in.
4. Select **Save**.

For example, step 1 could be Fire Peril Base Rate × Fire Territory Factor, and a later step could round the result.

If a part is still empty, you'll see "Values are missing for one or more functions". Fill it in before you save.

![Configure Calculation with three steps and the Binding Type options Step, Path and Value](../assets/rating/configure-calculation.webp)

## Configure a branch

Open a **Branch** node to set its condition in **Configure Condition**: give it a **Name**, build the **IF** condition, then add what happens under **THEN** and **ELSE**.

## Check your work

Use **Validate**, above the rater's tabs, to check the setup.

## Next

[Rate order](rate-order.md)
