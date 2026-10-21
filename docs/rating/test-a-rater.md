---
title: Test a rater
audience: internal  # final audience: external (flips in a release PR)
goals:
  - Create and run a manual test case
  - Use the Rate Log to check the math
video: ""
---

# Test a rater

Test a rater by entering rating inputs and comparing the premium Adaptify works out with the premium you expect.

## Create a test case

1. Open the rater and choose the **Manual tests** tab.
2. Select **Create test case**.
3. In **Add new manual test**, enter the **Test case name** and the **Expected premium**, then select **Add test**. You'll see "Test case added successfully".

Each test case in the list has **Export**, **Copy**, **Edit** and **Delete**. You can also **Import** test cases from a JSON file exported from manual tests, or **Export all**.

![The Add new manual test dialog with Test case name and Expected premium](../assets/rating/add-new-manual-test.webp)

## Run a test

1. Open the test case. You'll see the **Expected Premium** and **Actual Premium**.
2. On **Rating Inputs**, fill in the inputs. These are the fields marked as rating inputs in the structure, in sequence-number order. Use the **Policy** tree on the left to move between risk items.
3. Select **Execute Test**. A message tells you whether the test passed, with the premium.

If a required input is missing, the test fails. Fill it in and run the test again.

![A test case with Expected Premium, Actual Premium, Execute Test and the Rating Inputs](../assets/rating/test-case-inputs.webp)

## Read the Rate Log

Choose **Rate Log** to follow the math step by step. It's the quickest way to find out why a premium is off.

- The list on the left shows each calculation, grouped by risk item.
- For each table lookup, you see the **Input** and **Output**: the field, its path and its value.
- For each calculation, you see each step with the numbers filled in and its result.
- For each branch, you see the **IF**, **THEN** and **ELSE**, with the path that was taken.

Use the filters at the top, such as **Risk Item**, **Coverage** and **Node Type**, to narrow the log.

![The Rate Log with calculation steps and the numbers used in each one](../assets/rating/rate-log-steps.webp)

## Test suites

To run a batch of tests from a spreadsheet, use the **Test suites** tab:

1. Select **Download template** and fill it in.
2. Select **Create test suite**, enter the **Test suite name**, choose your file (XLSX, XLS or CSV), and select **Create**. You can also use **Import with template**.

Each suite shows its **Name**, how many tests **Passed** and **Failed**, the **File**, **Last Run** and **Status**.
