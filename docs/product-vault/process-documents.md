---
title: Process documents
audience: internal
goals:
  - Add the form and manual metadata that processing needs
  - Read form numbers and editions from file names
  - Run Process Documents and know when it is done
video: ""
---

# Process documents

Processing turns uploaded files into Vault assets. It needs a little metadata first.

## 1. Add form metadata

1. Open the jurisdiction → **Forms**.
2. Open a row's metadata dialog.
3. Enter **Form Number** and **Edition**. These are the only required fields.
4. Close the dialog. Closing saves your changes.

Form file names usually follow `{PREFIX} {NNNN} {MM} {YY}  {Title}.docx`:

| File name starts with | Form Number | Edition |
|---|---|---|
| `PPA 0001 07 16` | `PPA 0001` | `07 16` |
| `HO 0003 09 20` | `HO 0003` | `09 20` |

## 2. Add manual editions

1. Open **Manuals**.
2. For each row, select **Edit**, enter the **Edition**, then **Save Metadata**.

| File name clue | Edition |
|---|---|
| `01 21`, `Rev 06 21` | `01 21`, `06 21` |
| Four digits at the end, such as `0823` | `08 23` |

## 3. Process

1. Select **Process Documents** once.
2. The status moves to **Processing**, then **Processed**. This can take a minute or two. Refresh the page to see the update.
3. When processing is done, you see **Rater** and **Review & Publish**.

!!! tip
    Select **Process Documents** only once and give it time to finish.

Next: [Review and publish](review-and-publish.md).
