import itertools
import math
from random import uniform

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

import scyseq as sq

# Default colormap for consistent state coloring across all plots
DEFAULT_COLORMAP = "viridis"


def get_state_colors(alphabet, cmap_name=DEFAULT_COLORMAP):
    """
    Get consistent color scheme for alphabet states.
    Returns a colormap and normalization that ensures each state gets the same color across plots.

    :param alphabet: A symbolic Alphabet object
    :param cmap_name: Name of matplotlib colormap (default: 'viridis')
    :returns: Tuple of (cmap, norm) for consistent coloring
    """
    cmap = matplotlib.cm.get_cmap(cmap_name, len(alphabet))
    norm = matplotlib.colors.BoundaryNorm(np.arange(len(alphabet) + 1) - 0.5, cmap.N)
    return cmap, norm


def plot(
    seq,
    xlabel="Time",
    ylabel="States",
    title="Simple plot",
    labelsize=15,
    titlesize=25,
    color="blue",
    **kwargs,
):
    """
    Simple (discrete / symbolic) time series plot
    """

    alphabet = seq.alphabet
    yvals = seq.ivals
    xvals = list(range(len(seq)))

    fig, ax = plt.subplots()
    ax.scatter(xvals, yvals, c=color, **kwargs)

    ax.set_yticks(range(len(alphabet)))
    ax.set_yticks([i - 0.5 for i in range(len(alphabet) + 1)], minor=True)
    ax.set_yticklabels(alphabet.svals, rotation=90)

    ax.set_xlabel(xlabel, fontsize=labelsize)
    ax.set_ylabel(ylabel, fontsize=labelsize)
    ax.set_title(title, fontsize=titlesize)

    ax.set_xlim(0, max(xvals))
    ax.set_ylim(-0.5, len(alphabet) - 0.5)

    ax.grid(True, which="minor", axis="y")


