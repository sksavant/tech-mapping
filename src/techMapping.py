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
                self._g = load_graph(self._graph_input_file) #load the graphml file as a graph object in graph-tool
                print "intialised well"
            except ValueError:
                print "Cannot read the file given:",self._graph_input_file
        except IndexError:
            print "ERROR: Graphml file is not specified"
             
        
    
    def finalAllocation(self):
        #To print the final allocation of the logic elements
        print "The final gate implementation of the logic circuit is :"

if __name__=="__main__":
    #do something
    tm = TechMapping()
    graph_draw(tm._g, vertex_text=tm._g.vertex_index, vertex_font_size=12, output_size=(200,200), output="viewgraph.pdf")
    tm.finalAllocation()
    print "ending"
