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

logNameFormat = '{type}.{m}x{d}x{n}.vdhd.CRR.O3.timed{opt}.txt'

opts = [
  ('', 'No Load Sinking'),
  ('.sink', 'Load Sinking')
]

layouts = [
  ((8, 8, 16), '8x8x16'),
  ((32, 8, 32), '32x8x32')
]

if __name__ == '__main__':
  # Get data.
  data = {}
  for type in ['float']:
    # Holding place optimisation data.
    optData = {}

    # Get the data for each ACC layout.
    for optStr, optName in opts:
      layoutData = {}

      for (m, d, n), layoutName in layouts:
        # Read logs for data.
        log = logNameFormat.format(type=type, opt=optStr, m=m, d=d, n=n)

        # Save layout data.
        layoutData[layoutName] = tu.getFileStats('logs/sinkMerge/' + log)

      # Save layout data.
      optData[optName] = layoutData

    # Save type data.
    data[type] = optData

  print(data)

  # Set up figure and axes.
  fig = plt.figure()
  figWidth = 1
  figHeight = 1

  # Start plotting.
  groupLabels = [layout[1] for layout in layouts]
  barLabels = [opt[1] for opt in opts]
  for i, type in enumerate(['float']):
    # Get opt data for this type.
    optData = data[type]

    # Set up bar data points.
    bars = []
    for _, optName in opts:
      bar = [optData[optName][layoutName][0] for layoutName in groupLabels]
      bars.append(bar)
    print(bars)


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
    ax.set_title('Effect of Load Sinking on Float Matrices')

    ax.set_xlabel('Kernel Size')
    ax.set_ylabel('Runtime\n(\\textit{ns})')
    ax.legend(ncol=1, loc='upper left')

  # Save figure.
  # fig.legend(barLabels, ncol=1, loc='center', fontsize='small')
  # fig.suptitle('Runtime for Additional Optimisations per Type ')
  fig.set_size_inches(tu.textWidth, 3)
  fig.tight_layout()
  fig.savefig('sinkFloats.pgf')
