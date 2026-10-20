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

Use this to add a state to a product that's already in the Vault, for example adding Alaska to Personal Auto from its Alabama forms. The new state starts with the source state's forms. You then review them, add the new state's own forms and publish.

!!! note "Check this flow on the current build"
    These steps were checked on an earlier build. The **New project** menu has changed since. `TODO verify` every step on the current build.

## Before you start

- The product is published in the source state. See [Review and publish](../review-and-publish.md).
- This project covers forms only.

## Steps

1. In **Workbench**, choose **+ New project**, then **New product**. See [Create a project](../../workbench/create-project/index.md).
2. **Product:** under **Product type**, choose **New jurisdiction for existing product**.
3. **Project:** under **Project type**, choose **Forms**.
4. **Configuration:** under **Product source type**, choose **Product Vault**. Choose the **Existing product**, the **Target jurisdiction** (for example Alaska) and the **Type of insurance**.
5. **Finalize:** enter the **Project title** and **Project description**, then create the project. The project opens with the source state's forms on the **Forms** tab.
6. Check the copied forms. Remove any form that only applies to the source state, such as an Alabama amendatory endorsement. `TODO verify` how to remove one.
7. Move the project through its phases with **Submit**. At **End**, choose **Complete project**, then the **Non-admitted** tab. Check the preview of included and new assets, then confirm.

In the Vault, the new state now has a **Baseline** release marked **Current release**. See [Understand releases](../releases.md).

## Add the new state's own form

On the project, open **New document** and choose **New document** under **Document type**. Enter a **Form number** and check its availability. If it reads "Available. Use this number to lock it before continuing.", lock it, then add the **Edition** and **Form Name**. You see "Form number locked for this form."

`TODO verify`:
- the step that follows Configuration (the current build lists a **Source** step)
- the button that opens **New document**, and the button that locks the number
- how to upload the form's file
- the confirm button in **Complete project**
