import re
import sys
import collections
import networkx as nx
import matplotlib.pyplot as plt
import random
import copy
def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        sys.exit(1)

def preprocess_text(text):
    # 将换行符和标点符号替换为空格，并转换为小写
    text = re.sub(r'[^\w\s]', ' ', text)
    text = text.replace('\n', ' ').lower()
    # 分割成单词列表
    words = text.split()
    return words

class Graph():
    words = []
    maps = []
    nodes = []
    graph = []

    def __init__(self, words):
        self.words = words
        self.size = 0
        self.build_node_map()
        self.init_graph()
        self.build_graph()

    def build_node_map(self):
        for i in range(len(self.words)):
            if len(self.nodes) == 0:
                self.nodes.append(self.words[i])
                self.maps.append(0)
            else:
                flag = 0
                for j in range(len(self.nodes)):
                    if self.nodes[j] == self.words[i]:
                        self.maps.append(j)
                        flag = 1
                if flag == 0:
                    self.nodes.append(self.words[i])
                    self.maps.append(len(self.nodes) - 1)
        self.size = len(self.nodes)

    def init_graph(self):
        for i in range(self.size):
            temp = []
            for j in range(self.size):
                temp.append(0)
            self.graph.append(temp)

    def build_graph(self):
        for i in range(len(self.maps) - 1):
            word1, word2 = self.maps[i], self.maps[i + 1]
            if word1 != word2:
                self.graph[word1][word2] += 1

    def find_bridge_word(self, word1, word2, gen = False):
        flag1 = 0
        for i in range(self.size):
            if self.nodes[i] == word1:
                map1 = i
                flag1 = 1
        flag2 = 0
        for j in range(self.size):
            if self.nodes[j] == word2:
                map2 = j
                flag2 = 1
        if flag1 == 0 and flag2 == 0:
            if gen == False:
                print(f"No \"{word1}\" and \"{word2}\" in the graph!")
            return
        elif flag1 == 0 and flag2 == 1:
            if gen == False:
                print(f"No \"{word1}\" in the graph!")
            return
        elif flag1 == 1 and flag2 == 0:
            if gen == False:
                print(f"No \"{word2}\" in the graph!")
            return
        bridge_words = []
        for i in range(len(self.graph[map1])):
            if self.graph[map1][i] >= 1 and self.graph[i][map2] >= 1:
                bridge_words.append(self.nodes[i])
        len_of_bridge_words = len(bridge_words)
        if gen == False:
            if len_of_bridge_words >= 3:
                print(f"The bridge words from \"{word1}\" to \"{word2}\" are:{', '.join(bridge_words[:-2])}, {bridge_words[-2]} and {bridge_words[-1]}")
            elif len_of_bridge_words == 2:
                print(f"The bridge words from \"{word1}\" to \"{word2}\" are: {bridge_words[-2]} and {bridge_words[-1]}")
            elif len_of_bridge_words == 1:
                print(f"The bridge word from \"{word1}\" to \"{word2}\" is: {bridge_words[0]}")
            else:
                print(f"No bridge words from \"{word1}\" to \"{word2}\"!")
        return bridge_words

    def generateNewText(self,newwords):
        result_words=[]
        result_words.append(newwords[0])
        for i in range(len(newwords)-1):
            bridge_words = self.find_bridge_word(newwords[i], newwords[i+1], True)
            if bridge_words:
                len_of_bridge_words = len(bridge_words)
                if len_of_bridge_words == 1:
                    result_words.append(bridge_words[0])
                elif len_of_bridge_words > 1:
                    result_words.append(bridge_words[random.randint(0,len_of_bridge_words-1)])#random
            result_words.append(newwords[i+1])
        print(f"{' '.join(result_words)}")
        return
    
    def map(self, word2):
        if word2 != None:
            flag = 0
            for j in range(self.size):
                if self.nodes[j] == word2:
                    map2 = j
                    flag = 1
            if flag == 0:
                print("Word2 Not Found")
                return
            return map2
        else:
            return None
    
    def find_shortest_path(self, word1, word2 = None, info = True):
        map1 = self.map(word1)
        map2 = self.map(word2)
        local_graph = copy.deepcopy(self.graph)
        Array = []
        d = []
        path = []
        for j in range(self.size):
            path.append([map1])
            d.append(0)
        d[map1] = 1
        Array = local_graph[map1]
        for j in range(self.size):
            shortest = -1
            for i in range(self.size):
                if Array[i]!=0:
                    if (Array[i]<Array[shortest]  or shortest == -1)and not d[i]:
                        shortest = i
            if shortest == -1:
                break
            d[shortest] = 1
            temp = local_graph[shortest]
            for i in range(self.size):
                if temp[i] != 0 and not d[i]:
                    if Array[i] > Array[shortest] + temp[i] or Array[i] == 0:
                        Array[i] = Array[shortest] + temp[i]
                        path[i].append(shortest)
        if word2 != None:
            pathwords = []
            i = map2
            real_path_words = []
            path_map = []
            path_map.append(map2)
            real_path_map = []
            while len(path[i]) == 2:
                pathwords.append(self.nodes[path[i][1]])
                path_map.append(path[i][1])
                i = path[i][1]
            path_map.append(map1)
            for i in range(len(pathwords)):
                real_path_words.append(pathwords[len(pathwords) - i -1])
            for i in range(len(path_map)):
                real_path_map.append(path_map[len(path_map) - i -1])
            if Array[map2] != 0 and info == True:
                print(f"Shortest path from \"{word1}\" to \"{word2}\":")
                if len(real_path_words) >= 1:
                    print(f"{word1}->{'->'.join(real_path_words)}->{word2}")
                elif len(real_path_words) == 0:
                    print(f"{word1}->{word2}")
                print("The length is:" + str(Array[map2]))
                self.draw_graph(real_path_map,"path.png")
            elif info == True:
                print("no path from word1 to word2")
            return Array[map2]
        else:
            for j in range(self.size):
                if j != map1:
                    pathwords = []
                    real_path_words = []
                    des = j
                    while len(path[des]) == 2:
                        pathwords.append(self.nodes[path[des][1]])
                        des = path[des][1]
                    for i in range(len(pathwords)):
                        real_path_words.append(pathwords[len(pathwords) - i -1])
                    if Array[j] != 0 and info == True:
                        print(f"Shortest path from \"{word1}\" to \"{self.nodes[j]}\":")
                        if len(real_path_words) >= 1:
                            print(f"{word1}->{'->'.join(real_path_words)}->{self.nodes[j]}")
                        elif len(real_path_words) == 0:
                            print(f"{word1}->{self.nodes[j]}")
                        print("The length is:" + str(Array[j]))
                    elif info == True:
                        print("no path from word1 to word2")
    
    def all_shortest(self, word1, word2):
        map1= self.map(word1)
        map2= self.map(word2)
        local_graph = copy.deepcopy(self.graph)
        shortest_paths = []
        shortest_length = self.find_shortest_path(word1, word2, False)
        if shortest_length == 0:
            return
        visited = [False] * self.size
        path = [map1]
        def dfs(current, end, path, visited):
            if current == end:
                if len(path) - 1 == shortest_length:
                    shortest_paths.append(path[:])
                return
            visited[current] = True
            for neighbor, weight in enumerate(local_graph[current]):
                if weight > 0 and not visited[neighbor]:
                    path.append(neighbor)
                    dfs(neighbor, end, path, visited)
                    path.pop()
            visited[current] = False

        dfs(map1, map2, path, visited)
        pathwords = []
        for shortest_path in shortest_paths:
            pathword = []
            for item in shortest_path:
                pathword.append(self.nodes[item])
            print("one of the shortest path:")
            print(pathword)
            pathwords.append(pathword)
        #print(shortest_paths)
        return shortest_paths


    def random_walk(self):
        start = random.randint(0,self.size-1)
        path = []
        temp = self.graph[start]
        current = start
        real_path = []
        while 1:
            recode = []
            for i in range(self.size):
                if temp[i] >= 1 and (current,i) not in path:
                    recode.append(i)
            if recode:
                p = random.randint(0,len(recode)-1)
                path.append((current,recode[p]))
                current = recode[p]
                temp = self.graph[recode[p]]
            else:
                break
        for i in range(len(path)):
            if i == 0:
                real_path.append(self.nodes[path[i][0]])
            real_path.append(self.nodes[path[i][1]])
        print("Random walk:")
        if real_path:
            print(f"{'->'.join(real_path)}")
        else:
            print(f"Random walk selects a dead node:{start}")

    def draw_graph(self, highlight_path=None, save_path=None):
        G = nx.DiGraph()
        for i in range(self.size):
            G.add_node(self.nodes[i]) 
        for i in range(self.size):
            for j in range(self.size):
                if self.graph[i][j] > 0:
                    G.add_edge(self.nodes[i], self.nodes[j], weight=self.graph[i][j])
        pos = {node: (index, 0) for index, node in enumerate(self.nodes)}
        plt.figure(figsize=(18, 12))
        nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=12, font_color="black", font_weight="bold", edge_color="gray", arrowsize=20, connectionstyle="arc3,rad=0.2")
        edge_labels = {(self.nodes[i], self.nodes[j]): self.graph[i][j] for i in range(len(self.graph)) for j in range(self.size) if self.graph[i][j] > 0}
        for (n1, n2), label in edge_labels.items():
            x1, y1 = pos[n1]
            x2, y2 = pos[n2]
            x_label = (x1 + x2) / 2
            sig = 1 if (x1 > x2) else -1
            x_diff = abs(x1 -x2) ** 0.75
            y_label = sig * ((y1 + y2) / 2 + 0.1 * x_diff)  # Adjust y_label dynamically based on x_diff
            plt.text(x_label, y_label, label, fontsize=10, ha='center', va='center', color='red')
        if highlight_path:
            edges = [(self.nodes[highlight_path[i]], self.nodes[highlight_path[i+1]]) for i in range(len(highlight_path)-1)]
            nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='red', width=2.5, arrows=True, arrowsize=20, connectionstyle="arc3,rad=0.2")
        plt.title("Directed Graph")
        if save_path:
            plt.savefig(save_path)
            print(f"Graph saved as {save_path}")
        plt.show()

