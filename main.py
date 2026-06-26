import numpy as np
import pandas as pd
import scipy.stats as stats
from typing import *

def ttest(x, y, var, sample_size, cnt_groups):
    std = np.sqrt(var)
    n1 = len(x)
    n2 = len(y)

    xm = x.mean()
    ym = y.mean()
    diff = xm - ym

    t = diff / (std * np.sqrt(1 / n1 + 1 / n2))
    df = sample_size - cnt_groups
    # F(-t) = 1 - F(t) ???
    if t >= 0:
        pval = 2 * (1 - stats.t.cdf(t, df))
    else:
        pval = 2 * stats.t.cdf(t, df)

    return pval


def bstest(x, y, alpha=0.05):
    if len(x) != len(y):
        print("samples should have equal size")

    n = len(x)
    xm = x.mean()
    ym = y.mean()
    diff = xm - ym

    var_x = np.var(x, ddof=1)
    var_y = np.var(y, ddof=1)

    z_stat = sqrt(n) * diff / sqrt(var_x + var_y)
    if z_stat >= 0:
        pval = 2 * (1 - stats.norm.cdf(z_stat))
    else:
        pval = 2 * stats.norm.cdf(z_stat)

    
    q = (-1) * stats.norm.ppf(alpha / 2)
    half_len = q * sqrt(var_x + var_y) / sqrt(n)
    l = diff - half_len
    r = diff + half_len
    
    return pval, (l, r)


def anova(data: array_like):

    # data[group][obj_ix]
    # x[obj_ix][group]
    x = pd.DataFrame(data).T
   
    total_mean = x.mean(axis=None)
    groups_mean = x.mean(axis=0)
    groups_card = (~pd.isna(x)).sum(axis=0)

    outer_var = groups_card * (groups_mean - total_mean) ** 2 
    outer_var = outer_var.sum()

    data_centered = x - groups_mean
    inner_var = (data_centered**2).sum().sum()

    n = (~pd.isna(x)).sum().sum() # total_sample_size
    k = x.shape[1] # cnt_groups
    dfn = k - 1
    dfd = n - k
    f_stat = (outer_var / dfn) / (inner_var / dfd)

    pval = 1 - stats.f.cdf(f_stat, dfn, dfd)
    
    var_estimator = inner_var / dfd 

    return pval, var_estimator, n, k


def chisq_indep():
    pass

    


# data = [
# [38.7, 39.2, 40.1, 38.9],
# [41.9, 42.3, 41.3],
# [40.8, 41.2, 39.5, 38.9, 40.3],
# ]

# data = [
# [5, 9, 6, 8],
# [11, 13, 10, 12],
# [10, 6, 9, 9],
# ]


anova_p, var_est, n, k = anova(data)


print(ttest(
     np.array(data[1]),
     np.array(data[2]),
     var_est,
     n,
     k
     ))
