import json
import math
import numpy as np
import os
import scipy.stats as st
from scipy.stats.mstats import gmean

version = '2.5.2'

# Text width in inches.
textWidth = 5.50107

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
  # 'double',
  'float',
  'i16',
  'half',
  # 'bfloat',
  'i8',
  # 'i4'
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
    return (0, 0, 0)

  # Get times.
  times = []
  with open(logFile, 'r') as f:
    for line in f:
      times.append(int(line.strip()))

  # Calculate mean and ci.
  mean = np.mean(times)
  lower, upper = st.t.interval(confidence, len(times) - 1, loc=mean, scale=st.sem(times))
  return (mean, mean - lower, upper - mean)

def getJsonStats(logFile):
  '''
  Takes a path to a json log file.
  Returns a tuple of (iterations, cpu time, cycles).
  '''
  if not os.path.exists(logFile):
    print(f'The file "{logFile}" does not exist.')
    print('Returning zeroes.')
    return (0, 0, 0)

  with open(logFile, 'r') as f:
    objects = json.load(f)

  benchmarks = objects['benchmarks']
  assert len(benchmarks) == 1, 'Too many benchmark entries'
  benchmark = benchmarks[0]

  iterations = benchmark['iterations']
  cycles = benchmark['CYCLES']
  cpu_time = benchmark['cpu_time']

  return (iterations, cpu_time, cycles)

def getJsonDiffStats(logFile, firstBenchName, secondBenchName):
  '''
  Takes a path to a json log file and the name of two benchmarks for which the
  difference in statistics should be returned
  Returns a tuple of (iterations diff, cpu time diff, cycles diff).
  '''
  assert firstBenchName != secondBenchName, \
    'Benchmark diff names cannot be the same'

  if not os.path.exists(logFile):
    print(f'The file "{logFile}" does not exist.')
    print('Returning zeroes.')
    return (0, 0, 0)

  with open(logFile, 'r') as f:
    objects = json.load(f)

  benchmarks = objects['benchmarks']
  assert len(benchmarks) == 2, 'Too many benchmark entries'

  firstBench = None
  secondBench = None

  # Check first benchmark.
  if benchmarks[0]['name'] == firstBenchName:
    firstBench = benchmarks[0]
  elif benchmarks[0]['name'] == secondBenchName:
    secondBench = benchmarks[0]

  # Check second benchmark.
  if benchmarks[1]['name'] == firstBenchName:
    firstBench = benchmarks[1]
  elif benchmarks[1]['name'] == secondBenchName:
    secondBench = benchmarks[1]

  # Verify benchmarks were found.
  assert firstBench is not None, 'First benchmark not found'
  assert secondBench is not None, 'Second benchmark not found'


  iterations = firstBench['iterations']
  cycles = firstBench['CYCLES'] - secondBench['CYCLES']
  cpu_time = firstBench['cpu_time'] - secondBench['cpu_time']

  return (iterations, cpu_time, cycles)

def getJsonCumulativeStats(fmtLogPath, count, confidence=0.95):
  '''
  Takes a log path with containing a single formattable field for count.
  '''
  # Holding place for data.
  iterList = []
  timeList = []
  cycleList = []

  # Gather data.
  for i in range(count):
    logPath = fmtLogPath.format(i)
    iterations, cpuTime, cycles = getJsonStats(logPath)
    iterList.append(iterations)
    timeList.append(cpuTime)
    cycleList.append(cycles)

  mean = lambda l: sum(l) / len(l)
  def ci(l):
    m = mean(l)
    lower, upper = st.t.interval(confidence, len(l) - 1, loc=m, scale=st.sem(l))
    return (m - lower, upper - m)

  iterResults = (mean(iterList), *ci(iterList))
  timeResults = (mean(timeList), *ci(timeList))
  cycleResults = (mean(cycleList), *ci(cycleList))

  return (iterResults, timeResults, cycleResults)

def getJsonCumDiffStats(fmtLogPath, count, firstBench, secondBench, confidence=0.95):
  '''
  Takes a log path with containing a single formattable field for count.

  Differs from getJsonCumulativeStats only in that it calls getJsonDiffStats
  instead of getJsonStats. Probably a better way to factor this.
  '''
  # Holding place for data.
  iterList = []
  timeList = []
  cycleList = []

  # Gather data.
  for i in range(count):
    logPath = fmtLogPath.format(i)
    iterations, cpuTime, cycles = getJsonDiffStats(logPath, firstBench, secondBench)
    iterList.append(iterations)
    timeList.append(cpuTime)
    cycleList.append(cycles)

  mean = lambda l: sum(l) / len(l)
  def ci(l):
    m = mean(l)
    lower, upper = st.t.interval(confidence, len(l) - 1, loc=m, scale=st.sem(l))
    return (m - lower, upper - m)

  iterResults = (mean(iterList), *ci(iterList))
  timeResults = (mean(timeList), *ci(timeList))
  cycleResults = (mean(cycleList), *ci(cycleList))

  return (iterResults, timeResults, cycleResults)

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
  assert len(bars) > 0, 'No groups to plot.'
  assert len(bars) == len(errs), \
    'Different number of bar groups and error groups.'
  assert len(bars) == len(barLabels), \
    'Different number of bars and bar labels.'
  for bar in bars:
    assert len(bar) > 0, 'No data for bar.'
    for err in errs:
      assert len(bar) == len(err[0]), \
        'Different number of bars and errors within group.'
    assert len(groupLabels) == len(bar), \
      'Different number of bar groups and bar labels.'

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

def tableData(rows):
  '''
  Takes a 2-tuple of (name, data) where data is a 6-tuple of (mean iterations,
  95% CI difference, mean cpu time, 95% CI difference, mean cycles, 95% CI
  difference).

  Returns a fully formed tabular environment with four columns:
  --------------------------------
  | Name | n | CPU Time | Cycles |
  --------------------------------

  where n, CPU Time, and Cycles are formated as "mean +- 95%CI".
  '''
  header = \
    '\\makebox[\\textwidth][c]{\n' \
    '  \\begin{tabular}{| c | c | c | c |}\n' \
    '    \hline\n' \
    '    Name & $n$ & CPU Time (\\SI{}{\\textit{\\nano\\second}}) & Cycles\\\\\\hline\n'
  footer = \
    '  \\end{tabular}\n}'

  table = header

  for name, (iters, itersCI, cpuTime, cpuCI, cycles, cyclesCI) in rows:
    table += \
      f'    {name} & ${iters / 1e6:0.1f} \pm {itersCI / 1e6:0.2f}$ & ' \
      f'${cpuTime:0.2f} \pm {cpuCI:0.2f}$ & ${cycles:0.2f} \pm ' \
      f'{cyclesCI:0.2f}$ \\\\\\hline\n'

  table += footer

  return table
