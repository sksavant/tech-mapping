#!/usr/bin/python
import sys
from operator import itemgetter
#import os
from graph_tool.all import *
class TechMapping:
    #define functions
    def __init__(self,fn=None):
        #constructor
        #initialise the graph from the graphml file specified in the argument.
        try:
            self._graph_input_file = sys.argv[1] #take the input graph file from the terminal arguments
            f = self._graph_input_file
            #if ".blif" in f:
            #   os.system("../blif2graphml "+f+" >"+f[0:len(f)-5]+".xml")
            #   f = f[0:len(f)-5]+".xml"
            try:
                self._graph_original = load_graph(self._graph_input_file) #load the graphml file as a graph object in graph-tool
                print "intialised well"
            except ValueError:
                print "Cannot read the file given:",self._graph_input_file
        except IndexError:
            print "ERROR: Graphml file is not specified"
        if fn:
            self._graph_original = load_graph(fn)

    def two_input_and_gate(self, fan_in_vertices, x, i, temp_vertices):
        g= self._graph_original
        vertex_not = g.add_vertex()
        g.vertex_properties["name"][vertex_not]="!"
        vertex_nand = g.add_vertex()
        g.vertex_properties["name"][vertex_nand]="NAND"
        temp_vertices.append(vertex_not)
        g.add_edge(vertex_not,vertex_nand)
        g.add_edge(vertex_nand,fan_in_vertices[2*x])
        g.add_edge(vertex_nand,fan_in_vertices[2*x+i])

    def two_input_or_gate(self, fan_in_vertices, x, i, temp_vertices):
        g= self._graph_original
        vertex_not1 = g.add_vertex()
        g.vertex_properties["name"][vertex_not1]="!"
        vertex_not2 = g.add_vertex()
        g.vertex_properties["name"][vertex_not2]="!"
        vertex_nand = g.add_vertex()
        g.vertex_properties["name"][vertex_nand]="NAND"
        temp_vertices.append(vertex_nand)
        g.add_edge(vertex_nand, vertex_not1)
        g.add_edge(vertex_nand, vertex_not2)
        g.add_edge(vertex_not1, fan_in_vertices[2*x])
        g.add_edge(vertex_not2, fan_in_vertices[2*x+i])
 
    def balanced_n_input_and_gate(self,vertex):
        g= self._graph_original
        fan_in_vertices = []
        temp_vertices=[]
        for e in vertex.out_edges():
            fan_in_vertices.append(e.target())
        p=len(fan_in_vertices)
        while p>1:
            if(p%2==1):
                self.two_input_and_gate(fan_in_vertices,p/2,-1,temp_vertices)
                fan_in_vertices=fan_in_vertices[:-2]
                fan_in_vertices.append(temp_vertices[0])
                temp_vertices=[]
            q=len(fan_in_vertices)/2
            for x in range (0,q):
                self.two_input_and_gate(fan_in_vertices,x,1,temp_vertices)
            fan_in_vertices=temp_vertices
            temp_vertices=[]
            p=len(fan_in_vertices)
        for e in vertex.in_edges():
            g.add_edge(e.source(),fan_in_vertices[0] )
        g.clear_vertex(vertex)
        g.remove_vertex(vertex)

    def balanced_n_input_or_gate(self,vertex):
        g= self._graph_original
        fan_in_vertices = []
        temp_vertices=[]
        for e in vertex.out_edges():
            fan_in_vertices.append(e.target())
        p=len(fan_in_vertices)
        while p>1:
            if(p%2==1):
                self.two_input_or_gate(fan_in_vertices,p/2,-1,temp_vertices)
                fan_in_vertices=fan_in_vertices[:-2]
                fan_in_vertices.append(temp_vertices[0])
                temp_vertices=[]
            q=len(fan_in_vertices)/2
            for x in range (0,q):
                self.two_input_or_gate(fan_in_vertices,x,1,temp_vertices)
            fan_in_vertices=temp_vertices
            temp_vertices=[]
            p=len(fan_in_vertices)
        for e in vertex.in_edges():
            g.add_edge(e.source(),fan_in_vertices[0])
        g.clear_vertex(vertex)
        g.remove_vertex(vertex)

    def ConvertInputToBaseGates(self):
        g= self._graph_original
        k=1
        while(k==1):
            k=0
            for vertex in g.vertices():
                if g.vertex_properties["name"][vertex]=="&":
                    self.balanced_n_input_and_gate(vertex)
                    k=1
                    break
                elif g.vertex_properties["name"][vertex]=="|":
                    self.balanced_n_input_or_gate(vertex)
                    k=1
                    break

    def not_redundancy_removal(self):
        g= self._graph_original
        vp = g.vertex_properties["name"]
        trv = [] #To Remove vertices
        for v in g.vertices():
            try:
                nv= None
                i=0
                for e in v.out_neighbours():
                    if i is 1:
                        break
                    i=i+1
                    nv=e
                # To check if the vertex is a not, it's out_degree is one (indegree any), the adj vertex is a not and it has only one indegree.
                if vp[v] is '!' and v.out_degree() is 1 and  vp[nv] is '!' and nv.in_degree() is 1 and nv.out_degree() is 1:
                    #print "check",vp[v], v.out_degree(), vp[nv], nv.in_degree(), v
                    vp[v] = 'n!'
                    vp[nv] = 'n!'
                    trv.append(v)
                    #print "check",vp[v], v.out_degree(), vp[nv], nv.in_degree(), v
                    #print trv
            except TypeError:
                #print "error"
                pass
        print "Removing",len(trv),"!! redundancies"
        newtrv=[]
        for vert in trv: # trv is list of vertices(starting) which have double nots
            #print "name",vp[vert]
            in_vertices=vert.in_neighbours()
            nvert=None
            outvert=None
            i=0
            for e in vert.out_neighbours():
                nvert=e
            newtrv.append(vert)
            #print "vert", vp[vert]
            newtrv.append(nvert)
            #print vp[nvert]
            for e in nvert.out_neighbours():
                outvert=e
            #print vp[vert],vp[nvert]
            #assert(vp[v]=='n!' and vp[nv]=='n!')
            for inv in in_vertices:
                g.add_edge(inv,outvert)
        #print newtrv
        for e in newtrv:
            #print vp[e]
            g.clear_vertex(e)
            #print "newtrv",newtrv
        # The great loop is here...
        k=1
        while(k==1):
            k=0
            for vertex in g.vertices():
                if g.vertex_properties["name"][vertex]=="n!":
                    g.remove_vertex(vertex)
                    k=1
                    break

    def do_dfs(self): #dFS on graph to number the numbers... a number on the node denotes when it should be fucked.
        g = self._graph_original
        vprop_dfs = g.new_vertex_property("int")
        vprop_mark = g.new_vertex_property("bool")
        g.vertex_properties["level"] = vprop_dfs
        g.vertex_properties["visited"] = vprop_mark
        self.set_all_levels_to_zero() #clean the graph :P
        #find sources and initialize everything to zero.
        self.find_sources()
        #find the next adj vertices
        self.go_find_indices() #GTFO and find the indices for vertices which is the max distance from any sink
        #while(True):

    def go_find_indices(self):
        self.sorted_list=[]
        sl = self.sorted_list
        self.index = 0
        for v in self.sources:
            self.visit(v)

    def visit(self,v):
        g = self._graph_original
        vpl = g.vertex_properties["level"]
        vpv = g.vertex_properties["visited"]
        if vpv[v] == False :
            #means not visited
            vpv[v] = True
            for nv in v.out_neighbours():
                self.visit(nv)
        self.sorted_list.append(v)
        vpl[v] = self.index
        self.index=self.index+1

    def set_all_levels_to_zero(self):
        g = self._graph_original
        vpl = g.vertex_properties["level"]
        vpv = g.vertex_properties["visited"]
        for v in g.vertices():
            vpl[v] = -1 #sentinel value to check that it is not visited
            vpv[v] = False

    def find_optimal_pattern(self):
        #For each vertex in the sorted_list, arise the function optimal_pattern(v) to find the optimal pattern (obviously!)
        g = self._graph_original
        vprop_cost = g.new_vertex_property("int")
        vprop_gate = g.new_vertex_property("string")
        vprop_edge = g.new_vertex_property("int")
        g.vertex_properties["cost"] = vprop_cost
        g.vertex_properties["gate"] = vprop_gate
        g.vertex_properties["edge"] = vprop_edge
        vpc = g.vertex_properties["cost"]
        vpg = g.vertex_properties["gate"]
        vpe = g.vertex_properties["edge"]
        vpn = g.vertex_properties["name"]
        for v in g.vertices():
            if v.out_degree()==0:
                [vpc[v],vpg[v],vpe[v]]=[0,vpn[v],-1]
            else:
                [vpc[v],vpg[v],vpe[v]]=[0,"",-1]
        for v in self.sorted_list:
            if vpn[v]=='!' or vpn[v]=='NAND':
                self.optimal_pattern(v)

    def optimal_pattern(self,v):
        #Went to vertex v. It is guaranteed that all the inputs to this vertex were already called.
        # Algo.: check what? vertex with each pattern rooted at that vertex.
        g = self._graph_original
        vpn = g.vertex_properties["name"]
        vpl = g.vertex_properties["level"]
        vpc = g.vertex_properties["cost"]
        vpg = g.vertex_properties["gate"]
        vpe = g.vertex_properties["edge"]
        #for l in self.library_graphs:
        #    gl = l._graph_original
        #    vpnl = gl.vertex_properties["name"]
        #    vpll = gl.vertex_properties["level"]
        #    if vpn[v] == vpnl[l.sources[0]]: #the source vertex of the library graph
        #    #Got a top level match wtf to do now?
        #   
        costs=[]
        costs.append(self.find_3in_nand(v))
        costs.append(self.find_2in_nand(v))
        costs.append(self.find_not(v))
        for x in costs:
            if x[0]<0:
                costs.pop(costs.index(x))
        costs = sorted(costs,key=itemgetter(0))
        i=0
        #print costs
        while(True):
            try:
                if (costs[i][0]>0):
                    [vpc[v],vpg[v],vpe[v]] = costs[i]
                    break
                i=i+1
            except IndexError:
                pass

    def find_3in_nand(self,v):
        g = self._graph_original
        vpn = g.vertex_properties["name"]
        vpc = g.vertex_properties["cost"]
        vpg = g.vertex_properties["gate"]
        vpe = g.vertex_properties["edge"]
        if vpn[v]=='NAND':
            for nv in v.out_neighbours():
                if vpn[nv]=='!':
                    for nnv in nv.out_neighbours():
                        if vpn[nnv]=='NAND':
                            cost = 0
                            for nnnv in nnv.out_neighbours():
                                cost = vpc[nnnv]+cost
                                #print cost
                            for xv in v.out_neighbours():
                                if xv!=nv:
                                    #print xv,nv
                                    cost = cost + vpc[xv]
                                    #print cost
                            edge =  g.edge(v,nv)
                            return [cost+3,'3N',int(g.edge_index[edge])]
                            break
        return [None,"",-1]

    def find_2in_nand(self,v):
        g = self._graph_original
        vpn = g.vertex_properties["name"]
        vpc = g.vertex_properties["cost"]
        vpg = g.vertex_properties["gate"]
        vpe = g.vertex_properties["edge"]
        if vpn[v] == 'NAND':
            cost = 0
            for nv in v.out_neighbours():
                cost = vpc[nv]+cost
            edge = None
            return [cost+2,'2N',-1]
        else:
            return [-1,"",-1]

    def find_not(self,v):
        g = self._graph_original
        vpn = g.vertex_properties["name"]
        vpc = g.vertex_properties["cost"]
        vpg = g.vertex_properties["gate"]
        vpe = g.vertex_properties["edge"]
        if vpn[v] == '!':
            cost = 0
            for nv in v.out_neighbours():
                cost = vpc[nv]+cost
            edge = None
            return [cost+1,'!',-1]
        else:
            return [-1,"",-1]

    def replace_optimal_vertices(self):
        g = self._graph_original
        vpn = g.vertex_properties["name"]
        vpc = g.vertex_properties["cost"]
        vpg = g.vertex_properties["gate"]
        vpe = g.vertex_properties["edge"]
        to_remove_vertices=[]
        self.sorted_list=reversed(self.sorted_list)
        n=0
        for v in self.sorted_list:
            if not v in to_remove_vertices:
                target_vertices=[]
                if vpg[v]=='3N':
                    for nv in v.out_neighbours():
                        if g.edge_index[g.edge(v,nv)] == vpe[v]:
                            to_remove_vertices.append(nv)
                            for nnv in nv.out_neighbours():
                                to_remove_vertices.append(nnv)
                                vpn[nnv]='remove'
                                vpn[nv]='remove'
                                vpn[v]='3N'
                                n=n+1
                                for nnnv in nnv.out_neighbours():
                                    target_vertices.append(nnnv)
                    for addv in target_vertices:
                        g.add_edge(v,addv)
        print "Replaced",n,"vertices with 3in nands"
        for v in to_remove_vertices:
            g.clear_vertex(v)
        k=1
        while(k==1):
            k=0
            for vertex in g.vertices():
                if g.vertex_properties["name"][vertex]=="remove":
                    g.remove_vertex(vertex)
                    k=1
                    break

    def load_library_functions(self):
        self.library_graphs=[]
        filenames=["not.xml","2nand.xml","3_in_nand.xml","4_in_nand.xml","2_in_nor.xml","3_in_nor.xml","4_in_nor.xml"]
        for f in filenames:
            lib_tm=TechMapping("library/"+f)
            lib_tm.ConvertInputToBaseGates()
            lib_tm.not_redundancy_removal()
            lib_tm.do_dfs()
            self.library_graphs.append(lib_tm)
        # lib_tm.load_library_functions() #The end of universe?
    # Load and save all the library graphs in the list library_graphs

    def finalAllocation(self):
         #To print the final allocation of the logic elements
         print "The final gate implementation of the logic circuit is :"

    def find_sources(self):
        g = self._graph_original
        vp = g.vertex_properties["name"]
        self.sources=[]
        for v in g.vertices():
            if v.in_degree() is 0:
                self.sources.append(v)
        #for v in self.sources:
            #print vp[v]
        return

if __name__=="__main__":
    #do something
    tm = TechMapping()
    tm.ConvertInputToBaseGates()
    tm.not_redundancy_removal()
    tm.do_dfs()
    #tm.load_library_functions()
    tm.find_optimal_pattern()
    tm.replace_optimal_vertices()
    graph_draw(tm._graph_original, vertex_fill_color="#729fcf", vertex_text=tm._graph_original.vertex_properties["name"], vertex_font_size=10, output_size=(2000,2000))
    tm.finalAllocation()
    print "ending"
