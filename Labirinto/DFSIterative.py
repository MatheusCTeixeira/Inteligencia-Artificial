
from enum import Enum

import Graph
import Node

class DFS_algorithmcs:
    def __init__(self, list_action_function, execute_action_function,\
                       hash_function, cmp_function):
        self.list_action_function = list_action_function
        self.execute_action_function = execute_action_function
        self.hash_function = hash_function
        self.cmp_function = cmp_function

    #--------------------------------------------------------------------------

    #Find a solution from state_origin to state objective

    def DFS(self, state_origin, state_objective, lvl):
        #Create the graph
        #Prefer the node with lowest level
        graph = Graph.graph(self.hash_function, self.cmp_function,\
                            lambda new_node, old_node: new_node.level < old_node.level)

        #Create the first node
        node = Node.node(state_origin, "")

        #And add it to graph
        graph.append(node)

        #Initializes the border
        edge = [node]

        #First test
        if (self.cmp_function(state_origin, state_objective) == True):
            return self.trace_solution(node)


        while len(edge) > 0:
           
            #The most deep node
            node = edge.pop()

            actions = self.list_action_function(node.state)

            partial_edge = []

            for action in actions:
                #Create a new state
                new_state = self.execute_action_function(node.state, action)

                #Create a new node
                new_node = Node.node(new_state, action, node)

                #Verify if the state is new or not
                is_new_state = graph.append(new_node)

                #Add to edge
                if (new_node.level <  lvl and is_new_state == True):
                    partial_edge.insert(0, new_node)

                #Test solution
                if (self.cmp_function(new_state, state_objective) == True):                    
                    return self.trace_solution(new_node)

            
            edge.extend(partial_edge)       
            
        return []

    #--------------------------------------------------------------------------

    def trace_solution(self, node):
        solution = []
        temp_node = node

        while (temp_node != None):
            solution.insert(0, temp_node.action)
            temp_node = temp_node.parent

        return solution

    #--------------------------------------------------------------------------