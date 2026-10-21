---
title: Rate order
audience: internal  # final audience: external (flips in a release PR)
goals:
  - Set the order your calculations run in
video: ""
---

# Rate order

The rate order is the order Adaptify runs your calculations in. Open the rater and choose the **Rate Order Calculation** tab.

The calculations are numbered and grouped by risk item, such as **Protected Devices**, **Location** and **Policy**. Use **Search Calculations** and **Type** to find one. Select **Edit** to change the order.

![The Rate Order Calculation tab with numbered calculations grouped by risk item](../assets/rating/rate-order-calculation.webp)

## Get the order right

- Put the tables before the calculations that use them.
- Put **Total Premium** last.

When you're done, select **Validate** above the rater's tabs. **Import** and **Export** sit next to it.

## Next

[Test a rater](test-a-rater.md)
