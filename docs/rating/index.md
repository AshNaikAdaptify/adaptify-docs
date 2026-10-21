---
title: How rating works in Adaptify
audience: internal  # final audience: external (flips in a release PR)
goals:
  - Understand the parts of a rater and the order you build them in
  - Know where each part lives in Adaptify
video: ""
---

# How rating works in Adaptify

A rater works out the premium for a product. In the [Rating Catalog](../rating-catalog/index.md), each rater ties a product and one of its jurisdictions to the rating structure it's built on.

You build a rater in five parts, in this order:

**Rating structure** → **Rating tables** → **Calculations** → **Rate order** → **Tests**

| Part | What it is | Where |
|---|---|---|
| **Rating structure** | Every risk item, coverage and field your rating uses, such as Policy, Location, Zip code or Protection Class. | **Rating Administration** → **Rating Structure**. See [Rating structures](rating-structures.md). |
| **Rating tables** | Your rate tables and factor tables. Each column is linked to a field in the structure. | The rater's **Tables** tab. See [Rating tables](rating-tables.md). |
| **Calculations** | The steps that turn table values and inputs into premium, drawn as a flow. | The rater's **Calculations** tab. See [Calculations](calculations.md). |
| **Rate order** | The order Adaptify runs the calculations in. | The rater's **Rate Order Calculation** tab. See [Rate order](rate-order.md). |
| **Tests** | Test cases with an expected premium, so you can check the rater gives the right answer. | The rater's **Manual Tests** and **Test Suites** tabs. See [Test a rater](test-a-rater.md). |

## Start with the structure

Everything your rating uses to develop the rate lives in the rating structure. Set it up first: tables and calculations can only use fields that are already in the structure.

## Next

- [Rating structures](rating-structures.md)
- [Open a rater](open-a-rater.md)
