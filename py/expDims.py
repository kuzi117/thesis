import thesUtils as tu

def printDimsTable(typeName, dimF):
  lines = ['{\small Acc. Layout} & Computation']
  for layout in tu.layouts:
    m, n = layout
    a, c, b = dimF(layout, tu.types[typeName])
    tableParts = [
      F'${m} \\times {n}$',
      F'\\matmul{{{a}}}{{{c}}}{{{b}}}'
    ]
    lines.append(' & '.join(tableParts))
  for line in lines:
    print(line, end=' \\\\\\hline\n')

if __name__ == '__main__':
  print(F'ThesisUtils v{tu.version}')
  #for typeName, typeInfo in types.items():
  #  for layout in layouts:
  #    a, c, b = getMLMADims(layout, typeInfo)
  #    print(F'{typeName}, {layout}: {a}x{b} = {a}x{c} * {c}x{b}')

  printDimsTable('i4', tu.getMLSADims)
  printDimsTable('float', tu.getMLMADims)
  printDimsTable('half', tu.getMLMADims)
