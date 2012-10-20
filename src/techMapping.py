#!/usr/bin/python
import sys
from graph_tool.all import *
class TechMapping:
    #define functions
    def __init__(self):
        #constructor
        #initialise the graph from the graphml file specified in the argument.
        try:
            self._graph_input_file_name = sys.argv[1] #take the input graph file from the terminal arguments
            try:
                self._graph_original = load_graph(self._graph_input_file_name) #load the graphml file as a graph object in graph-tool
                print "intialised well"
            except ValueError:
                print "Cannot read the file given:",self._graph_input_file_name
        except IndexError:
            print "ERROR: Graphml file is not specified"
    
    def ninandtobase(self,node):
        _node_degree=node.outdegree() #? Is it right? ?-in and
        # TO convert to base
    
    def ConvertInputToBaseGates(self):
        for node in _graph_original.nodes: #loop through the nodes to get the & and | nodes. #SYNTAX NOT CORRECT : TO CHECK
            if node["name"]=='&':
                tm.ninandtobase(node)
            elif node["name"]=='|':
                tm.ninortobase(node):
    
    def finalAllocation(self):
        #To print the final allocation of the logic elements
        print "The final gate implementation of the logic circuit is :"

if __name__=="__main__":
    #do something
    tm = TechMapping()
    tm.ConvertInputToBaseGates()
    graph_draw(tm._graph_original,  vertex_font_size=12, output_size=(1000,1000), output="viewgraph.pdf")
    tm.finalAllocation()
    print "ending"
