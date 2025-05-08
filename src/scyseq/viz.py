import math
import numpy as np
import itertools
from random import uniform
import matplotlib.pyplot as plt
import matplotlib

from . import sequence as S

# file:///usr/share/doc/python-matplotlib-doc/html/examples/pylab_examples/ellipse_demo.html

def plot(seq, xlabel='Time', ylabel='States', title='Simple plot', labelsize=15,
        titlesize=25, color='blue', **kwargs):
    """
    Simple (discrete / symbolic) time series plot
    """

    alphabet = seq.alphabet
    yvals = seq.ivals
    xvals = list(range(len(seq)))

    fig, ax = plt.subplots()
    ax.plot(xvals, yvals, color=color)

    ax.set_yticks(range(len(alphabet)))
    ax.set_yticks([i-0.5 for i in range(len(alphabet)+1)], minor=True)
    ax.set_yticklabels(alphabet.strvals, rotation=90)

    ax.set_xlabel(xlabel, fontsize=labelsize)
    ax.set_ylabel(ylabel, fontsize=labelsize)
    ax.set_title(title, fontsize=titlesize)

    ax.set_xlim(0, max(xvals))
    ax.set_ylim(-0.5, len(alphabet)-0.5)

    ax.grid(True, which='minor', axis='y')

def plot_bar(seq, xlabel='Time', ylabel='States', title='Bar plot', labelsize=15,
        titlesize=25, cmap=matplotlib.cm.jet, **kwargs):
    """
    Plots bar code like graph.
    """

    alphabet = seq.alphabet
    xvals = list(range(len(seq)))
    svals = []
    for i in range(len(alphabet)):
        svals.append([])

    for s in seq.ivals:
        for i in range(len(alphabet)):
            if i == s:
                svals[i].append(i)
            else:
                svals[i].append(-1)

    fig, ax = plt.subplots()
    ax.matshow(np.ma.masked_values(svals, -1), aspect='auto', cmap=cmap)

    ax.set_yticks(range(len(alphabet)))
    ax.set_yticks([i-0.5 for i in range(len(alphabet)+1)], minor=True)
    ax.set_yticklabels(alphabet.strvals, rotation=90)

    ax.set_xlabel(xlabel, fontsize=labelsize)
    ax.set_ylabel(ylabel, fontsize=labelsize)
    ax.set_title(title, fontsize=titlesize)

    ax.set_xlim(0, max(xvals))
    ax.set_ylim(-0.5, len(alphabet)-0.5)

def plot_color(seq, aspect=5, title='Sequence', xlabel='Time', labelsize=15,
        titlesize=25, **kwargs):
    """
    Plots as ???
    """

    ar = np.reshape(seq.ivals, (len(seq), 1))

    fig, ax = plt.subplots()
    ax.imshow(ar.T, aspect=aspect)
    ax.set_xlabel(xlabel, fontsize=labelsize)
    ax.set_title(title, fontsize=titlesize)



def plot_grid(seq1, seq2, xlabel='1st sequence', ylabel='2nd Sequence',
              title='Grid plot', labelsize=15, titlesize=25, color='blue',
              alpha=0.3, scale=100, jitter=0.4, **kwargs):
    """
    Plots state-space grids plots inspired from

    Hollenstein T. (2013) State space grids. Springer.
    """

    alphabet1 = seq1.alphabet
    alphabet2 = seq2.alphabet
    
    size = []
    visited = []
    xyvals = []
    previous = None

    for current in zip(seq1.ivals, seq2.ivals):

        if current not in visited:
            visited.append(current)
            xyvals.append(current)
            size.append(1)
            previous = current
        elif current in visited:
            if current == previous:
                size[-1] += 1
            else:
                x, y = current
                dx = uniform(-jitter, jitter)
                dy = uniform(-jitter, jitter)
                xyvals.append((x+dx, y+dy))
                size.append(1)
                previous = current

    xvals = [xy[0] for xy in xyvals]  
    yvals = [xy[1] for xy in xyvals]  
    size = [s*scale for s in size]

    fig, ax = plt.subplots()
    ax.scatter(xvals, yvals, c=color, s=size, alpha=alpha)
    ax.plot(xvals, yvals)

    ax.set_xticks(range(len(alphabet1)))
    ax.set_xticks([i-0.5 for i in range(len(alphabet1)+1)], minor=True)
    ax.set_xticklabels(alphabet1.strvals)

    ax.set_yticks(range(len(alphabet2)))
    ax.set_yticks([i-0.5 for i in range(len(alphabet2)+1)], minor=True)
    ax.set_yticklabels(alphabet2.strvals, rotation=90)

    ax.set_xlabel(xlabel, fontsize=labelsize)
    ax.set_ylabel(ylabel, fontsize=labelsize)
    ax.set_title(title, fontsize=titlesize)

    ax.set_xlim(-0.5, len(alphabet1)-0.5)
    ax.set_ylim(-0.5, len(alphabet2)-0.5)

    ax.grid(True, which='minor')

def plot_independence(seq1, seq2, xlabel='1st sequence', ylabel='2nd Sequence',
              title='Independence plot', labelsize=15, titlesize=25,
              color=('blue', 'red'),
              alpha=0.3, scale=100, **kwargs):
    """
    Plots state-space grids representing the elements of the mutual information
    between sequences.
    """

    alphabet1 = seq1.alphabet
    alphabet2 = seq2.alphabet

    fq1 = seq1.frequency()
    fq2 = seq2.frequency()
    
    seq3 = S.recode([seq1, seq2], new_alphabet=False)
    # visited = S.visited_states(seq3, sort=False)
    fq3 = seq3.frequency()

    xvals = []
    yvals = []
    size = []

    bialphabet = list(itertools.product(alphabet1, alphabet2))
    print(bialphabet)

    for n, xy in enumerate(bialphabet):
        x = xy[0].ival
        y = xy[1].ival
        xvals.append(x)
        yvals.append(y)
        size.append(fq3[n] * math.log(fq3[n] / (fq1[x] * fq2[y])))

    sizes = [abs(s)*scale for s in size]
    colors = []

    for s in size:
        if s <0 :
            colors.append(color[0])
        else:
            colors.append(color[1])

    fig, ax = plt.subplots()
    ax.scatter(xvals, yvals, c=colors, s=sizes, alpha=alpha)
    # ax.plot(xvals, yvals)

    ax.set_xticks(range(len(alphabet1)))
    ax.set_xticks([i-0.5 for i in range(len(alphabet1)+1)], minor=True)
    ax.set_xticklabels(alphabet1.strvals)

    ax.set_yticks(range(len(alphabet2)))
    ax.set_yticks([i-0.5 for i in range(len(alphabet2)+1)], minor=True)
    ax.set_yticklabels(alphabet2.strvals, rotation=90)

    ax.set_xlabel(xlabel, fontsize=labelsize)
    ax.set_ylabel(ylabel, fontsize=labelsize)
    ax.set_title(title, fontsize=titlesize)

    ax.set_xlim(-0.5, len(alphabet1)-0.5)
    ax.set_ylim(-0.5, len(alphabet2)-0.5)

    ax.grid(True, which='minor')


