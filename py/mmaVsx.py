from matplotlib import pyplot as plt

import thesUtils as tu

# Log file name format.
mmaLogNameFormat = '{type}.8x32x16.vdhd.CRR.O3.bench.{c}.json'
vecLogNameFormat = '{type}.8x32x16.vdhd.CCC.O3.vector.bench.{c}.json'
vec2LogNameFormat = '{type}.8x32x16.vdhd.RRR.O3.vector.bench.{c}.json'

def generatePlot():
  # Get data.
  data = {}
  for type in tu.orderedTypes:
    # Read logs for data.
    mmaLog = mmaLogNameFormat.format(type=type, c='{}')
    vecLog = vecLogNameFormat.format(type=type, c='{}')
    vec2Log = vec2LogNameFormat.format(type=type, c='{}')

    # Save vec and mma data.
    _, _, mmaCycleStats = tu.getJsonCumulativeStats('logs/all/' + mmaLog, 25)
    _, _, vecCycleStats = tu.getJsonCumulativeStats('logs/all/' + vecLog, 25)
    _, _, vec2CycleStats = tu.getJsonCumulativeStats('logs/all/' + vec2Log, 25)

    # Save type data.
    data[type] = (mmaCycleStats, vecCycleStats, vec2CycleStats)

  # Set up figure and axes.
  fig = plt.figure()
  figWidth = 1
  figHeight = 1

  groupNames = tu.orderedTypes
  barNames = ['MMA', 'VSX, Columns', 'VSX, Rows']

  bars = [
    [data[type][0][0] for type in groupNames],
    [data[type][1][0] for type in groupNames],
    [data[type][2][0] for type in groupNames]
  ]

  # Get error bounds.
  errs = [
    [
      [data[type][0][1] for type in groupNames],
      [data[type][0][2] for type in groupNames]
    ],
    [
      [data[type][1][1] for type in groupNames],
      [data[type][1][2] for type in groupNames]
    ],
    [
      [data[type][2][1] for type in groupNames],
      [data[type][2][2] for type in groupNames]
    ]
  ]

  # Get axis and start plotting.
  ax = fig.add_subplot(figHeight, figWidth, 1)
  tu.plotGroupedData(ax, groupNames, barNames, bars, errs)
  # ax.set_title(plot)
  ax.set_xlabel('Data Type', fontsize=8)
  ax.set_ylabel('Cycles')
  ax.legend(loc='upper right', fontsize='small')

  fig.suptitle('MMA vs Vectorisation for Different Types')
  # fig.legend(['MMA', 'Vector'], loc='lower right')
  # fig.legend(['MMA', 'Vector'])
  fig.set_size_inches(tu.textWidth, 3)
  fig.tight_layout()
  fig.savefig('mmaVsx.png')
  fig.savefig('mmaVsx.pgf')

def generateTable():
  # Get data.
  rows = []
  for type in tu.orderedTypes:
    # Read logs for data.
    mmaLog = mmaLogNameFormat.format(type=type, c='{}')
    vecLog = vecLogNameFormat.format(type=type, c='{}')
    vec2Log = vec2LogNameFormat.format(type=type, c='{}')

    # Save vec and mma data.
    mmaIterStats, mmaTimeStats, mmaCycleStats = \
      tu.getJsonCumulativeStats('logs/all/' + mmaLog, 25)
    vecIterStats, vecTimeStats, vecCycleStats = \
      tu.getJsonCumulativeStats('logs/all/' + vecLog, 25)
    vec2IterStats, vec2TimeStats, vec2CycleStats = \
      tu.getJsonCumulativeStats('logs/all/' + vec2Log, 25)

    # Add row with name and data.
    rows.append(
      (f'\code{{{type}}}, MMA',
      (*mmaIterStats[:2], *mmaTimeStats[:2], *mmaCycleStats[:2]))
    )
    rows.append(
      (f'\code{{{type}}}, VSX, Columns',
      (*vecIterStats[:2], *vecTimeStats[:2], *vecCycleStats[:2]))
    )
    rows.append(
      (f'\code{{{type}}}, VSX, Rows',
      (*vec2IterStats[:2], *vec2TimeStats[:2], *vec2CycleStats[:2]))
    )

  print(tu.tableData(rows))

if __name__ == '__main__':
  generatePlot()
  generateTable()
