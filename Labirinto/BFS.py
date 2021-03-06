import Graph
import Node
from collections import deque

class BFS_algorithmics:
    def __init__(self, list_action_function, execute_action_function,\
                       hash_function, cmp_function):
        self.list_action_function = list_action_function
        self.execute_action_function = execute_action_function
        self.hash_function = hash_function
        self.cmp_function = cmp_function


    def trace_solution(self, state_objective):
        solution = []
        for node in self.graph.graphs[len(self.graph.graphs) - 1]:
            if self.cmp_function(node.state, state_objective) == True:                
                solution.append(node)
        
        if len(solution) > 0:
            while (solution[0].parent != None):
                solution.insert(0, solution[0].parent)

        return solution



    def BFS(self, state_origin, state_objective):
        self.graph = Graph.graph(self.hash_function, self.cmp_function)

        node = Node.node(state_origin, "$")
        self.graph.append(node)
        edge = [node]

        solution_found = self.cmp_function(state_origin, state_objective)

        while (len(edge) > 0 and solution_found == False):
            currentNode = edge.pop()         

            actions = self.list_action_function(currentNode.state)

            for action in actions:
                # Create a new state from currentNode.state + action
                state = self.execute_action_function(currentNode.state, action)
                
                # Create a new node from state
                new_node = Node.node(state, action, currentNode)

                # Add the node to graph
                is_new_state = self.graph.append(new_node)

                # Add the node to edge
                if (is_new_state == True):
                    edge.insert(0, new_node)

                solution_found = solution_found or self.cmp_function(state, state_objective)
                
        
        return self.trace_solution(state_objective)
