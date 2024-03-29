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

logNameFormat = '{type}.64x32x64.v{v}h{h}.CRR.O3.bench.{c}.json'

layouts = [
  ((2, 4), '2x4'),
  ((1, 8), '1x8'),
  ((4, 2), '4x2'),
  ((8, 1), '8x1'),
]

if __name__ == '__main__':
  # Get data.
  data = {}
  for type in tu.orderedTypes:
    # Holding place ACC data.
    accData = {}

    # Get the data for each ACC layout.
    for (v, h), layoutName in layouts:
      # Read logs for data.
      log = logNameFormat.format(type=type, v=v, h=h, c='{}')

      # Read logs for data.
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
  barLabels = ['runtime']
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
    ax.set_title(f'\\texttt{{{type}}}')

    ax.set_xlabel('Accumulator Layout')
    ax.set_ylabel('Cycles')

  # Save figure.
  fig.suptitle('Runtime for Different ACC Layouts per Type ')
  fig.set_size_inches(tu.textWidth, 5.5)
  fig.tight_layout()
  fig.savefig('accLayouts.png')
  fig.savefig('accLayouts.pgf')
