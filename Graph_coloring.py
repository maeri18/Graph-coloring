"""A graph is set of tuples of nodes. Nodes are labeled with integers (starting at 0).
For example, a graph could be {(0,1),(1,2),(2,3),(1,3)}. It represents a graph with 4 vertices, 4 edges.
There is an edge between node 0 and node 1, node 1 and node 2, between node 2 and node 3, between node 1 and node 3.

For the chromosomes of the genetic algorithm, we will use a list in which the first element is 
the color of node 1, the second is the color of node 2... 
The length of chromosomes will hence depend on the number of nodes of the input graph.


Constraints :
* The graph cannot contain self loops. Or self loops do not count for adjacency.

* The nodes of the graph should cover all consecutive numbers within a range.
For example, we can't have a graph that contain node 1, node 3, and node 4, with no node 2 and node 0.
And names of nodes start at 0.
* If between two nodes, there are multiple edges, oriented or not, they all will be counted once. This means that in our graph,
we should not have edge (3,1) and edge (1,3), or multiple times edge (3,1). To prevent adding multiple time the same edge, we declared our graph as a set.
And to avoid put an edge and its reversal ((3,1) and (1,3)), we have a function well-formed graph"""

import random
from pyvis.network import Network #for graph visualization

Graph = set[tuple[int,int]]
Chromosome = list[str]
Generation = list[Chromosome]

population : int = 4 #even number always

#list of 35 colors
colors = ["#FB0000","#004CFB","#deb887","#008080","#FFA500","#FFB6C1","#00FFFF","#7FFFD4","#008000","#FFFF00","#964B00","#faf0e6","#000000","#A020F0","#DFFF00","#7B3F00",
        "#DC143C","#00FFFF","#8B0000","#00008B","#006400","#808080","#FF00FF","#800000","#bc8f8f","	#dda0dd","#CD853F","#4169e1","2E8B57","#D8BFD8","#30D5C8","#A50055","#FF1493","#FFD700","#E6E6FA"]

#test graphs
g1 : Graph = {(0,1),(1,2),(2,3),(1,3)}
g2 : Graph = {(0,2),(2,7),(4,5),(6,3),(0,4),(1,5),(7,3),(4,9),(8,1),(4,2),(7,8),(9,0)}
g3 : Graph = {(0,1),(2,0),(3,2),(5,2),(6,7),(1,7),(14,15),(11,3),(15,3),(10,4),(16,10),
              (4,11),(17,20),(9,18),(5,18),(3,17),(13,1),(9,0),(12,10),(15,8),(6,9),(20,5),(17,14),(8,7),(19,16),(18,10),(7,16),(17,5),(12,6),(16,20)}
g4 : Graph = {(0,1),(0,2),(2,3)}
g5 : Graph = {(0,1),(0,2),(1,3),(2,4),(3,5),(4,5)} #hexagon--requires at least 2 colors
g6 : Graph = {(0,1),(1,2),(2,0)} #triangle -- requires at least 3 colors
g7 : Graph = {(0,1),(1,2),(2,3),(3,0)} #square -- requires at least 2 colors

def well_formed_graph(g : Graph)->bool:
    """Checks whether  graph g satisfies our conditions on not.
    The conditions are: 
    * The graph cannot contain self loops. Or self loops do not count for adjacency.
    * The nodes of the graph should cover all consecutive numbers within a range.
    * If between two nodes, there are multiple edges, oriented or not, they all will be counted as one single edge. """
    nodes:set[int]=set()
    for n1,n2 in g:
        nodes.add(n1)
        nodes.add(n2)
        if n1==n2:#self loops
            return False
        for n11,n22 in g:
            if n11 == n2 and n22==n1:#avoid counting an edge twice. For example:  (3,1) and (1,3)
                return False
    max_node:int = max(nodes)
    for i in range(max_node+1):
        if i not in nodes:#there is a node missing in the range.
            return False 
    return True

assert(well_formed_graph(g1)==True)

def nodes_of_graph(g:Graph)->set[int]:
    """Returns the set of nodes of a graph"""
    nodes:set[int]=set()
    for node1,node2 in g:
        nodes.add(node1)
        nodes.add(node2)
    return nodes

