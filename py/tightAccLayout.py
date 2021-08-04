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

logNameFormat = '{type}.{ve}x32x{he}.v{v}h{h}.CRR.O3.bench.{c}.json'

layouts = [
  ((2, 4), '$2 \\times 4$'),
  ((4, 2), '$4 \\times 2$'),
  ((1, 8), '$1 \\times 8$'),
  ((8, 1), '$8 \\times 1$')
]
def generatePlot():
  # Get data.
  data = {}
  for type in tu.orderedTypes:
    # Holding place ACC data.
    accData = {}

    # Get the data for each ACC layout.
    for (v, h), layoutName in layouts:
      # Read logs for data.
      log = logNameFormat.format(type=type, v=v, h=h, ve=v * 4, he=h * 4, c='{}')

      # Save layout data.
      _, _, cycleStats = tu.getJsonCumulativeStats('logs/all/' + log, 25)
      accData[layoutName] = cycleStats

    # Save type data.
    data[type] = accData

  # Set up figure and axes.
  fig = plt.figure()
  figWidth = 2
  figHeight = 2

  # Start plotting.
  groupLabels = [layout[1] for layout in layouts]
  barLabels = ['cycles']
  for i, type in enumerate(tu.orderedTypes):
    # Get data for this type.
    accData = data[type]

    # Set up bar data points.
    bars = [
      [accData[layout][0] for layout in accData]
    ]

    # Set up error data for the bars.
    errs = [
      [
        [accData[layout][1] for layout in accData],
        [accData[layout][2] for layout in accData]
      ]
    ]

    # Get axis and start plotting.
    ax = fig.add_subplot(figHeight, figWidth, i + 1)
    tu.plotGroupedData(ax, groupLabels, barLabels, bars, errs)
    ax.set_title('\\texttt{{{}}}'.format(type))

    ax.set_xlabel('Accumulator Layout')
    ax.set_ylabel('Cycles')

  # Save figure.
  fig.suptitle('Cycle Counts for Different Accumulator Layouts per Type')
  fig.set_size_inches(tu.textWidth, 5)
  fig.tight_layout()
  fig.savefig('tightAccLayouts.png')
  fig.savefig('tightAccLayouts.pgf')

def generateTable():
  # Get data.
  rows = []
  for type in tu.orderedTypes:
    # Get the data for each ACC layout.
    for (v, h), layoutName in layouts:
      # Read logs for data.
      log = logNameFormat.format(type=type, v=v, h=h, ve=v * 4, he=h * 4, c='{}')

      # Save layout data.
      iterStats, timeStats, cycleStats = \
        tu.getJsonCumulativeStats('logs/all/' + log, 25)

      # Add row with name and data.
      rows.append(
        (f'\code{{{type}}}, {layoutName}',
        (*iterStats[:2], *timeStats[:2], *cycleStats[:2]))
      )

  print(tu.tableData(rows))


if __name__ == '__main__':
  generatePlot()
  generateTable()
