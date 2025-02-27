# **Implicit Biased Set (IBS) Identification Algorithm**

## **Overview**
This script implements an **Implicit Biased Set (IBS) Identification Algorithm** to detect **biased subgroups** in datasets using protected attributes. It processes datasets, computes imbalance ratios, and visualizes results.

---

## **Table of Contents**
- [Installation](#installation)
- [Usage](#usage)
- [Functions](#functions)
  - [Data Processing](#data-processing)
  - [Ratio Computation](#ratio-computation)
  - [Handling Imbalances](#handling-imbalances)
  - [IBS Algorithm](#ibs-algorithm)
  - [Running Tests](#running-tests)
- [Datasets Used](#datasets-used)
- [Visualization](#visualization)
- [Authors](#authors)

---

## **Installation**
### **Dependencies:**
Ensure you have the required Python libraries installed:
```bash
pip install pandas numpy seaborn matplotlib sympy
```

---

## **Usage**
To run the IBS Identification Algorithm on a dataset:
```python
from ibs_identification import implicit_biased_set_identification

time_taken, max_updates = implicit_biased_set_identification(data, protected_attributes, y_label, imbalance_threshold=0.1, k=10)
```

To execute **predefined dataset tests**, run:
```python
from ibs_identification import run_tests
run_tests(X, check_cols, y)
```

---

## **Functions**

### **Data Processing**
#### `get_protected_attr_data(data, protected_attr, y_label)`
- Extracts **protected attributes** and **target variable (`y_label`)**.
- Groups data **with and without `y_label`**.

#### `get_parents_and_cnt_regions(data, protected_att, label)`
- Finds **parent groups** by removing one attribute at a time.

#### `construct_hierarchy(protected_attributes)`
- Generates all possible **non-empty subsets** of `protected_attributes`.

---

### **Ratio Computation**
#### `Calculate_ratio_rn(group_lst, parents, pos, neg)`
- Computes **neighboring region imbalance ratio (`ratio_rn`)** using parent groups.

#### `compute_ratio(data, att_vals, protected_att, y_label)`
- Filters `data` by `att_vals`.
- Returns **positive (`pos`), negative (`neg`), and total counts**.

---

### **Handling Imbalances**
#### `handle_imbalance(ratio_rn, pos, neg, group_lst, need_pos, need_neg, imbalance_threshold)`
- Determines if a **group is imbalanced** based on `ratio_rn` and `imbalance_threshold`.
- Updates **`need_pos` or `need_neg`** lists.

---

### **IBS Algorithm**
#### `implicit_biased_set_identification(data, protected_attr, y_label, imbalance_threshold, k, verbose=True)`
- Identifies **biased subgroups** using protected attributes.
- **Steps:**
  1. Builds **hierarchical groups**.
  2. Iterates **bottom-up** through subgroups.
  3. Computes **imbalance ratios**.
  4. Filters **small groups (`k` threshold)**.
  5. Stores results in **scatter plot visualization**.

---

### **Running Tests**
#### `run_tests(X, check_cols, y)`
- Runs **multiple experiments** with varying `k` and `imbalance_threshold`.
- Produces:
  - **Execution Time vs. `k`** plot.
  - **Max updates vs. `imbalance_threshold`** plot.

---

## **Datasets Used**
### **German Credit Data (`german_credit_data.csv`)**
- **Protected attributes:** `['Age', 'Sex', 'Job', 'Saving accounts']`
- **Target variable:** `'class'`
- Runs `run_tests()`.

### **COMPAS Dataset (`CleanAdult_numerical_cat.csv`)**
- **Protected attributes:** `['age', 'marital-status', 'relationship', 'race', 'gender', 'native-country']`
- **Target variable:** `'income'`
- Runs `run_tests()`.

### **Stop, Question, and Frisk (`SQFD - CY 2017.csv`)**
- Converts `Y/N` → `1/0` in **'SUSPECT_ARRESTED_FLAG'**.
- **Protected attributes:** `['Age', 'Sex', 'Race']`
- Runs `run_tests()`.

### **Credit Card Default (`default of credit card clients.xls`)**
- **Protected attributes:** `['X2', 'X3', 'X4', 'X5']`
- **Target variable:** `'Y'`
- Runs `run_tests()`.

---

## **Visualization**
### **Scatter Plot Example (Identifying Imbalances)**
This script generates a scatter plot of **protected attribute subgroups**, showing the imbalance in `need_pos` and `need_neg`.

```python
# Example Output:
sns.scatterplot(x=subgroups, y=need_pos_values, color='blue', marker='o', label='Need Pos')
sns.scatterplot(x=subgroups, y=need_neg_values, color='red', marker='x', label='Need Neg')
sns.scatterplot(x=subgroups, y=need_total_values, color='green', marker='o', label='Need Total')
```

---

## **Authors**
**Adi Cohen & Dan Zlotnikov** 

## **License**
This project is licensed under the MIT License - see the `LICENSE` file for details.