def plot_bar(
    seq,
    xlabel="Time",
    ylabel="States",
    title="Bar plot",
    labelsize=15,
    titlesize=25,
    cmap_name=DEFAULT_COLORMAP,
    legend=False,
    legend_title="States",
    **kwargs,
):
    """
    Plots bar code like graph with consistent state colors.
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

    # Get consistent color scheme
    cmap, norm = get_state_colors(alphabet, cmap_name)

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.imshow(
        np.ma.masked_values(svals, -1),
        aspect="auto",
        cmap=cmap,
        norm=norm,
        interpolation="nearest",
    )

    ax.set_yticks(range(len(alphabet)))
    ax.set_yticks([i - 0.5 for i in range(len(alphabet) + 1)], minor=True)
    ax.set_yticklabels(alphabet.svals, rotation=90)

    ax.set_xlabel(xlabel, fontsize=labelsize)
    ax.set_ylabel(ylabel, fontsize=labelsize)
    ax.set_title(title, fontsize=titlesize)

    ax.set_xlim(0, max(xvals))
    ax.set_ylim(-0.5, len(alphabet) - 0.5)

    # Add legend for state colors
    if legend:
        handles = [
            Patch(facecolor=cmap(norm(idx)), edgecolor="none", label=label)
            for idx, label in enumerate(alphabet.svals)
        ]
        ax.legend(
            handles=handles,
            title=legend_title,
            loc="upper center",
            bbox_to_anchor=(0.5, -0.15),
            ncol=min(len(handles), 6),
            frameon=False,
            fontsize=max(labelsize - 4, 8),
            title_fontsize=max(labelsize - 3, 9),
        )

    return fig, ax


def plot_color(
    seq,
    aspect="auto",
    title="Sequence",
    xlabel="Time",
    labelsize=15,
    titlesize=25,
    cmap_name=DEFAULT_COLORMAP,
    figsize=(10, 2.4),
    legend=True,
    legend_title="States",
    **kwargs,
):
    """
    Plots a sequence as a color strip with consistent state colors.
    """

    alphabet = seq.alphabet
    ar = np.reshape(seq.ivals, (1, len(seq)))

    # Get consistent color scheme
    cmap, norm = get_state_colors(alphabet, cmap_name)

    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0.08, 0.45, 0.84, 0.14])  # thinner strip axis

    ax.imshow(
        ar, aspect=aspect, cmap=cmap, norm=norm, interpolation="nearest", **kwargs
    )

    ax.set_yticks([])
    ax.set_xlabel(xlabel, fontsize=labelsize)
    ax.set_title(title, fontsize=titlesize)

    if legend:
        handles = [
            Patch(facecolor=cmap(norm(idx)), edgecolor="none", label=label)
            for idx, label in enumerate(alphabet.svals)
        ]
        ax.legend(
            handles=handles,
            title=legend_title,
            loc="upper center",
            bbox_to_anchor=(0.5, -1.5),
            ncol=len(handles),
            frameon=False,
            fontsize=max(labelsize - 4, 8),
            title_fontsize=max(labelsize - 3, 9),
        )

    return fig, ax


def plot_grid(
    seq1,
    seq2,
    xlabel="1st sequence",
    ylabel="2nd Sequence",
    title="Grid plot",
    labelsize=15,
    titlesize=25,
    color="blue",
    alpha=0.3,
    scale=100,
    jitter=0.4,
    **kwargs,
):
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
                xyvals.append((x + dx, y + dy))
                size.append(1)
                previous = current

    xvals = [xy[0] for xy in xyvals]
    yvals = [xy[1] for xy in xyvals]
    size = [s * scale for s in size]

    fig, ax = plt.subplots()
    ax.scatter(xvals, yvals, c=color, s=size, alpha=alpha)
    ax.plot(xvals, yvals)

    ax.set_xticks(range(len(alphabet1)))
    ax.set_xticks([i - 0.5 for i in range(len(alphabet1) + 1)], minor=True)
    ax.set_xticklabels(alphabet1.svals)

    ax.set_yticks(range(len(alphabet2)))
    ax.set_yticks([i - 0.5 for i in range(len(alphabet2) + 1)], minor=True)
    ax.set_yticklabels(alphabet2.svals, rotation=90)

    ax.set_xlabel(xlabel, fontsize=labelsize)
    ax.set_ylabel(ylabel, fontsize=labelsize)
    ax.set_title(title, fontsize=titlesize)

    ax.set_xlim(-0.5, len(alphabet1) - 0.5)
    ax.set_ylim(-0.5, len(alphabet2) - 0.5)

    ax.grid(True, which="minor")

    return fig, ax


def plot_independence(
    seq1,
    seq2,
    xlabel="1st sequence",
    ylabel="2nd Sequence",
    title="Independence plot",
    labelsize=15,
    titlesize=25,
    color=("blue", "red"),
    alpha=0.3,
    scale=100,
    **kwargs,
):
    """
    Plots state-space grids representing the elements of the mutual information
    between sequences.
    """

    alphabet1 = seq1.alphabet
    alphabet2 = seq2.alphabet

    fq1 = seq1.frequency()
    fq2 = seq2.frequency()

    seq3 = sq.recode([seq1, seq2], new_alphabet=False)
    # visited = sq.visited_states(seq3, sort=False)
    fq3 = seq3.frequency()

    xvals = []
    yvals = []
    size = []

    bialphabet = list(itertools.product(alphabet1, alphabet2))

    for n, xy in enumerate(bialphabet):
        x = xy[0].ival
        y = xy[1].ival
        xvals.append(x)
        yvals.append(y)
        if fq3[n] == 0:
            size.append(0)
        else:
            size.append(fq3[n] * math.log(fq3[n] / (fq1[x] * fq2[y])))

    sizes = [abs(s) * scale for s in size]
    colors = []

    for s in size:
        if s < 0:
            colors.append(color[0])
        else:
            colors.append(color[1])

    fig, ax = plt.subplots()
    ax.scatter(xvals, yvals, c=colors, s=sizes, alpha=alpha)
    # ax.plot(xvals, yvals)

    ax.set_xticks(range(len(alphabet1)))
    ax.set_xticks([i - 0.5 for i in range(len(alphabet1) + 1)], minor=True)
    ax.set_xticklabels(alphabet1.svals)

    ax.set_yticks(range(len(alphabet2)))
    ax.set_yticks([i - 0.5 for i in range(len(alphabet2) + 1)], minor=True)
    ax.set_yticklabels(alphabet2.svals, rotation=90)

    ax.set_xlabel(xlabel, fontsize=labelsize)
    ax.set_ylabel(ylabel, fontsize=labelsize)
    ax.set_title(title, fontsize=titlesize)

    ax.set_xlim(-0.5, len(alphabet1) - 0.5)
    ax.set_ylim(-0.5, len(alphabet2) - 0.5)

    ax.grid(True, which="minor")
