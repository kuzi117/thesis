from matplotlib import pyplot as plt

import thesUtils as tu

# Log file name format.
handLogNameFormat = 'float.8x32x16.vdhd.CRR.hand.{c}.json'
regLogNameFormat = 'float.8x32x16.vdhd.CRR.O3.bench.{c}.json'
sinkLogNameFormat = 'float.8x32x16.vdhd.CRR.O3.bench.sink.{c}.json'

def generatePlot():
  # Get log names.
  handLog = handLogNameFormat.format(type=type, c='{}')
  regLog = regLogNameFormat.format(type=type, c='{}')
  sinkLog = sinkLogNameFormat.format(type=type, c='{}')

  # Get
  _, _, handCycleStats = tu.getJsonCumDiffStats(
                              'logs/all/' + handLog, 25, 'handMult', 'fnCall')
  _, _, regCycleStats = tu.getJsonCumulativeStats('logs/all/' + regLog, 25)
  _, _, sinkCycleStats = tu.getJsonCumulativeStats('logs/all/' + sinkLog, 25)

  # Set up figure and axes.
  fig = plt.figure()
  figWidth = 1
  figHeight = 1

  groupNames = ['No Load Sinking', 'Load Sinking', 'Handwritten']
  barNames = ['Cycles']

  bars = [
    [regCycleStats[0], sinkCycleStats[0], handCycleStats[0]]
  ]

  # Get error bounds.
  errs = [
    [
      [regCycleStats[1], sinkCycleStats[1], handCycleStats[1]],
      [regCycleStats[2], sinkCycleStats[2], handCycleStats[2]]
    ]
  ]

  # Get axis and start plotting.
  ax = fig.add_subplot(figHeight, figWidth, 1)
  tu.plotGroupedData(ax, groupNames, barNames, bars, errs)
  # ax.set_title(plot)
  ax.set_xlabel('Kernel Type', fontsize=8)
  ax.set_ylabel('Cycles')

  ax.set_title('Cycle Counts for Intrinsic vs Handwritten Kernel')
  fig.set_size_inches(tu.textWidth * 3 / 4, 3)
  fig.tight_layout()
  fig.savefig('intrHand.png')
  fig.savefig('intrHand.pgf')

def generateTable():
  # Get data.
  rows = []
  # Read logs for data.
  handLog = handLogNameFormat.format(type=type, c='{}')
  regLog = regLogNameFormat.format(type=type, c='{}')
  sinkLog = sinkLogNameFormat.format(type=type, c='{}')

  # Save handwritten, sunk, and unsunk data.
  handIterStats, handTimeStats, handCycleStats = \
    tu.getJsonCumDiffStats('logs/all/' + handLog, 25, 'handMult', 'fnCall')
  regIterStats, regTimeStats, regCycleStats = \
    tu.getJsonCumulativeStats('logs/all/' + regLog, 25)
  sinkIterStats, sinkTimeStats, sinkCycleStats = \
    tu.getJsonCumulativeStats('logs/all/' + sinkLog, 25)

  # Add row with name and data.
  rows.append(
    ('No Load Sinking',
    (*regIterStats[:2], *regTimeStats[:2], *regCycleStats[:2]))
  )
  rows.append(
    ('Load Sinking',
    (*sinkIterStats[:2], *sinkTimeStats[:2], *sinkCycleStats[:2]))
  )
  rows.append(
    ('Handwritten',
    (*handIterStats[:2], *handTimeStats[:2], *handCycleStats[:2]))
  )

  print(tu.tableData(rows))

if __name__ == '__main__':
  generatePlot()
  generateTable()
