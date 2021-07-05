import os
import math
import numpy as np
import scipy.stats as st

version = '2.0'

vregSize = 128

types = {
  'i4': (4, (4, 8)),
  'i8': (8, (4, 4)),
  'i16': (16, (4, 2)),
  'half':(16, (4, 2)),
  'float': (32, (4, 1)),
#  'double': (64, (4, 1))
}

orderedTypes = [
  # 'i4',
  'i8',
  'i16',
  'half',
  'float'
]

layouts = [(1, 1), (2, 1), (1, 2), (2, 2), (4, 1), (1, 4), (4, 2), (2, 4), (8, 1), (1, 8)]
layouts = sorted(layouts, key=lambda x: x[0] * x[1] + max(x[0], x[1]) + x[1])

def getFileStats(logFile, confidence=0.95):
  '''
  Takes a path to a run log file.
  Returns a tuple of (mean, 95% CI lower bound, 95% CI upper bound).
  '''
  if not os.path.exists(logFile):
    print(f'The file "{logFile}" does not exist.')
    print('Returning zeroes.')
    return (0, (0, 0))

  # Get times.
  times = []
  with open(logFile, 'r') as f:
    for line in f:
      times.append(int(line.strip()))

  # Calculate mean and ci.
  mean = np.mean(times)
  lower, upper = st.t.interval(confidence, len(times) - 1, loc=mean, scale=st.sem(times))
  return (mean, mean - lower, upper - mean)

def plotGroupedData(ax, groupLabels, barLabels, bars, errs):
  '''
  Plots grouped data using pyplot.
  Takes a pyplot-axis-like object, labels, and data and plots it.

  groupLabels: labels for the groups -- i.e. on the x axis.
  barLabels: labels for the bars -- i.e. in the legend.
  bars: data points, bar heights. A list of lists of data points for each bar
        type.
  errs: error bounds. A list of lists of endpoints for each bar type
  '''
  # Sanity check.
  assert len(bars) > 0, "No groups to plot."
  assert len(bars) == len(errs), \
    "Different number of bar groups and error groups."
  assert len(bars) == len(barLabels), \
    "Different number of bars and bar labels."
  for bar in bars:
    assert len(bar) > 0, "No data for bar."
    for err in errs:
      assert len(bar) == len(err[0]), \
        "Different number of bars and errors within group."
    assert len(groupLabels) == len(bar), \
      "Different number of bar groups and bar labels."

  # Get spacing.
  groupBarCount = len(bars)
  groupsCount = len(bars[0])
  barWidth = 1
  grpWidth = barWidth * groupBarCount
  btwnGrpWidth = (barWidth * groupBarCount) / 2.5
  secWidth = btwnGrpWidth + grpWidth

  # Get axis data.
  axisData = zip(bars, errs)
  for i, (barData, barErrs) in enumerate(axisData):
    barPos = [i * barWidth + j * secWidth for j in range(len(barData))]
    ax.bar(barPos, barData, width=barWidth, label=barLabels[i], yerr=barErrs,
      capsize=.75)

  # Setup x axis.
  # ax.tick_params(labelsize=7, pad=0)
  ax.set_xticks([secWidth * i + grpWidth / 2 - barWidth / 2 for i in range(len(groupLabels))])
  ax.set_xticklabels(groupLabels)
  ax.set_xlim(left=-barWidth/2, right=groupsCount * secWidth - barWidth)

  # Setup y axis.
  maximum = max(max(barData) for barData in bars) * 1.1
  yInterval = round(maximum / 4, -(math.floor(math.log10(maximum)) - 1))
  ax.set_ylim(0, maximum)
  ax.set_yticks(np.arange(0, maximum, yInterval))

  # Setup legend.
  # ax.legend(frameon=False)
