---
title: Rate order
audience: internal  # final audience: external (flips in a release PR)
goals:
  - Set the order your calculations run in
video: ""
---

# Rate order

The rate order is the order Adaptify runs your calculations in. Open the rater and choose the **Rate order calculation** tab.

The calculations are numbered in the order they run, grouped by risk item. For example, **Vehicle (1 to N)** lists **1 Bodily Injury Liability**. Use **Search** and **Type** to find a calculation, and select **Edit** to change the order. Until a rater has calculations, the tab reads "No calculations found".

![The Rate order calculation tab with the Bodily Injury Liability calculation under Vehicle](../assets/rating/rate-order-calculation.webp)

## Get the order right

- Inside each flow, put the table lookup before the calculation that uses its value.
- If you have a total premium calculation, put it last.

When you're done, open the rater's **Actions** menu and choose **Validate**.

## Next

[Test a rater](test-a-rater.md)
