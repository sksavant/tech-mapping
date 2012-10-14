#!/usr/bin/python
import sys
import graphtool
class TechMapping:
    #define functions
    def __init__(self):
        #constructor
        #initialise the graph from the graphml file specified in the argument.
        self._graph_input_file = sys.argv[1] #take the input graph file from the terminal arguments
        self._g = load_graph(_graph_input_file) #load the graphml file as a graph object in graph-tool

if __name__=="__main__":
    #do something
    tm = TechMapping()
    print tm.finalAllocation()
