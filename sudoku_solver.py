from pulp import *
from itertools import product


def lp_solver(prior):
  seq = range(9)

  model = LpProblem('Sudoku', LpMinimize)
  x = LpVariable.dicts('X', (seq, seq, seq), cat=LpBinary)

  for i, j in product(seq, repeat=2):
    model += lpSum([x[i][j][k] for k in seq]) == 1
    model += lpSum([x[k][i][j] for k in seq]) == 1
    model += lpSum([x[i][k][j] for k in seq]) == 1

  for row, col in product(range(0, 9, 3), repeat=2):
    for k in seq:
      model += lpSum([x[i][j][k] for i in range(row, row+3) for j in range(col, col+3)]) == 1

  for p in prior:
    model += x[p[0]][p[1]][p[2]] == 1

  model.solve()
  value = [[None for i in seq] for j in seq]
  for i, j in product(seq, repeat=2):
      value[i][j] = int(sum([x[i][j][k].varValue * (k + 1) for k in seq]))

  print(LpStatus[model.status])
  for i in value:
    print(i)


lp_solver([(0, 0, 0), (1, 1, 1), (2, 2, 2)])
