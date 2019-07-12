# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.1.7
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# This is a just an implementation script to understand what is happening ref the [docs](../Formulation.md)

from gurobipy import *

# init model
m = Model()

# add a powerdraw constant for chipset
P = 50

# add Lead var terms
L = m.addVars(3)

# add vars for number in every orientation
# x1 = 1,2
# x2 = 1,3
# x3 = 2,3 
x = m.addVars(3)

# add x for orientation terms
m.addConstr(P*(x[0]+x[1]),GRB.EQUAL,L[1])
m.addConstr(P*(x[0]+x[2]),GRB.EQUAL,L[2])
m.addConstr(P*(x[1]+x[2]),GRB.EQUAL,L[3])

# make sure we are doing this for the number of chips that we have
n = 15
m.addConstr(quicksum(x),GRB.EQUAL,n)


