#!/bin/python

set_size = 500
r = np.zeros((set_size+1, set_size+1), dtype=np.int32)
for i in range(1, set_size+1):
    for j in range(1, set_size+1):
        if i!=j and sqrt((i)*(j)) == floor(sqrt((i)*(j))):
            r[i,j] = 1
a, b = np.where(np.triu(r[1:, 1:])==1)
m = gp.Model("find")
X = m.addVars(set_size, vtype=GRB.BINARY, name="X")
m.setObjective(
    gp.quicksum(
        X[i]
        for i in range(len(X))
    ),
    GRB.MAXIMIZE,
)
m.addConstrs(
    (X[i] <= 1-X[j] for i, j in zip(a,b)),
    name="a_or_b_or_neither_constraint",
)
m.optimize()

# Sanity Check
sol = [idx+1 for idx, v in enumerate(m.getVars()) if v.X == 1]
for i in sol:
    for j in sol:
        if i!=j and sqrt((i)*(j)) == floor(sqrt((i)*(j))):
            print('fail')
