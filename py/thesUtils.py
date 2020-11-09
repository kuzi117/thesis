version = '1.0'

vregSize = 128

types = {
  'i4': (4, (4, 8)),
  'i8': (8, (4, 4)),
  'i16': (16, (4, 2)),
  'half':(16, (4, 2)),
  'float': (32, (4, 1)),
#  'double': (64, (4, 1))
}

layouts = [(1, 1), (2, 1), (1, 2), (2, 2), (4, 1), (1, 4), (4, 2), (2, 4), (8, 1), (1, 8)]
layouts = sorted(layouts, key=lambda x: x[0] * x[1] + max(x[0], x[1]) + x[1])

def lcm(a, b):
  # GCD division algorithm.
  gcd = a
  rem = b
  while rem != 0:
    temp = rem
    rem = gcd % rem
    gcd = temp

  # LCM is ab / gcd(a, b)
  prod = a * b
  assert prod % gcd == 0, 'Product was not divisible by GCD'
  return (a * b) // gcd

def getMLSADims(layout, typeInfo):
  m, n = layout
  s, (i, j) = typeInfo

  a = i * m
  b = i * n
  c = j

  return (a, c, b)


def getMLMADims(layout, typeInfo):
  m, n = layout
  s, (i, j) = typeInfo

  assert vregSize // s, 'VR wasn\'t evenly divided by type size'
  vregElems = vregSize // s

  a = lcm(vregElems, i * m)
  b = lcm(vregElems, i * n)
  c = lcm(vregElems, j)
  return (a, c, b)
