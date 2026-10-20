---
title: Update rules
audience: internal
goals:
  - Start a rules project for a published product
  - Add your rule changes and move the project to End
video: ""
---

# Update rules

A rules project changes the rules of a product that's already published in the Product Vault. You run it in the Project Workbench (the Workbench), like a [forms](update-forms.md) or [rates](update-rates.md) update.

## Before you start

- The product is published in each state you want to change. Only published states can be picked. See [Review and publish](../product-vault/review-and-publish.md).
- Have the updated rules manual ready.

## Steps

1. Go to **Workbench**, select **+ New project**, then choose **Product update**. See [Start a product update](create-project/product-update.md).
2. In **Setup**, under **Project type**, choose **Rules**. Select **Next**.
3. In **Configuration**, choose the product and the states (jurisdictions) to change.
4. In **Finalize**, enter a title and description, choose the **Rule Update** workflow, and pick a due date from the calendar. Select **Create**. `TODO verify` the Finalize field labels for a rules project.
5. In the rules project, add your rule changes. `TODO verify` the name of the add-rule-changes action and its dialog.
6. Move the project to **End** with **Submit**. See [Move work through phases](phases.md).

!!! note "Uploading a whole manual"
    A manual you upload in a rules project is added as one rule. It isn't split into separate rules, and a rules project can't copy rules from another state.

## Reuse rules from another state

When you add a state, you can reuse the rules already generated for an earlier state: download the generated rules from that state's earlier project and add them to the new state's rules project. `TODO verify` these steps. This path hasn't been tested yet.

## What happens next

When the project reaches **End**, complete it. See [Complete a project](complete-project/index.md).
