---
title: Before you start
goals:
  - Sign in and confirm you are in the right tenant
  - Set up the Group and Underwriting Company lists that new products need
  - Check that your product list is ready
video: ""
---

# Before you start

A few one-time setup steps make creating products in the Vault smooth.

## Sign in and choose your tenant

1. Sign in with your email first, then your password.
2. Open the user menu (your initials) and confirm the organization shown, for example `Organization — {tenant}`.
3. To change tenant, choose **Switch Tenant** and select the tenant you want, then **Confirm**.

!!! tip "Use a test tenant for practice"
    Try new steps in a test tenant first. Administrators viewing another tenant see a yellow banner with **Switch Back**.

## Set up Group and Underwriting Company

Every product needs a **Group** and an **Underwriting Company**. Underwriting Company depends on Group, so each company must sit under a group.

1. Go to **System Administration** → **Lists**.
2. Create the **Group** value first.
3. Open **Underwriting Company** and choose the **Grouped by Group** view.
4. Select **+ Add value under {Group}** and enter the company name.
5. Reload the page and reopen **Underwriting Company**. The companies should still appear under the group.

!!! note
    If the **Underwriting Company** field later shows **No Options** when you create a product, the companies are not linked to a group yet. Repeat the steps above.

## Check your product list

Products are created from your tenant's product list (lines such as Personal and Commercial, and products such as Auto or Homeowners). Make sure the products you need are on the list before you create them. `TODO verify` where the product list is managed.