def chromosome_length(g:Graph)->int:
    """Calculates the number of nodes in the graph G, which is also the length of a chromosome"""
    return len(nodes_of_graph(g))

assert(chromosome_length(g1)==4)

def fitness_max(g:Graph)->int:
    """Calculates the maximal value of the fitness function, which in our case will be the goal value
    of the fitness_function applied to a chromosome
    """
    return len(g)
    
    
def fitness_function(g:Graph, c: Chromosome)->int:
    """Calculates the number of well colored edges (that is, adjacent node have different colors)
    Hence the higher the value of the fitness function, the better for us."""
    well_colored:int=0
    for n1,n2 in g:
        if c[n1].lower() != c[n2].lower(): #well colored edge
            well_colored += 1
    return well_colored

def random_population(g:Graph,pop:int, k:int)->Generation:
    """Produces the initial generation of chromosomes.
    g:Graph is the graph, of type Graph
    pop:int is the initial population of chromosomes.
    k:int is the number of colors we can use.
    k<=35 as currently we dispose of 35 colors
    The function returns a list of randomly generated chromosomes
    """
    chrs_length = chromosome_length(g) #length of chromosomes

    init_chrs:Generation=[] #result list

    for i in range(pop):
        c:Chromosome=[]
        for j in range(chrs_length):
            #we use only the first k colors in the list colors
            c.append(colors[random.randint(0,(k-1))]) 
        init_chrs.append(c)
    return init_chrs
  

def crossing(c1:Chromosome, c2:Chromosome,crossing_point:int)->tuple[Chromosome,Chromosome]:
    """Produces the two descendants of c1 and c2
    c1:Chromosome
    c2:Chromosome
    crossing_point:int indicates after how many genes the cross over point is taken.

    length c1 == length c2
    crossing_point > 0
    crossing_point < length of a chromosome"""

    chr1:Chromosome=[] #first child
    chr2:Chromosome=[] #second child
    if(len(c1)==len(c2)):
        if crossing_point > 0 and crossing_point < len(c1):
            chr1 = c1[:crossing_point] + c2[crossing_point:]
            chr2 = c2[:crossing_point] + c1[crossing_point:]
            return (chr1,chr2)
        else:
            raise Exception("Invalid crossing point.")
    else:
        raise Exception("Chromosomes of different length. Can't cross")

def mutation(c:Chromosome,fmax:int, g:Graph,k:int)->Chromosome:
    """Randomly mutates a chromosome so that the chromosome gets closer to the goal
    fmax: maximum value of the fitness function for our graph 
    fval: fitness function value for chromosome c
    k:int number of colors we can use"""
    fval : int = fitness_function(g,c)
    gene_to_mutate:int = random.randint(0,len(c)-1)#position of the gene to mutate

    #We only mutate chromosomes that are not solutions
    if fval != fmax:
        fmc : int = fval #fitness value of the mutated chromosome
        mc : Chromosome = c #mutated  chromosome
 
        #We only perform a mutation if the fitness score of the mutated chromosome is better
        while True:
            mc[gene_to_mutate] = colors[random.randint(0,k-1)]
            fmc = fitness_function(g,mc)
            if fmc >= fval:
                return mc
        
    return c
  
    
def next_gen_probabilities(gen:Generation,g:Graph)->list[float]:
    """Calculates the probability of choosing each chromosome in the list of chromosome gen
    It returns a list of probabilities where the first probability is the probability of choosing gen[0], the second is the 
    probability of choosing gen[1]..."""
    choosing_probabilities : list[float] = []
    fitness_total_gen : int = 0
    for c in gen:
        fval:int = fitness_function(g,c)
        choosing_probabilities.append(fval)
        fitness_total_gen += fval
    if fitness_total_gen!=0:
        return [x/fitness_total_gen for x in choosing_probabilities] 
    else :
        return []



