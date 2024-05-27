import re
import sys
import collections
#import networkx as nx
import matplotlib.pyplot as plt

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

    def init_graph(self):
        size = len(self.nodes)
        for i in range(size):
            temp = []
            for j in range(size):
                temp.append(0)
            self.graph.append(temp)

    def build_graph(self):
        print(self.maps)
        print(len(self.nodes))
        for i in range(len(self.maps) - 1):
            word1, word2 = self.maps[i], self.maps[i + 1]
            print(word1)
            print(word2)
            print(len(self.graph[word1]))
            print( )
            self.graph[word1][word2] += 1
    '''
    def display_graph(self):
        pos = nx.spring_layout(graph)
        edge_labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw(graph, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=12, font_weight='bold')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
        plt.show()
    '''

    def find_bridge_word(self, word1, word2):
        flag = 0
        for i in range(len(self.nodes)):
            if self.nodes[i] == word1:
                map1 = i
                flag = 1
        if flag == 0:
            print("Word1 Not Found")
            return
        flag = 0
        for j in range(len(self.nodes)):
            if self.nodes[j] == word2:
                map2 = j
                flag = 1
        if flag == 0:
            print("Word1 Not Found")
            return
        bridge_words = []
        for i in range(len(self.graph[map1])):
            if self.graph[map1][i] >= 1 and self.graph[i][map2] >= 1:
                bridge_words.append(self.nodes[i])
        return bridge_words

    def generateNewText(self,newwords):
        result_words=[]
        for i in range(len(newwords)):
            if i == 0:
                result_words.append(newwords[0])
            else:
                bridge_words = self.find_bridge_word(newwords[i-1],newwords[i])
                if len(bridge_words) == 1:
                    result_words.append(bridge_words[0])
                elif len(bridge_words) > 1:
                    result_words.append(bridge_words[0])#random
                result_words.append(newwords[i])
        return result_words


def main(file_path):
    text = read_text_file(file_path)
    words = preprocess_text(text)
    dgraph = Graph(words)
    #display_graph(graph)
    
    while True:
        word1 = input("Enter the first word (or 'exit' to quit): ").lower()
        if word1 == 'exit':
            break
        word2 = input("Enter the second word: ").lower()
        bridge_words = dgraph.find_bridge_word(word1, word2)
        if bridge_words:
            print(f"Bridge words between '{word1}' and '{word2}': {', '.join(bridge_words)}")
        else:
            print(f"No bridge words found between '{word1}' and '{word2}'.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
    else:
        file_path = sys.argv[1]
        main(file_path)
        
