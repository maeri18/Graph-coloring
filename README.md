
# Graph Coloring Genetic Algorithm
This Python script implements a genetic algorithm for solving the graph coloring problem. Given a graph represented as a set of tuples of nodes, the goal is to find the minimal number of colors needed to color the graph such that no adjacent nodes have the same color.

## Problem Description
A graph is defined as a set of tuples of nodes, where nodes are labeled with integers starting at 0. For example, a graph could be {(0,1),(1,2),(2,3),(1,3)}, representing a graph with 4 vertices and 4 edges.

For the chromosomes of the genetic algorithm, a list is used where each element corresponds to the color of a node in the graph. The length of chromosomes depends on the number of nodes in the input graph.

## Constraints:
* The graph cannot contain self-loops.
* Nodes of the graph should cover all consecutive numbers within a range, starting from 0.
* Multiple edges between two nodes are counted only once.
  
## Functionality
The script provides functionalities to:

* Check if a graph satisfies certain conditions.
* Calculate the fitness function for a chromosome.
* Generate random initial populations of chromosomes.
* Perform crossover and mutation operations.
* Determine the minimal number of colors required to color a graph.

## Usage
To use the script:

* Define your graph as a set of tuples of nodes.
* Call the graph_coloring function with your graph as input.
* The function returns the minimal number of colors required and a possible coloring scheme.

### Example
```sh
# Define your graph
graph = {(0,1),(1,2),(2,3),(1,3)}

# Get the minimal number of colors and coloring scheme
minimal_colors, coloring_scheme = graph_coloring(graph)

print("The graph can be colorized with", minimal_colors, "colors.")
```

## Dependencies
This script requires the following dependencies:

### pyvis: for graph visualization
Install [pyvis](https://pyvis.readthedocs.io/en/latest/install.html) using pip:

```sh
pip install pyvis
```
## Author
This script was authored by Ingrid Maéva chekam.
