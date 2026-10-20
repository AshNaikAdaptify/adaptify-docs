---
title: Start a project to add a state
audience: internal  # final audience: external (flips in a release PR)
goals:
  - Start a Workbench project that adds a state to an existing product
  - Choose the source state and the new state
video: ""
---

# Start a project to add a state

A **New jurisdiction for existing product** project adds a state to a product that's already in the Vault. The new state starts from another state's forms. You find it under **New product** in the **New project** menu.

Use this when you're expanding into a new state where you don't have the product yet. If you already sell the product in the state but the state was never added in Adaptify, [add it with Edit product](../../product-vault/add-a-state/edit-product.md) instead.

## Before you start

The product is published in the state you'll copy from. See [Review and publish](../../product-vault/review-and-publish.md).

## Steps

1. In **Workbench**, select **+ New project**, then **New product**.
2. **Product:** under **Product type**, keep **New jurisdiction for existing product**. It's selected at first.
3. **Project:** choose **Forms**.
4. **Configuration:** keep **Product Vault** as the **Product source type**. Choose the **Source product** and the **Source jurisdiction** whose forms you want to copy. **Source jurisdiction** lists only states that have a release.

    ![Configuration step: Product Vault selected, with Source product and Source jurisdiction](../../assets/workbench/add-state-project-configuration.webp)

5. **Source:** choose the **Target jurisdiction** (the new state) and the **Type of insurance**, for example 19.0 Personal Auto. Add a **Subtype of insurance** if one applies. The **Existing product** is already filled in.
6. **Finalize:** enter the **Project title** and **Project description**, choose the **Workflow**, and pick a **Due date** from the calendar. Add anyone else under **Additional members**.

    ![Finalize step with Project title, Project description, Workflow and Due date](../../assets/workbench/add-state-project-finalize.webp)

7. Select **Create project**. The project opens in the **Select** phase. The **Forms** tab lists the source state's forms with the change type **Include**.

![The new project's Forms tab, with a copied form marked Include](../../assets/workbench/add-state-project-forms.webp)

**Target jurisdiction** lists only states the product doesn't have yet.

!!! note "Known limitation: forms only"
    This project copies the source state's forms only. Rates, manuals and supporting materials aren't copied. To add the new state's rules after it's published, see [Update rules](../update-rules.md).

## What happens next

Review the copied forms, add the new state's own forms and publish the new state. See [Copy a state's forms to a new state](../../product-vault/add-a-state/from-existing-state.md).
