from matplotlib import pyplot as plt

import thesUtils as tu

# Log file name format.
mmaLogNameFormat = '{type}.{m}x{d}x{n}.vdhd.CRR.O3.bench.{c}.json'
vecLogNameFormat = '{type}.{m}x{d}x{n}.vdhd.CRR.O3.vector.bench.{c}.json'

# Layouts in test with name.
layouts = [
  ((8, 8, 16), '8x8x16'),
  ((16, 8, 16), '16x8x16'),
  ((32, 8, 32), '32x8x32'),
  ((64, 8, 64), '64x8x64'),
  ((128, 8, 128), '128x8x128'),
]

def plotByType():
  # Set up figure and axes.
  fig = plt.figure()
  figWidth = 2
  figHeight = 2

  # Set up plot for data.
  layoutLabels = [layout[1] for layout in layouts]
  barNames = ['MMA', 'Vector']
  for i, type in enumerate(tu.orderedTypes):
    # Get the data for the type.
    mmaData, vecData = data[type]

    # Get data points.

    bars = [
      [mmaData[layoutName][0] for layoutName in layoutLabels],
      [vecData[layoutName][0] for layoutName in layoutLabels]
    ]

    # Get error bounds.
    errs = [
      [
        [mmaData[layoutName][1] for layoutName in layoutLabels],
        [mmaData[layoutName][2] for layoutName in layoutLabels]
      ],
      [
        [vecData[layoutName][1] for layoutName in layoutLabels],
        [vecData[layoutName][2] for layoutName in layoutLabels]
      ]
    ]

    # Get axis and start plotting.
    ax = fig.add_subplot(figHeight, figWidth, i + 1)
    tu.plotGroupedData(ax, layoutLabels, barNames, bars, errs)
    ax.set_title(type.capitalize())

    # ax.set_xlabel(, fontsize=8)
    ax.set_xlabel('Data Size')

  fig.tight_layout()
  fig.savefig('fig.png')


if __name__ == '__main__':
  # Get data.
  data = {}
  for type in tu.orderedTypes:
    # Holding place for vec and mma data.
    mmaData = {}
    vecData = {}

    # Get the vec and mma data.
    for (m, d, n), layoutName in layouts:
      # Read logs for data.
      mmaLog = mmaLogNameFormat.format(type=type, m=m, d=d, n=n, c='{}')
      vecLog = vecLogNameFormat.format(type=type, m=m, d=d, n=n, c='{}')

      # Save vec and mma data.
      _, _, mmaCycleStats = tu.getJsonCumulativeStats('logs/all/' + mmaLog, 25)
      mmaData[layoutName] = mmaCycleStats
      _, _, vecCycleStats = tu.getJsonCumulativeStats('logs/all/' + vecLog, 25)
      vecData[layoutName] = vecCycleStats

    # Save type data.
    data[type] = (mmaData, vecData)

  # Set up figure and axes.
  fig = plt.figure()
  figWidth = 2
  figHeight = 3

  plots = [layout[1] for layout in layouts]
  groupNames = tu.orderedTypes
  barNames = ['MMA', 'Vector']


  # Get data points.
  for type in groupNames:
    for layoutName in plots:
      print(type, layoutName, data[type][0][layoutName][0])

  for i, plot in enumerate(plots):
    bars = [
      [data[type][0][plot][0] for type in groupNames],
      [data[type][1][plot][0] for type in groupNames]
    ]

    # Get error bounds.
    errs = [
      [
        [data[type][0][plot][1] for type in groupNames],
        [data[type][0][plot][2] for type in groupNames]
      ],
      [
        [data[type][1][plot][1] for type in groupNames],
        [data[type][1][plot][2] for type in groupNames]
      ]
    ]

    # Get axis and start plotting.
    ax = fig.add_subplot(figHeight, figWidth, i + 1)
    tu.plotGroupedData(ax, groupNames, barNames, bars, errs)
    ax.set_title(plot)
    ax.set_xlabel('Data Type', fontsize=8)
    ax.set_ylabel('Runtime\n(ns)')

  fig.suptitle('MMA vs Vectorisation for Different Types and Kernel Layouts')
  fig.legend(['MMA', 'Vector'], loc='lower right')
  fig.tight_layout()
  fig.savefig('MMAvsVSX.png')

    #   if paperPlot:
    #   fig = plt.figure(figsize=(3.48761, 3))
    # else:
    #   fig = plt.figure()
    #
    #   fig.suptitle('Speedup of Polybench Benchmarks', fontsize=10)
    #   # Layout plot specifically for paper.
    #   if paperPlot:
    #     fig.tight_layout(pad=0)
    #     plt.gcf().subplots_adjust(bottom=0.21, left=0.116, right=.986, top=.93)
    #   # plt.show()
    #   if paperPlot:
    #     fig.savefig(output + '.pgf')
    #   else:
    #     fig.savefig(output + '.png')


# # Custom legend placing.
# if paperPlot:
#   ax.legend(bbox_to_anchor=(1.1, -0.12), prop={'size': 7}, frameon=True,
#             ncol=2, handletextpad=0.1, columnspacing=.1)
# else:
#   ax.legend(loc="upper right", prop={'size': 7}, ncol=2)
# if i == 0:
#   ax.set_ylabel('Speedup', fontsize=8)
#   ax.yaxis.labelpad = 0
