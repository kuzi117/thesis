import matplotlib

matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

from matplotlib import pyplot as plt
from matplotlib.transforms import ScaledTranslation

import thesUtils as tu

logNameFormat = '{type}.8x32x16.vdhd.{aOrd}{bOrd}{cOrd}.O3.bench.{c}.json'

orders = [
  (('C', 'C', 'C'), '$\\textrm{C} = \\textrm{C} \\times \\textrm{C}$'),
  (('R', 'R', 'R'), '$\\textrm{R} = \\textrm{R} \\times \\textrm{R}$'),
  (('C', 'R', 'C'), '$\\textrm{C} = \\textrm{C} \\times \\textrm{R}$'),
  (('C', 'R', 'R'), '$\\textrm{R} = \\textrm{C} \\times \\textrm{R}$')
]

def generatePlot():
  # Get data.
  data = {}
  for type in tu.orderedTypes:
    # Holding place for access order data.
    orderData = {}

    # Get the data for each access order.
    for (aOrd, bOrd, cOrd), orderName in orders:
      # Read logs for data.
      log = logNameFormat.format(type=type, aOrd=aOrd, bOrd=bOrd, cOrd=cOrd, c='{}')

      # Save access order data.
      _, _, cycleStats = tu.getJsonCumulativeStats('logs/all/' + log, 25)
      orderData[orderName] = cycleStats

    # Save type data.
    data[type] = orderData

  # Set up figure and axes.
  fig = plt.figure()
  figWidth = 2
  figHeight = 2

  # Start plotting.
  groupLabels = [order[1] for order in orders]
  barLabels = ['runtime']
  for i, type in enumerate(tu.orderedTypes):
    # Get data for this type.
    orderData = data[type]

    # Set up bar data points.
    bars = [
      [orderData[order][0] for order in orderData]
    ]

    # Set up error data for the bars.
    errs = [
      [
        [orderData[order][1] for order in orderData],
        [orderData[order][2] for order in orderData]
      ]
    ]

    # Get axis and start plotting.
    ax = fig.add_subplot(figHeight, figWidth, i + 1)
    tu.plotGroupedData(ax, groupLabels, barLabels, bars, errs)

    # Set extra info.
    ax.set_title(f'\\texttt{{{type}}}')

    # Manipulate x ticks.
    dx, dy = 5, 0
    offset = ScaledTranslation(dx/fig.dpi, dy/fig.dpi, scale_trans=fig.dpi_scale_trans)
    for tick in ax.get_xticklabels():
      tick.set_rotation(15)
      tick.set_ha('right')
      tick.set_transform(tick.get_transform() + offset)

    ax.set_xlabel('Matrix Access Order')
    ax.set_ylabel('Cycles')

  # Save figure.
  fig.suptitle('Cycle Counts for Different Matrix Access Orders per Type')
  fig.set_size_inches(tu.textWidth, 5.5)
  fig.tight_layout()
  fig.savefig('accessOrder.png')
  fig.savefig('accessOrder.pgf')

def generateTable():
  # Get data.
  rows = []
  for type in tu.orderedTypes:
    # Get the data for each access order.
    for (aOrd, bOrd, cOrd), orderName in orders:
      # Read logs for data.
      log = logNameFormat.format(type=type, aOrd=aOrd, bOrd=bOrd, cOrd=cOrd, c='{}')

      # Save access order data.
      iterStats, timeStats, cycleStats = \
        tu.getJsonCumulativeStats('logs/all/' + log, 25)

      # Add row with name and data.
      rows.append(
        (f'\code{{{type}}}, {orderName}',
        (*iterStats[:2], *timeStats[:2], *cycleStats[:2]))
      )

  print(tu.tableData(rows))

if __name__ == '__main__':
  generatePlot()
  generateTable()
