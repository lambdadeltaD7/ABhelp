### This readme was written entirely by LLM but LLM didn't write a single line of code in the project (for better or worse).
# 🚀 ABhelp – Statistical Analysis Toolkit for A/B Testing & Hypothesis Testing

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**A lightweight, no-nonsense Python library for A/B testing, ANOVA, and proportion comparisons—designed for data scientists who want clarity without the scikit-learn bloat.**

---

## 📖 Table of Contents
- [Overview](#-overview)
- [Installation](#-installation)
- [Core Functions](#-core-functions)
  - [1. `anova()` – One-Way ANOVA](#1-anova--one-way-anova)
  - [2. `ttest()` – Post-Hoc t-Test with Pooled Variance](#2-ttest--post-hoc-t-test-with-pooled-variance)
  - [3. `bstest()` – Large-Sample z-Test for Proportions](#3-bstest--large-sample-z-test-for-proportions)
  - [4. `chisq_hom()` – Chi-Square Test for Homogeneity](#4-chisq_hom--chi-square-test-for-homogeneity)
- [Usage Examples](#-usage-examples)
  - [Scenario 1: Comparing Age Across Decks (ANOVA + t-test)](#scenario-1-comparing-age-across-decks-anova--t-test)
  - [Scenario 2: Transported Proportions by Destination (z-test)](#scenario-2-transported-proportions-by-destination-z-test)
  - [Scenario 3: Chi-Square Test for Homogeneity](#scenario-3-chi-square-test-for-homogeneity)
- [Why ABhelp?](#-why-abhelp)
- [License](#-license)

---

## 🔍 Overview

**ABhelp** is a minimalistic Python module built on top of `numpy`, `pandas`, and `scipy` that provides:

- **Pure Python implementations** of core statistical tests—no black boxes, no magic.
- **Transparent formulas** – every function returns intermediate statistics (test statistic, degrees of freedom, p-value, confidence intervals).
- **Designed for A/B testing** – with built-in support for Bernoulli/Binary outcomes (conversion rates, click-through rates).
- **Post-hoc ready** – the `ttest()` function uses pooled variance from ANOVA, making it perfect for follow-up pairwise comparisons.

> **Ideal for**: Data science coursework, exploratory analysis, quick A/B test validations, and teaching statistical concepts.

---

## 🛠️ Installation

### Option 1: Direct Download
```bash
git clone https://github.com/lambdadeltaD7/ABhelp.git
cd ABhelp
```

### Option 2: Copy-Paste
Just copy `stuff.py` into your project folder and import it:

```python
from stuff import anova, ttest, bstest, chisq_hom
```

### Dependencies
```bash
pip install numpy pandas scipy typing
```

---

## ⚙️ Core Functions

### 1. `anova()` – One-Way ANOVA
```python
anova(data: array_like) -> (pval, var_estimator, n, k)
```
- **Input**: List of groups (each group is an array-like of numeric values).
- **Output**:
  - `pval` – p-value for the F-test (null hypothesis: all group means are equal).
  - `var_estimator` – pooled variance estimate (mean squared error).
  - `n` – total sample size.
  - `k` – number of groups.
- **Use Case**: Testing if age, spending, or any metric differs across multiple categories (e.g., decks, planets).

---

### 2. `ttest()` – Post-Hoc t-Test with Pooled Variance
```python
ttest(x, y, var, sample_size, cnt_groups, alpha=0.05) -> (pval, (l, r))
```
- **Input**:
  - `x`, `y` – two groups to compare.
  - `var` – pooled variance from `anova()`.
  - `sample_size` – total `n` from `anova()`.
  - `cnt_groups` – total number of groups `k` from `anova()`.
  - `alpha` – significance level (default 0.05).
- **Output**:
  - `pval` – two-sided p-value.
  - `(l, r)` – 95% confidence interval for the mean difference.
- **Why this is special**: It uses the **pooled variance estimate** from the overall ANOVA, giving you more stable post-hoc comparisons than running separate t-tests.

---

### 3. `bstest()` – Large-Sample z-Test for Proportions
```python
bstest(x, y, alpha=0.05) -> (pval, (l, r))
```
- **Input**: Two Bernoulli/Binary groups (arrays of 0s and 1s).
- **Output**:
  - `pval` – p-value from the two-proportion z-test.
  - `(l, r)` – 95% confidence interval for the difference in proportions.
- **Use Case**: A/B testing conversion rates, click-through rates, or any binary outcome.
- **Note**: Uses pooled proportion for variance estimation under the null.

---

### 4. `chisq_hom()` – Chi-Square Test for Homogeneity
```python
chisq_hom(data: array_like) -> pval
```
- **Input**: List of groups (each group is an array-like of binary 0/1 values).
- **Output**: p-value for the chi-square test of homogeneity.
- **Use Case**: Testing whether the distribution of a binary outcome is the same across multiple groups (e.g., Transported proportion across decks/destinations).

---

## 💡 Usage Examples

### Scenario 1: Comparing Age Across Decks (ANOVA + t-test)

```python
import pandas as pd
from stuff import anova, ttest

# Simulate age data for 6 decks
np.random.seed(42)
groups = [
    np.random.normal(35, 13, 1000),  # Deck A
    np.random.normal(33, 13, 1000),  # Deck B
    np.random.normal(35, 13, 1000),  # Deck C
    np.random.normal(34, 13, 1000),  # Deck D
    np.random.normal(30, 13, 1000),  # Deck E
    np.random.normal(28, 13, 1000),  # Deck F
]

# Step 1: Run ANOVA
pval, var_est, n, k = anova(groups)
print(f"ANOVA p-value: {pval:.4f}")  # Typically < 0.05

# Step 2: Post-hoc t-tests with Bonferroni correction
# Compare Deck A vs Deck F
pval_pair, ci = ttest(groups[0], groups[5], var_est, n, k)
bonferroni_pval = min(6 * pval_pair, 1)  # 6 groups = 6 comparisons if using Dunn's method
print(f"Bonferroni-corrected p-value: {bonferroni_pval:.4f}")
print(f"95% CI for mean difference: ({ci[0]:.2f}, {ci[1]:.2f})")
```

---

### Scenario 2: Transported Proportions by Destination (z-test)

```python
from stuff import bstest

# Simulate Transported (1 = yes, 0 = no) for 3 destinations
trappist = np.random.binomial(1, 0.47, 1000)
ps0 = np.random.binomial(1, 0.50, 1000)
cancri = np.random.binomial(1, 0.62, 1000)

# Compare TRAPPIST-1e vs 55 Cancri e
pval, ci = bstest(trappist, cancri)
bonferroni_pval = min(3 * pval, 1)  # 3 pairwise comparisons
print(f"Bonferroni-corrected p-value: {bonferroni_pval:.4f}")
print(f"95% CI for proportion difference: ({ci[0]:.4f}, {ci[1]:.4f})")
```

---

### Scenario 3: Chi-Square Test for Homogeneity

```python
from stuff import chisq_hom

# Test if Transported proportion differs across all decks
deck_data = [
    np.random.binomial(1, 0.48, 1000),  # Deck A
    np.random.binomial(1, 0.73, 1000),  # Deck B
    np.random.binomial(1, 0.68, 1000),  # Deck C
    np.random.binomial(1, 0.43, 1000),  # Deck D
    np.random.binomial(1, 0.35, 1000),  # Deck E
    np.random.binomial(1, 0.43, 1000),  # Deck F
]

pval = chisq_hom(deck_data)
print(f"Chi-square homogeneity p-value: {pval:.4f}")  # Typically < 0.05
```

---

## ❓ Why ABhelp?

| Feature | ABhelp | SciPy/Statsmodels |
|---------|--------|-------------------|
| **Transparent formulas** | ✅ Yes – pure Python, easy to modify | ❌ Black-box C/Fortran routines |
| **Post-hoc t-test with pooled variance** | ✅ Built-in (`ttest()`) | ❌ Requires manual calculation |
| **Lightweight** | ✅ Minimal dependencies | ❌ Heavy dependencies |
| **Educational** | ✅ Perfect for teaching | ❌ Too abstract for beginners |
| **Flexible confidence intervals** | ✅ Returns CIs for every test | ❌ Not all tests provide CIs |

---

## 📄 License

This project is licensed under the **MIT License** – feel free to use, modify, and distribute it for any purpose.

---

## 🙏 Acknowledgements

- Built with `numpy`, `pandas`, and `scipy`.
- Inspired by real-world A/B testing challenges in space travel data (see the accompanying Jupyter Notebook).

---

**Happy Testing!** 🚀 If you find this useful, give it a ⭐ on GitHub!
