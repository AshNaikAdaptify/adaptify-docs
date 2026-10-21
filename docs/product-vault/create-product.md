---
title: Create a product
audience: internal  # final audience: external (flips in a release PR)
goals:
  - Add a new product to the Vault
  - Choose its insurance type, lines of business, Group, Underwriting company and states
video: ""
---

# Create a product

Creating a product gives it a place in the Vault. You add its files in the next step.

## Before you start

Your organization admin sets up the **Group** and **Underwriting company** lists once. See [Before you start](before-you-start.md).

## Steps

1. Open **Product Vault** and select **Add product**. (On the Dashboard, **Import product** also takes you to the Product Vault.)
2. Enter a **Product name** and a **Description**.
3. Choose an **Insurance type**, **Personal** or **Commercial**, then choose the **Lines of business**.
4. Choose your **Group**, then your **Underwriting company**.
5. Under **Jurisdictions**, select every state the product needs. Double-check them before you save, for example AK, not AZ.
6. Select **Add product**. You see "Product created successfully".
7. Find the product in the **Product catalog**. Its status shows **Pending Import**, ready for its files.

When you open the product, its state reads "No releases yet — publish this jurisdiction to create its initial release." It gets its first release, **Baseline**, when you publish it.

!!! note
    If **Underwriting company** shows **No Options**, its companies aren't linked to your Group yet. Ask your organization admin.

## Lines of business

Your organization's lists may differ. For example:

| Insurance type | Lines of business |
|---|---|
| Personal | Homeowners, Auto, Dwelling Property, Homeowners By Peril |
| Commercial | Builders Risk, Motor Truck Cargo, Inland Marine, Commercial Output |

## Add product or a Workbench project?

**Add product** creates the product right away, with no Workbench project and no release yet. Use it when you have the product's documents ready to upload, process and publish yourself.

!!! tip "Made a mistake?"
    While none of the product's states is published, you can still delete it. See [Delete Product](delete-product.md).

Next: [Upload documents for a state](import-documents.md).
