import matplotlib.pyplot as plt
from gurobipy import *
import seaborn as sns
import pandas as pd


def glob(rack_name, chips, quantity, powerdraw, slots_required):
    
    # init the model
    m = Model('Tactus')
    
    # fixed data
    slots = range(1,49)
    phases = [1,2,3]
    theta = ['L1-L2','L2-L3','L3-L1']
    
    # add vars
    L  = m.addVars(rack_name,phases,name='phases')
    x = m.addVars(chips,theta,rack_name,slots,vtype=GRB.BINARY,name='placement')
    u = m.addVars(chips,theta,rack_name,vtype=GRB.BINARY,name='singleassignment')
    z = m.addVar(name='toprack')
    
    # add objective function
    m.setObjective(quicksum(L[rack,1]-L[rack,3] for rack in rack_name)-z,GRB.MINIMIZE)
    
    # add constraints - desc in docs
    m.addConstrs(x.sum(chip,'*','*','*') == quantity[chip] for chip in chips);
    m.addConstrs(x.sum('*','*','*',slot) <= 1 for slot in slots);
    m.addConstr(x.sum('*',['L1-L2','L2-L3'],'*',range(1,17)) == 0);
    m.addConstr(x.sum('*',['L1-L2','L3-L1'],'*',range(17,33)) == 0);
    m.addConstr(x.sum('*',['L2-L3','L3-L1'],'*',range(33,49)) == 0);
    m.addConstrs(u.sum(chip,'*','*') <= 1 for chip in chips);
    m.addConstrs(x.sum(chip,orientation,rack,'*') <= quantity[chip]*u[chip,orientation,rack] for chip in chips for rack in rack_name for orientation in theta)
    for rack in rack_name:
        m.addConstr(quicksum(powerdraw[chip]*x.sum(chip,['L1-L2','L3-L1'],rack) for chip in chips) == L[rack,1]); # L1
        m.addConstr(quicksum(powerdraw[chip]*x.sum(chip,['L1-L2','L2-L3'],rack) for chip in chips) == L[rack,2]); # L2
        m.addConstr(quicksum(powerdraw[chip]*x.sum(chip,['L2-L3','L3-L1'],rack) for chip in chips) == L[rack,3]); # L3
    m.addConstrs(L[rack,1]>=L[rack,2] for rack in rack_name);
    m.addConstrs(L[rack,2]>=L[rack,3] for rack in rack_name);
    m.addConstr(quicksum(slot/100*x[chip,orientation,rack,slot] for chip in chips for rack in rack_name for orientation in theta for slot in slots) == z);
    
    # solve model
    m.optimize()
    
    # visualize solution
    df = pd.DataFrame(index=range(1,49))
    for key in x.keys():
        if x[key].X > 0:
            chip, orientation, rack, slot = key
            df.loc[slot,rack] = f'{chip}->{orientation}'
    
    rack = [rack for rack, phase in L.keys()]
    phase = [phase for rack, phase in L.keys()]
    load = [L[var].X for var in L]
    data = {'Rack':rack,'Phase':phase,'Load':load}
    
    df = pd.DataFrame(data)
    
    plt.subplot(1, 2, 1)
    sns.barplot(x='Rack',y='Load',hue='Phase',data=data,palette='Blues')
    plt.title('Loads Across Phase')
    plt.xlabel('Rack')
    plt.ylabel('Power Consumption (W)')
    
    grouped = df.groupby('Rack')
    diff = grouped['Load'].max() - grouped['Load'].min()
    
    plt.subplot(1,2,2)
    sns.barplot(x=diff.index,y=diff.values)
    plt.title('Largest Phase Difference')
    plt.ylabel('Power Difference (W)')
    plt.tight_layout()
    plt.show()
        
        
    
    