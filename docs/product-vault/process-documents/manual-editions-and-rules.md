---
title: Add manual editions and set up rules
audience: internal  # final audience: external (flips in a release PR)
goals:
  - Give each manual its edition
  - Tell the Vault how your manual headings are numbered, before you process
video: ""
---

# Add manual editions and set up rules

The Vault reads your manuals to find their rules. Give each manual an edition, then confirm how its headings are numbered. For most manuals, the default setup is all you need.

## Add the edition

1. Open the product, choose the state under **Jurisdiction**, and open the **Manual** tab.
2. On each manual, select the pencil icon, enter the **Edition**, then save.

| File name clue | Edition |
|---|---|
| `01 21`, `Rev 06 21` | `01 21`, `06 21` |
| Four digits at the end, such as `0823` | `08 23` |

## Set up rules

1. On the **Manual** tab, select **Configure rules**.
2. On a Word or PDF manual marked **Needs configuration**, select **Configure**.
3. Keep **Configure manually** and accept the defaults. The default **Numbering style** is **Multi-level numbers with dots (1, 1.1, 1.1.2, ...)**.
4. To use the same setup for other manuals, check them under **Apply this configuration to other manuals**.
5. Select **Save**, then **Done**.

Leave Excel manuals (.xls files) alone. You don't need to configure them.

!!! warning "Set up rules before you process"
    After a state is processed, **Configure rules** can become unavailable. This is a known issue, not how it's meant to work. Set up every manual first.

!!! tip "Add editions early"
    Add a manual's edition before you use it in another state. A manual shared across states can lock its **Edition** if you add the edition afterwards, and that blocks publishing. This is a known issue.

Next: [Process documents and check the rules](run-processing.md).