def main(file_path):
    text = read_text_file(file_path)
    words = preprocess_text(text)
    dgraph = Graph(words)
    while True:
        print()
        print("Please select a number to execute a command:")
        print("1. Draw picture")
        print("2. Find bridge")
        print("3. Renew text")
        print("4. Find shortest path")
        print("5. Random walk")
        print("6. All shortest path")
        print("7. Exit")
        command = input("Please input the number of the command you want to execute: ").lower()
        
        if command == '1':
            dgraph.draw_graph(save_path="pic.png")
        elif command == '2':
            word1 = input("Enter the first word (or 'exit' to quit): ").lower()
            if word1 != 'exit':
                word2 = input("Enter the second word: ").lower()
                dgraph.find_bridge_word(word1, word2)        
        elif command == '3':
            ''''
            path = input("Enter the path to new txt (or 'exit' to quit): ").lower()
            if path != 'exit':
                temp_txt = read_text_file(path)
                temp_words = preprocess_text(temp_txt)
                dgraph.generateNewText(temp_words)
            '''
            txt = input("Please enter your text: ")
            if txt:
                temp_words = preprocess_text(txt)
                dgraph.generateNewText(temp_words)
        elif command == '4':
            word1 = input("Enter the first word (or 'exit' to quit): ").lower()
            if word1 != 'exit':
                word2 = input("Enter the second word(if there is no second word please input 0): ").lower()
                if word2 != '0': 
                    dgraph.find_shortest_path(word1, word2)
                else:
                    dgraph.find_shortest_path(word1)
        elif command == '5':
            dgraph.random_walk()
        elif command == '6':
            word1 = input("Enter the first word (or 'exit' to quit): ").lower()
            if word1 != 'exit':
                word2 = input("Enter the second word (or 'exit' to quit): ").lower()
                if word2 != 'exit':
                    dgraph.all_shortest(word1, word2)
        elif command == '7':
            break
        else:
            print("Invalid command, please try again.")
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
    else:
        file_path = sys.argv[1]
        main(file_path)
        
