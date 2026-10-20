---
title: Record approval and archive to a new release
audience: internal  # final audience: external (flips in a release PR)
goals:
  - Record the state's approval on the filing
  - Archive the filing so the state gets a new release in the Product Vault
video: ""
---

# Record approval and archive to a new release

Do this when the state approves the filing. Archiving the approved filing creates that state's new release in the Product Vault.

## Steps

1. On the filing, choose the **Pending** chip next to **Submission**.
2. Set **Disposition status** to **Approved** and pick the **Change date** from the calendar. Save. The submission shows **Approved**. See [Filing statuses and dispositions](../filing-manager/statuses.md).
3. Choose **Archive project**.
4. In **Archive project**, check the **Destination product state** (product and state). Under **Release association**, choose **Create new release**. The **Release version** fills in for you.
5. Enter the **New business effective date**, the **Renewal effective date** and a **Description**, then archive. A success message appears.
6. Repeat for each state's filing.

## Fields

| Field | Example |
|---|---|
| **Release version** | Filled in for you, for example 1 |
| **New business effective date** | 12/01/2026 |
| **Renewal effective date** | 12/01/2026 |
| **Description** | Fall 2026 forms and rates update |

`TODO verify`:
- the labels of the save and archive buttons
- where **Archive project** sits on the filing
- when to use the other **Disposition status** values (**Disapproved**, **Withdrawn**, **Closed**, **Noted**)
- when to add the filing to an existing release instead of creating a new one

## Next

[Check the new release in the Product Vault](check-new-release.md)
