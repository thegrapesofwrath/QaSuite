# Column Manipulation of Pandas DataFrames

This is an exercise in which you will learn to manipulate the structure of a Pandas DataFrame, namely its columns. Often times, it is necessary to alter the structure of a Pandas DataFrame to fit the needs of the user.

## Instructions

Perform the following:

1. Import the `pandas` and `pathlib` libraries.

2. Create a variable `csvpath` that represents the path to the [people.csv](Resources/people.csv) using the Pathlib library.

3. Read the CSV into a Pandas DataFrame using the `csvpath` variable and display a few rows of the DataFrame.

4. View the column names of the Pandas DataFrame.

5. View the column data types of the Pandas DataFrame.

6. Rename the columns of the Pandas DataFrame to "Person_ID", "First_Name", "Last_Name", "Email", "Gender", "University", "Occupation", "Salary".

7. Alternatively, rename the columns of the Pandas DataFrame using a Dictionary.

8. Re-order the columns of the Pandas DataFrame to "Person_ID", "Last_Name", "First_Name", "Gender", "University", "Occupation", "Salary", "Email".

    **Bonus:** Tackle the bonus activity if you finish early.

9. Add the [Numpy](https://numpy.org/) library to your list of imported libraries.[Numpy](https://numpy.org/)

    If you are unfamiliar with the numpy library the typical import statement reads:

    ```python
    import numpy as np
    ```

10. Create two additional columns: `Age` and `Age_Copy`. Use the `randint` function from the `numpy` library with the `low`, `high`, and `size` parameters set to `22`, `65`, and `1000`, respectively, to randomly generate an integer from 22 to 65 for 1000 rows.

      The numpy code to generate the randome values is as follows:

      ```python
      np.random.randint(low=22, high=65, size=1000)
      ```

11. Delete the newly created `Age_Copy` column.

12. Save the modified DataFrame to a new CSV, and put the file in the `Resources` folder.

---

© 2020 Trilogy Education Services, a 2U, Inc. brand. All Rights Reserved.
