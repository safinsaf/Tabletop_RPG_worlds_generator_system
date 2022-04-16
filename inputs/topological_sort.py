from random import shuffle
class TopologicalSort():
    
    def topological_sort(self, graph):
        self.graph = graph
        visited = [False]*len(self.graph)
        stack = []

        self.order = [i for i in range(len(self.graph))]
        shuffle(self.order)

        for i in self.order:
            if visited[i] == False:
                self.topological_sort_util(i,visited,stack)
        return stack

    
    def topological_sort_util(self,v,visited,stack):
        visited[v] = True
 
        for i in self.order:
            if self.graph[v][i] > 0:
                if visited[i] == False:
                    self.topological_sort_util(i,visited,stack)
    
        stack.insert(0,v)

    def is_cyclic(self, graph):
        visited = [False] * (len(graph) + 1)
        rec_stack = [False] * (len(graph) + 1)
        for node in range(len(graph)):
            if visited[node] == False:
                if self.is_cyclic_util(node,visited,rec_stack,graph) == True:
                    return True
        return False

    def is_cyclic_util(self, v, visited, rec_stack, graph):

        visited[v] = True
        rec_stack[v] = True
 
        for i in range(len(graph[v])):
            if graph[v][i] > 0:
                if visited[i] == False:
                    if self.is_cyclic_util(i, visited, rec_stack, graph) == True:
                        return True
                elif rec_stack[i] == True:
                    return True
    
        rec_stack[v] = False
        return False
