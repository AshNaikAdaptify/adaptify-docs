---
title: Copy a state's forms to a new state
audience: internal  # final audience: external (flips in a release PR)
goals:
  - Start a project that adds a new state from an existing state's forms
  - Add the new state's own forms
  - Publish the new state's Baseline
video: ""
---

# Copy a state's forms to a new state

Use this to add a state to a product that's already in the Vault, starting from another state's forms, for example adding Alaska to Personal Auto from its Alabama forms. The new state starts with the source state's forms. You then review them, add the new state's own forms and publish.

!!! note "Check this flow on the current build"
    Steps 1–5 (the project wizard) were checked on the current build, without creating the project. Steps 6 and 7 and the new-form steps were checked on an earlier build. `TODO verify` them on the current build.

## Before you start

- The product is published in the source state. See [Review and publish](../review-and-publish.md).
- `TODO verify` whether rates and rules copy too. On an earlier build, this project covered forms only.

## Steps

1. In **Workbench**, choose **+ New project**, then **New product**. For each wizard step, see [Start a project to add a state](../../workbench/create-project/new-jurisdiction.md).
2. **Product:** under **Product type**, keep **New jurisdiction for existing product**.
3. **Project:** under **Project type**, choose **Forms**.
4. **Configuration:** under **Product source type**, keep **Product Vault**. Choose the **Source product** and the **Source jurisdiction** to copy from, for example Alabama.
5. **Source:** choose the **Target jurisdiction** (for example Alaska) and the **Type of insurance**. Then in **Finalize**, enter the **Project title**, **Project description**, **Workflow** and **Due date**, and select **Create project**. `TODO verify` that the project opens with the source state's forms on the **Forms** tab.
6. Check the copied forms. The source state's own state-specific forms, such as an Alabama amendatory endorsement, can be copied too. This is a known issue. Remove any form that only applies to the source state. `TODO verify` how to remove one.
7. Move the project through its phases with **Submit**. At **End**, choose **Complete project**, then the **Non-admitted** tab. Check the preview of included and new assets, then confirm.

In the Vault, the new state now has a **Baseline** release marked **Current release**. See [Understand releases](../releases.md).

## Add the new state's own form

On the project, open **New document** and choose **New document** under **Document type**. Enter a **Form number** and check its availability. If it reads "Available. Use this number to lock it before continuing.", lock it, then add the **Edition** and **Form Name**. You see "Form number locked for this form."

`TODO verify`:
- the button that opens **New document**, and the button that locks the number
- how to upload the form's file
- the confirm button in **Complete project**

To add a state from its own files instead, see [Add a state with Edit product](edit-product.md). To compare both ways, see [Add a state to a product](index.md).
