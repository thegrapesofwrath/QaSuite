# Slice and Dice Pandas DataFrames via Indexes

In this exercise you'll learn how to use indexes to select specific portions (via rows and columns) of a Pandas DataFrame.

## Instructions

Perform the following:

1. Import the `pandas` and `pathlib` libraries.

2. Create a variable `csvpath` that represents the path to the [people_cleansed.csv](Resources/people_cleansed.csv) using the Pathlib library.

3. Read the CSV into a Pandas DataFrame and display a few rows.

4. Index Selection with `iloc`:

    1. Select the second row of the DataFrame using `iloc`.

    2. Select the first 5 rows of the DataFrame using `iloc`.

    3. Select the third column using `iloc`.

    4. Select the second to last column using `iloc`.

    5. Select the first five columns using `iloc`.

    6. Select the 2nd, 4th, 6th, and 8th rows of the 1st, 3rd, and 5th columns using `iloc`.

    7. Select the first 5 rows of the 2nd, 3rd, and 4th columns using `iloc`.

    8. Modify the `last_name` column value of the third row using `get_loc` and `iloc`.

5. Index Selection with `loc`:

    1. Set the `First_Name` column as the Pandas DataFrame index.

    2. Sort the DataFrame by the `First_Name` index in descending order.

    3. Select the row with the `First_Name` index "Robert" using `loc`.

    4. Select the rows where `Gender` is equal to 'Female' using `loc`.

    5. Change the `First_Name` value of the rows with 'Zerk' as the `First_Name` index to 'A.A.-Ron'.

---

© 2020 Trilogy Education Services, a 2U, Inc. brand. All Rights Reserved.