def colorize(g:Graph,k:int,fmax:int)->Chromosome:
    """Function that returns a solution to the graph coloring problem with k colors
    k<=35"""

    #initial generation of chromosomes
    gen : Generation = random_population(g, population, k)
    stuck:int=0
    best_fitness : int = fitness_function(g,gen[0])
    while True:
        #If we are stuck with the same best fitness value since 1000 iteration, then we abort the search
        if stuck>1000:
            return None
        next_gen : Generation = []
        choosing_probabilities = next_gen_probabilities(gen, g)

        #there is no solution, fitness value is evaluated to zero
        if choosing_probabilities == []:
                return None
        #selecting the best parents
        gen = random.choices(gen,weights=choosing_probabilities,k=population)
        i : int =0 
        while i < population-1:
            c1,c2 = crossing(gen[i],gen[i+1],random.randint(1,population-2))
            fitness_c1 = fitness_function(g,c1)
            fitness_c2 = fitness_function(g,c2)

            #if we found a solution we return it
            if fitness_c1 == fmax:
                return c1
            if fitness_c2 == fmax:
                return c2
            
            #next generation is composed of children
            next_gen.append(c1)
            next_gen.append(c2)
            i += 2

        #mutation
        for c in next_gen:
            if random.randint(0,1):
                c = mutation(c,fmax,g,k)
        
        #handling plateau or no solution search (nothing gets better)
        new_best_fitness:int = max([fitness_function(g,c) for c in next_gen]+[best_fitness]) #best fitness for this generation
        if best_fitness == new_best_fitness :
            stuck +=1
        else:
            best_fitness = new_best_fitness
            stuck = 0
        
        gen = next_gen


def visualize_graph(g:Graph,coloring:Chromosome,name="graph"):
    """Allows to visualize the graph"""
    nodes:list[int] = list(nodes_of_graph(g))
    graph_drawing = Network()
    graph_drawing.add_nodes(nodes,label=[str(n) for n in nodes],color=coloring)
    graph_drawing.add_edges(g)
    graph_drawing.show(name+".html",notebook=False)

def graph_coloring(g:Graph)->tuple[int,Chromosome]:
    """Returns the minimal number of colors necessary to color graph g, 
    along with a possible colouring for the minimal amount of colors"""
    coloring:Chromosome 
    temp:Chromosome = None
    if well_formed_graph(g):
        for k in range(35,-1,-1):
            coloring = temp
            temp:Chromosome = colorize(g,k,fitness_max(g))
            if temp == None: #no solution is found
                visualize_graph(g,coloring)
                return (k+1,coloring) 
    else:
        raise Exception("Your graph is not well formed. It either possesses self-loops, \n* Or you considered incoming and outgoing edges,that is an edge is counted at least twice, \n* Or you didn't named you nodes properly. Nodes are named from 0 to n, with no number missing in that range")

def main():  
    color = random.randint(0,34)   
    #graph 1
    #visualize_graph(g1,[colors[color] for x in range(len(nodes_of_graph(g1)))],"graph1")
    #minimal_color, coloring = graph_coloring(g1)
    #print("The graph g1 can be colorized with ", minimal_color, " colors")

    #graph 2
    #visualize_graph(g2,[colors[color] for x in range(len(nodes_of_graph(g2)))],"graph2")
    #minimal_color, coloring = graph_coloring(g2)
    #print("The graph g2 can be colorized with ", minimal_color, " colors")
    
    #graph 3
    #visualize_graph(g3,[colors[color] for x in range(len(nodes_of_graph(g3)))],"graph3")
    #minimal_color, coloring = graph_coloring(g3)
    #print("The graph g3 can be colorized with ", minimal_color, " colors")
    
    #graph 4
    #visualize_graph(g4,[colors[color] for x in range(len(nodes_of_graph(g4)))],"graph4")
    #minimal_color, coloring = graph_coloring(g4)
    #print("The graph g4 can be colorized with ", minimal_color, " colors")
    
    #graph 5 
    visualize_graph(g5,[colors[color] for x in range(len(nodes_of_graph(g5)))],"graph5")
    minimal_color, coloring = graph_coloring(g5)
    print("The graph g5 can be colorized with ", minimal_color, " colors")

    #graph 6
    #visualize_graph(g6,[colors[color] for x in range(len(nodes_of_graph(g6)))],"graph6")
    #minimal_color, coloring = graph_coloring(g6)
    #print("The graph g6 can be colorized with ", minimal_color, " colors")

    #graph 7
    #visualize_graph(g7,[colors[color] for x in range(len(nodes_of_graph(g7)))],"graph7")
    #minimal_color, coloring = graph_coloring(g7)
    #print("The graph g7 can be colorized with ", minimal_color, " colors")
    

if __name__=="__main__":
    main()