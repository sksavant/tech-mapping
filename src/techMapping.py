#!/usr/bin/python
import sys
from graph_tool.all import *
class TechMapping:
    #define functions
    def __init__(self):
        #constructor
        #initialise the graph from the graphml file specified in the argument.
        try:
            self._graph_input_file = sys.argv[1] #take the input graph file from the terminal arguments
            try:
                self._graph_original = load_graph(self._graph_input_file) #load the graphml file as a graph object in graph-tool
                print "intialised well"
            except ValueError:
                print "Cannot read the file given:",self._graph_input_file
        except IndexError:
            print "ERROR: Graphml file is not specified"

    def andgate(self,vertex):
        adjacent_vertices=[]
        for e in self._graph_original.vertex(vertex).all_edges():
            adjacent_vertices.append(e.target())
        print "adj",adjacent_vertices
        self._graph_original.clear_vertex(vertex)
        self._graph_original.remove_vertex(vertex)
        vertex_nand=self._graph_original.add_vertex()
        self._graph_original.vertex_properties["name"][vertex_nand]="NAND"
        vertex_not=self._graph_original.add_vertex()
        self._graph_original.vertex_properties["name"][vertex_not]="NOT"
        for advertex in adjacent_vertices:
            self._graph_original.add_edge(vertex_nand,advertex)
        self._graph_original.add_edge(vertex_not,vertex_nand)

    def ConvertInputToBaseGates(self):
        for vertex in self._graph_original.vertices(): #loop through the nodes to get the & and | nodes. #SYNTAX NOT CORRECT : TO CHECK
            if self._graph_original.vertex_properties["name"][vertex]=="&":
                self.andgate(vertex)
    def finalAllocation(self):
        #To print the final allocation of the logic elements
        print "The final gate implementation of the logic circuit is :"

if __name__=="__main__":
    #do something
    tm = TechMapping()
    #graph_draw(tm._graph_original, vertex_text=tm._graph_original.vertex_properties["name"], vertex_font_size=12, output_size=(200,200))
    tm.ConvertInputToBaseGates()
    graph_draw(tm._graph_original, vertex_text=tm._graph_original.vertex_properties["name"], vertex_font_size=12, output_size=(200,200))
    tm.finalAllocation()
    print "ending"
