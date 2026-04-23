# encoding:utf8
"""
Runs utilities version beta
"""

import numpy as np
from math import sqrt
from scipy.stats import norm

def runs(seq, retlist=False, counts=False):
    """
    Returns for each symbol the number of runs of each length
    """
    len_seq = len(seq)
    runs = [[] for i in range(seq.alen)]
    ct_seq = 0
    ct_run = 1
    symb = seq[0]
    for testsymb in seq[1:]:
        if testsymb == symb:
            ct_run += 1
        else:
            runs[symb].append(ct_run)
            symb = testsymb
            ct_run = 1
    runs[symb].append(ct_run)

    if retlist:
        return runs
    else:
        retval = [[] for i in range(seq.alen)]
        for no_symb, runlist in enumerate(runs):
            try:
                max_run = max(runlist)
            except ValueError:
                max_run = 0
            if max_run == 0:
                retval[no_symb].append(0)
            else:
                for lrun in range(max_run+1):
                    retval[no_symb].append(runlist.count(lrun))
        if counts:
            return retval
        else:
            freqs = []
            for val in retval:
                freqs.append(np.array(val).astype(float) / np.sum(np.array(val)))
            return freqs

""" R function runs.test from tseries library
function (x, alternative = c("two.sided", "less", "greater")) 
{
    if (!is.factor(x)) 
        stop("x is not a factor")
    if (any(is.na(x))) 
        stop("NAs in x")
    if (length(levels(x)) != 2) 
        stop("x does not contain dichotomous data")
    alternative <- match.arg(alternative)
    DNAME <- deparse(substitute(x))
    n <- length(x)
    R <- 1 + sum(as.numeric(x[-1] != x[-n]))
    n1 <- sum(levels(x)[1] == x)
    n2 <- sum(levels(x)[2] == x)
    m <- 1 + 2 * n1 * n2/(n1 + n2)
s <- sqrt(2 * n1 * n2 * (2 * n1 * n2 - n1 - n2)/((n1 + n2)^2 * (n1 + n2 - 1)))
STATISTIC <- (R - m)/s
METHOD <- "Runs Test"
if (alternative == "two.sided") 
PVAL <- 2 * pnorm(-abs(STATISTIC))
else if (alternative == "less") 
PVAL <- pnorm(STATISTIC)
else if (alternative == "greater") 
PVAL <- pnorm(STATISTIC, lower.tail = FALSE)
else
stop("irregular alternative")
names(STATISTIC) <- "Standard Normal" 
structure(list(statistic = STATISTIC, alternative = alternative, p.value = PVAL, method = METHOD, data.name = DNAME), class = "htest") 
}
"""

def runs_test(seq, alternative="two-sided"):
    if seq.alen != 2:
        raise ValueError("Only works with binary sequences yet")
    n = float(len(seq))
    R = float(1 + sum(seq[1:] != seq[:-1]))
    # we know that it is a binary sequence
    n1 = float(sum(seq == 0))
    n2 = float(sum(seq == 1))
    m = 1 + 2 * n1 * n2 / (n1 + n2)
    s = sqrt(2 * n1 * n2 * (2 * n1 * n2 - n1 - n2)/((n1 + n2)**2 * (n1 + n2 - 1)))
    statistics = (R - m) / s

    if alternative == 'two-sided':
        p_value = 2 * norm.cdf(-abs(statistics))
    elif alternative == 'less':
        p_value = norm.cdf(statistics)
    elif alternative == "greater":
        p_value = 1 - norm.cdf(statistics)
    else:
        raise ValueError('Irregular alternative')

    return statistics, p_value


if __name__ == '__main__':

    import scikits.symbolic.sequence as S

    seq = S.Sequence([0,1,1,1,0,0], 2)
    print runs(seq, retlist=True)
    seq = S.Sequence([0,1,1,1,0,0,0,1,1,1,1,0,0,1,0,1], 2)
    print runs(seq, retlist=True)
    seq = S.Sequence([0,1,1,1,0,0], 2)
    print runs(seq)
    seq = S.Sequence([0,1,1,1,0,0,0,1,1,1,1,0,0,1,0,1], 2)
    print runs(seq)
