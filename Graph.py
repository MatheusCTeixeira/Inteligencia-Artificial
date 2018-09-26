
import Node
import random

def cmp_default(st1, st2):
    return st1 == st2

def hash_function_default(st):
    return 0

class graph:
    graphs = []
    hash_table = {}
    repeated_state = 0

    def __init__(self, hash_function = hash_function_default, cmp_function = cmp_default):
        self.reset()
        self.hash_function = hash_function
        self.cmp_function = cmp_function

    def reset(self):
        self.graphs.clear()
        self.hash_table.clear()
        self.repeated_state = 0

    def append(self, node):
        hash_value = self.hash_function(node.state)
        
        # Verify if the state is a repeated state
        if (self.state_exists(node, True) == True):
            return False

        # Add a new hash if necessary
        if (self.hash_table.get(hash_value, None) == None):            
            entry = {hash_value: []}
            self.hash_table.update(entry) 
        
        # Add new hash value
        self.hash_table[hash_value].append(node)       
        
        # Add a node in a specific level
        while (len(self.graphs) < node.level + 1):
            self.graphs.append([])
              
        self.graphs[node.level].append(node)
  
        return True

    def status(self):
        print("@graph levels: "    + str(len(self.graphs))        + "\n" + \
              "@hash entrys: "     + str(len(self.hash_table))    + "\n" + \
              "@banch factor: "    + str(self.branching_factor()) + "\n" + \
              "@repeated states: " + str(self.repeated_state)     + "\n" ) 

    def branching_factor(self):        
        childrens_max = []

        for level in self.graphs:
            if len(level) > 0:
                childrens_max.append(max([len(node.childrens) for node in level]))
        if len(childrens_max) > 0:
            return max(childrens_max)
        else:
            return 0

    def state_exists(self, node, stat = False):  
        state = node.state 
        hash_value = self.hash_function(state)     
        node_list = self.hash_table.get(hash_value, None)
        
        if node_list == None:
            return False
        
        for some_node in node_list:
            if self.cmp_function(some_node.state, state) == True: 
                #If there some collision, remove the node most depth
                if (node.level < some_node.level):
                    self.hash_table[hash_value].remove(some_node)
                    return False

                if (stat == True):
                    self.repeated_state = self.repeated_state + 1               
                
                return True

        return False   
            


#def my_hash(st):
#    return st % 100
#
#graph1 = graph(hash_function=my_hash)
#
#node1 = Node.node(100, "<-")
#graph1.append(node1)
#
#fathers = [node1]
#
#
#for i in range(0, 1000):    
#    for k in range(0, 1000):
#        val = int( random.random()*(len(fathers) - 1) )
#        state = int(random.random() * 5000)
#        no = Node.node(state, "-<", fathers[val])
#        fathers.append(no)
#        graph1.append( no )
#
#graph1.status()
#
#for a in graph1.hash_table:
#    print(len(graph1.hash_table[a]))    
#
#print("---------------------------------------------")
#
#for i in range(4995, 5005):
#    print(graph1.state_exists(i))
#        