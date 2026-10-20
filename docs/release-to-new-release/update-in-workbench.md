---
title: Update your product in Workbench
audience: internal  # final audience: external (flips in a release PR)
goals:
  - Start one project that updates forms and rates for several states
  - Enter the new editions and move the work to End
video: ""
---

# Update your product in Workbench

Do this when a published product needs new editions of its forms or rates. One Workbench project can cover forms and rates for every state you're changing.

## Steps

1. In **Workbench**, choose **+ New project**, then **Product update**. For each step in detail, see [Start a product update](../workbench/create-project/product-update.md).
2. **Setup:** under **Project type**, choose **Forms**, **Rates** or both, then choose **Next**. If you choose both, you get one combined project with a child project for each type.
3. **Configuration:** choose the **Product** and the **Jurisdictions**, for example Personal Auto in Alabama and Alaska. Choose **Next**.
4. **Finalize:** enter the **Project title** and **Project description**, check the workflow for each type, and pick a **Due date** from the calendar. Choose **Create**.
5. Open the forms child project and choose **Add form**. In **Add form changes**, choose **Update form**, select the forms, enter the **Updated edition** (for example 01 27) and choose **Change**. In the rates child project, do the same under **Add rate changes** with **Update rate**. See [Update forms](../workbench/update-forms.md) and [Update rates](../workbench/update-rates.md).
6. Move each child project forward with **Submit**. Choose a person under **Select Assignee**, add a **Due date** if you want one, and enter **Add notes**. Form projects move through **Select**, **Review**, **Approve** and **End**. Rate projects move from **Select** to **End**.

When every child project reaches **End**, the combined project shows that all its projects are complete.

## Fields

| Where | Field | Example |
|---|---|---|
| Finalize | **Project title** | Personal Auto – Fall 2026 forms and rates update |
| Finalize | **Project description** | Fall 2026 edition update for forms and rates |
| Finalize | Workflow | **Product Update** for forms, **Rate Update** for rates |
| Finalize | **Due date** | Pick from the calendar |
| Add form changes / Add rate changes | **Updated edition** | 01 27 |
| Submit | **Add notes** | Ready for review. |

Keep the description short: only the first 100 characters are kept.

`TODO verify`:
- whether Finalize asks for an **Owner** (not shown on the current build for a forms-only project)
- the label of the button that opens **Add rate changes**

## Next

[Create filings from your project](create-filings.md)
