from random import shuffle
class TopologicalSort():
    
    def topological_sort(self, graph, type):
        
        cc = self.find_connected_components(graph)
        order = [i for i in range(len(cc))]
        shuffle(order)

        cc_copy = []
        for i in range(len(order)):
            cc_copy.append(cc[order[i]])
        cc = cc_copy


        graph = self.merge_graph(cc, graph)
        assert not self.is_cyclic(graph), "There is cycle in " + type

        visited = [False]*len(cc)
        stack = []

        for i in range(len(graph)):
            if visited[i] == False:
                self.topological_sort_util(i,visited,stack,graph)

        return [cc, stack]


    def topological_sort_util(self,v,visited,stack, graph):
        visited[v] = True
 
        for i in range(len(graph)):
            if graph[v][i] == 1:
                if visited[i] == False:
                    self.topological_sort_util(i,visited,stack, graph)    
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
            if graph[v][i] == 1:
                if visited[i] == False:
                    if self.is_cyclic_util(i, visited, rec_stack, graph) == True:
                        return True
                elif rec_stack[i] == True:
                    return True
    
        rec_stack[v] = False
        return False


    def merge_graph(self, cc, graph):
        new_graph = [[0 for j in range(len(cc))] for i in range(len(cc))]
        
        for i in range(len(new_graph)):
            for j in range(len(new_graph)):
                prev_vertices_from = cc[i]
                prev_vertices_to = cc[j]

                #print(prev_vertices_from, prev_vertices_to)
                for x in prev_vertices_from:
                    for y in prev_vertices_to:
                        if graph[x][y] == 1:
                            new_graph[i][j] = 1

        return new_graph

    def find_connected_components(self, graph):
        visited = [False] * len(graph)
        cc = []
        for v in range(len(graph)):
            if visited[v] == False:
                temp = []
                cc.append(self.find_connected_components_util(temp, v, visited, graph))
        return cc

    def find_connected_components_util(self, temp, v, visited, graph):
 
        visited[v] = True
        temp.append(v)
 
        for i in range(len(graph[v])):
            if graph[v][i] != 2:
                continue
            if visited[i] == False:
 
                temp = self.find_connected_components_util(temp, i, visited, graph)
        return temp

