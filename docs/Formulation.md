---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.1'
      jupytext_version: 1.1.7
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# Formulation


### Problem Statement


Most computing clusters are homogenous in the sense that they are composed of chipsets that are uniform in power draw. This unifomity makes it easy to load balance along the leads in a PDU. The load balancing amongst heterogenous clusters quickly becomes non-trivial and leads to safety issues. In this formulation, we construct a generalized solution to this load balancing problem using mixed integer programming.


### Homogenous Chipset Formulation


We will begin by solving the easiest form of this problem and gradually increasing the difficulty and the complexity of the problem. We begin with with a single rack with 15 slots for uniform chipsets.


### Variables


<center>$L_i  \quad \forall i \in \{1...n\}$ the amount of power flow through a lead<center> 
<center>$x_j \quad \forall j \in \{1...m\}$ the number of chipsets in a specific orientation *<center>


###### * the set of orientations is finite $ \{ (1,2),(1,3),(2,3)\} $ and independent of ranking or order


### Objective Function


There are several opitons for an objective function for this problem:

1) minimizing the largest power difference between the set of leads 

$$ \mathbf{min} \quad Max(L_{i}-L_{j}) \quad \forall i,j\in S$$ 

2) minimize the total power difference between all the leads 

$$ \mathbf{min} \quad \sum_{i,j \in S}{|L_{i}-L_{j}|} $$


Both of these objectives have trade-offs, 1) might lead to a solution where the overall powerflow through the system may be suboptimal and 2) has the issue of leading to a solution where one pair of leads has a huge difference to allow for the other pairs to have the smallest possible gap.


### Constraints


There is a single constraint for our problem which is the the effect of the orientation on the total lead value which can be expressed as:

<center>$P\theta x = L$</center>

where $P$ is a constant that represents the power draw from a single chipset

$x$ is our set of decision varibles in matrix form

$\theta$ is a matrix representing the possible orientations e.g 

$$
\begin{vmatrix}
1 & 1 & 0 \\ 
1 & 0 & 1 \\
0 & 1 & 1 
\end{vmatrix}
$$
