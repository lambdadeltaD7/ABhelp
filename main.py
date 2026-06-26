import numpy as np
import pandas as pd
import scipy.stats as stats
from typing import *

# t-test after anova based on pooled variance 
def ttest(x, y, var, sample_size, cnt_groups, alpha=0.05):
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


    q = (-1) * stats.t.ppf(alpha / 2, df)
    half_len = q * std * np.sqrt(1 / n1 + 1 / n2)
    l = diff - half_len
    r = diff + half_len

    return pval, (l, r)

# big sample test for difference in means
# only for bernoulli
def bstest(x, y, alpha=0.05):
    if len(x) != len(y):
        print("samples should have equal size")

    n = len(x)
    xm = x.mean()
    ym = y.mean()
    diff = xm - ym

    var_x = xm * (1 - xm)
    var_y = ym * (1 - ym)

    z_stat = np.sqrt(n) * diff / np.sqrt(var_x + var_y)
    if z_stat >= 0:
        pval = 2 * (1 - stats.norm.cdf(z_stat))
    else:
        pval = 2 * stats.norm.cdf(z_stat)

    
    q = (-1) * stats.norm.ppf(alpha / 2)
    half_len = q * np.sqrt(var_x + var_y) / np.sqrt(n)
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


# only for bernoulli
def chisq_hom(data: array_like):
    cnt_groups = len(data) 

    # table[i] = (cnt0, cnt1) 
    table = [ [len(data[i]) - sum(data[i]), sum(data[i])] for i in range(cnt_groups) ]
    table = np.array(table) # shape = (cnt_groups, 2)

    cnt_total = table.sum()
    category_proportions = table.sum(axis=0) / cnt_total

    group_sizes = table.sum(axis=1)

    chisq_stat = 0
    for i in range(cnt_groups):
        for j in range(2):
            #if category_proportions[j] == 0:
            #    continue
            expected = group_sizes[i] * category_proportions[j]
            observed = table[i][j]
            chisq_stat += ((observed - expected) ** 2) / expected

    df = (cnt_groups - 1) * (2 - 1)

    pval = 1 - stats.chi2.cdf(chisq_stat, df)

    return pval


    


data = [
[38.7, 39.2, 40.1, 38.9],
[41.9, 42.3, 41.3],
[40.8, 41.2, 39.5, 38.9, 40.3],
]

# data = [
# [5, 9, 6, 8],
# [11, 13, 10, 12],
# [10, 6, 9, 9],
# ]


# data = [
#   [0,1,1,0],
#   [1,1,1,0],
#   [1,1,1,1,1,0,0,0]  
# ]

# print(chisq_hom(data))

anova_p, var_est, n, k = anova(data)


print(ttest(
     np.array(data[1]),
     np.array(data[0]),
     var_est,
     n,
     k
     ))

# p1=0.43
# p2=0.4
# n=1000
# pval,(l,r) = bstest(np.random.binomial(1,p1,n),
#                     np.random.binomial(1,p2,n))
# print(pval)
# print(l,r)