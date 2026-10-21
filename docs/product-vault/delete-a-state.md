---
title: Delete a State
audience: internal  # final audience: external (flips in a release PR)
goals:
  - Remove a state you added to a product by mistake
  - Know what deleting a state removes and what it keeps
video: ""
---

# Delete a State

Use this to fix a mistake, for example a state you added to the wrong product. It isn't meant for routine cleanup.

You delete a state in the **Edit product** dialog. There's no delete option on the **Jurisdiction** selector, in the **Actions** menu or in the Product Vault list.

## Steps

1. Open **Product Vault** and open the product.
2. Select **Actions**, then **Edit product**.
3. Under **Jurisdictions**, select **×** on the state you want to remove.
4. Select **Save**. A **Please confirm** dialog asks whether you want to delete the state.
5. Select **Delete**. You see "Product updated", and the state is no longer listed under **Jurisdiction**.

!!! warning "This is permanent"
    Deleting a state permanently removes the product state and its documents. Assets still used elsewhere, and published assets, are kept.

## Good to know

A product needs at least one state. If you remove its only state, **Save** stays unavailable.

To delete the whole product instead, see [Delete Product](delete-product.md).
