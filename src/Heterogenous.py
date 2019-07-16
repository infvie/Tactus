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

from gurobi import *



def solve(rack_name, slots,chips, quantity, powerdraw, slots_required):

    m = Model()

    # always need the load on each phase Lead
    L = m.addVars(3, name='phases')

    # add x_ij where i is the chip and j is the possible orientations
    # assume only 2 slots necessary
    # orientation
    # 1 = 1,2
    # 2 = 1,3
    # 3 = 2,3
    # again the set is not an SOS
    indicies = [(chip,orientation) for chip in chips for orientation in range(3)] # gen pairs 
    x = m.addVars(indicies,vtype=GRB.INTEGER)

    m.addConstr(quicksum(powerdraw[chip]*(x[chip,0]+x[chip,1]) for chip in chips),GRB.EQUAL,L[0]);
    m.addConstr(quicksum(powerdraw[chip]*(x[chip,0]+x[chip,2]) for chip in chips),GRB.EQUAL,L[1]);
    m.addConstr(quicksum(powerdraw[chip]*(x[chip,1]+x[chip,2]) for chip in chips),GRB.EQUAL,L[2]);

    m.addConstrs(quicksum(x[chip,orient] for orient in range(3)) == quantity[chip] for chip in chips);

    # simplifies later constraints
    m.addConstr(L[0],GRB.LESS_EQUAL,L[1])
    m.addConstr(L[1],GRB.LESS_EQUAL,L[2])

    m.setObjective(L[2]-L[0])

    m.optimize()
    
    # print solution
    for chip in chips:
        for i in range(3):
            print(f'Put $(x[chip,i]) $chip in orientation $i')
    



