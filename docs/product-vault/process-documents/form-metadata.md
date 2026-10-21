---
title: Add form numbers and editions
audience: internal  # final audience: external (flips in a release PR)
goals:
  - Add the form number and edition for each form
  - Read both from the form's file name
video: ""
---

# Add form numbers and editions

Every form needs a **Form Number** and an **Edition** before you process the state. You enter them yourself. Processing doesn't fill them in from the file name.

## Steps

1. Open the product, choose the state under **Jurisdiction**, and open the **Forms** tab.
2. On a form, select the pencil icon to open its details.
3. Enter the **Form Number** and **Edition**. These are the only required fields.
4. Save your changes and close the dialog.

Repeat for each form. A form shows **Metadata incomplete** until its details are in.

## Read them from the file name

Form file names usually start with the form number and edition, for example `PPA 0001 07 16 Personal Automobile Policy.docx`:

| File name starts with | Form Number | Edition |
|---|---|---|
| `PPA 0001 07 16` | `PPA 0001` | `07 16` |
| `HO 0003 09 20` | `HO 0003` | `09 20` |

The form number is a prefix plus four digits. The edition is the month and year, as `MM YY`.

Next: [Add manual editions and set up rules](manual-editions-and-rules.md).
