import matplotlib

matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

from matplotlib import pyplot as plt

import thesUtils as tu

# logNameFormat = '{type}.{m}x{d}x{n}.vdhd.CRR.O3.timed{opt}.txt'
logNameFormat = '{type}.{m}x{d}x{n}.vdhd.CRR.O3.bench{opt}.{c}.json'

opts = [
  ('', 'No Load Sinking'),
  ('.sink', 'Load Sinking')
]

layouts = [
  ((8, 8, 16), '$8 \times 8 \times 16$'),
  ((32, 8, 32), '$32 \times 8 \times 32$')
]

def generatePlot():
  # Get data.
  data = {}
  for type in ['float', 'i16']:
    # Holding place optimisation data.
    optData = {}

    # Get the data for each ACC layout.
    for optStr, optName in opts:
      layoutData = {}

      for (m, d, n), layoutName in layouts:
        # Read logs for data.
        # log = logNameFormat.format(type=type, opt=optStr, m=m, d=d, n=n)
        log = logNameFormat.format(type=type, opt=optStr, m=m, d=d, n=n, c='{}')

        # Save layout data.
        # layoutData[layoutName] = tu.getFileStats('logs/sinkMerge/' + log)
        _, _, cycleStats = tu.getJsonCumulativeStats('logs/all/' + log, 25)
        layoutData[layoutName] = cycleStats

      # Save layout data.
      optData[optName] = layoutData

    # Save type data.
    data[type] = optData

  # Set up figure and axes.
  fig = plt.figure()
  figWidth = 2
  figHeight = 1

  # Start plotting.
  groupLabels = [layout[1] for layout in layouts]
  barLabels = [opt[1] for opt in opts]
  for i, type in enumerate(['float', 'i16']):
    # Get opt data for this type.
    optData = data[type]

    # Set up bar data points.
    bars = []
    for _, optName in opts:
      bar = [optData[optName][layoutName][0] for layoutName in groupLabels]
      bars.append(bar)

    # Set up error data for the bars.
    errs = []
    for _, optName in opts:
      err = [
        [optData[optName][layoutName][1] for layoutName in groupLabels],
        [optData[optName][layoutName][2] for layoutName in groupLabels]
      ]
      errs.append(err)

    # Get axis and start plotting.
    ax = fig.add_subplot(figHeight, figWidth, i + 1)
    tu.plotGroupedData(ax, groupLabels, barLabels, bars, errs)
    ax.set_title('\\texttt{{{}}}'.format(type))
    # ax.set_title(type.capitalize())

    ax.set_xlabel('Kernel Size')
    ax.set_ylabel('Cycles')
    # ax.legend(ncol=1, loc='upper left')

  # Save figure.
  fig.legend(barLabels, ncol=1, loc='lower center', bbox_to_anchor=(.55, -.01), fontsize='small', frameon=True)
  fig.suptitle('Effect of Load Sinking on Matrices')
  fig.set_size_inches(tu.textWidth, 3)
  fig.tight_layout()
  fig.set_size_inches(tu.textWidth, 3.3)
  fig.savefig('sinkFloats.pgf')

def generateTable():
  rows = []
  for type in ['float', 'i16']:
    for (m, d, n), layoutName in layouts:
      for optStr, optName in opts:
        # Read logs for data.
        log = logNameFormat.format(type=type, opt=optStr, m=m, d=d, n=n, c='{}')
        log = 'logs/all/' + log

        # Get stats.
        iterStats, timeStats, cycleStats = tu.getJsonCumulativeStats(log, 25)

        # Add row with name and data.
        rows.append(
          (f'\code{{{type}}}, ${m} \\times {d} \\times {n}$, {optName}',
          (*iterStats[:2], *timeStats[:2], *cycleStats[:2]))
        )

  print(tu.tableData(rows))

if __name__ == '__main__':
  generatePlot()
  generateTable()
