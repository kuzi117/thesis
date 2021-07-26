from matplotlib import pyplot as plt

import thesUtils as tu

# logNameFormat = '{type}.{m}x{d}x{n}.vdhd.CRR.O3.timed{opt}.txt'
logNameFormat = '{type}.{m}x{d}x{n}.vdhd.CRR.O3.bench{opt}.{c}.json'

opts = [
  ('', 'No Opt'),
  ('.sink', 'Sink'),
  ('.merge', 'Merge'),
  ('.sink.merge', 'Sink & Merge'),
]

layouts = [
  ((8, 8, 16), '8x8x16'),
  ((32, 8, 32), '32x8x32')
]

if __name__ == '__main__':
  # Get data.
  data = {}
  for type in tu.orderedTypes:
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
        print(log, cycleStats)
        layoutData[layoutName] = cycleStats

      # Save layout data.
      optData[optName] = layoutData

    # Save type data.
    data[type] = optData

  # Set up figure and axes.
  fig = plt.figure()
  figWidth = 2
  figHeight = 2

  # Start plotting.
  groupLabels = [layout[1] for layout in layouts]
  barLabels = [opt[1] for opt in opts]
  for i, type in enumerate(tu.orderedTypes):
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
    ax.set_title(type.capitalize())

    ax.set_xlabel('Layout')
    ax.set_ylabel('Cycles')

  # Save figure.
  fig.legend(barLabels, ncol=1, loc='center', fontsize='small')
  fig.suptitle('Runtime for Additional Optimisations per Type ')
  fig.tight_layout()
  fig.savefig('sinkMerge.png')
