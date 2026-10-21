---
title: Rate order
audience: internal  # final audience: external (flips in a release PR)
goals:
  - Set the order your calculations run in
video: ""
---

# Rate order

The rate order is the order Adaptify runs your calculations in. Open the rater and choose the **Rate order calculation** tab.

The calculations are numbered and grouped by risk item, such as **Location** and **Policy**. Use **Search** and **Type** to find one. Select **Edit** to change the order. Until a rater has calculations, the tab reads "No calculations found".

![The Rate order calculation tab with Search, Type and Edit](../assets/rating/rate-order-calculation.webp)

## Get the order right

- Put the tables before the calculations that use them.
- Put **Total Premium** last.

When you're done, open the rater's **Actions** menu and choose **Validate**.

## Next

[Test a rater](test-a-rater.md)
