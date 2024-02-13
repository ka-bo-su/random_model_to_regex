import re
import graphviz
import random
from time import sleep

class node:
    def __init__(self, name, is_start=False, is_end=False):
        self.is_start = is_start
        self.is_end = is_end
        self.name = name
        self.childlen = []
        self.parent = []

    def __str__(self):
        return f"Name : {self.name}"

    def __repr__(self):
        return f"Name : {self.name}"

    def __eq__(self, other):
        return self.name == other.name

    def remove(self):
        if self.is_start or self.is_end:
            print("Can't remove start node or end node")
        else:
            for parent in self.parent:
                parent.childlen.remove(self)
            for child in self.childlen:
                child.parent.remove(self)


class edge:
    def __init__(self, start, end, label):
        self.start = start
        self.end = end
        self.label = label

    def __str__(self):
        return f"Node {self.start} -- {self.label} -> Node {self.end}"

    def __repr__(self):
        return f"Node {self.start} -- {self.label} -> Node {self.end}"

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end


class graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def print_nodes(self):
        print("Node list")
        for node in self.nodes:
            if node.is_start:
                print(f"{node} <---- Start")
            elif node.is_end:
                print(f"{node} <---- End")
            else:
                print(node)

    def print_edges(self):
        print("Edge list")
        for edge in self.edges:
            print(edge)

    def print_graph(self):
        self.print_nodes()
        self.print_edges()

    def add_node(self, name, is_start=False, is_end=False):
        self.nodes.append(node(name, is_start, is_end))

    def remove_node(self, node):
        if node.is_start or node.is_end:
            print("Can't remove start or end node")
        else:
            node_to_node = self.pop_edge_label(node.name, node.name)
            if node_to_node != "":
                node_to_node = f"{node_to_node}*"
            for i in range(len(node.parent)):
                if node.parent[i] != node:
                    new_edge_label = node_to_node
                    parent_to_node = self.pop_edge_label(node.parent[i].name, node.name)
                    if parent_to_node != "":
                        new_edge_label = f"{parent_to_node}{new_edge_label}"
                    for j in range(len(node.childlen)):
                        if node.childlen[j] != node:
                            node_to_child = self.pop_edge_label(node.name, node.childlen[j].name)
                            new_edge_label = f"{new_edge_label}{node_to_child}"
                            parent_to_child = self.pop_edge_label(node.parent[i].name, node.childlen[j].name)
                            if parent_to_child != "" and not node.parent[i].is_start:
                                new_edge_label = f"({new_edge_label}|{parent_to_child})"
                            self.add_edge(node.parent[i].name, node.childlen[j].name, new_edge_label)
                            if node.childlen[j] not in node.parent[i].childlen:
                                node.parent[i].childlen.append(node.childlen[j])
                            if node.parent[i] not in node.childlen[j].parent:
                                node.childlen[j].parent.append(node.parent[i])
            node.remove()
            # self.draw_graph("a")
            # sleep(2)

    def pop_edge_label(self, start, end):
        for i in range(len(self.edges)):
            if self.edges[i].start == start and self.edges[i].end == end:
                edge = self.edges.pop(i)
                return edge.label
        return ""

    def get_edge_label(self, start, end):
        for edge in self.edges:
            if edge.start == start and edge.end == end:
                return edge.label
        return ""

    def add_edge(self, start, end, label):
        if len(self.edges) > 1:
            for i in range(len(self.edges)):
                if self.edges[i].start == start and self.edges[i].end == end:
                    tmp = [self.edges[i].label, label]
                    tmp.sort()
                    self.edges[i].label = f"({tmp[0]}|{tmp[1]})"
                    return
        if label == "":
            self.edges.append(edge(start, end, label))
        else:
            self.edges.append(edge(start, end, f"{label}"))

    def add_content_from_dot_file(self, file_path="secret_code_orig_nfa.dot"):
        with open(file_path, "r") as f:
            tmp = f.read()
            tmp = (
                tmp.replace(" ", "")
                .replace("\t", "")
                .replace(";", "")
                .replace("{", "")
                .replace("\n}", "")
                .replace("[", "")
                .replace("]", "")
                .replace('"', "")
                .replace("!", "\!")
                .replace("?", "\?")
            )
            tmp = tmp.split("\n")[2:]
            for content in tmp:
                content = re.split(r"shape=|,label=|label=", content)
                if "->" not in content[0]:
                    if content[1] == "point":
                        self.add_node(content[0], True, False)
                    elif content[1] == "doublecircle":
                        self.add_node(content[0], False, True)
                    else:
                        self.add_node(content[0])
                else:
                    start = content[0].split("->")[0]
                    end = content[0].split("->")[1]
                    if len(content) < 2:
                        label = ""
                    else:
                        label = "("+content[1]+")"
                    self.add_edge(start, end, label)
                    for i in range(len(self.nodes)):
                        if self.nodes[i].name == start:
                            start_node = self.nodes[i]
                        if self.nodes[i].name == end:
                            end_node = self.nodes[i]
                    if end_node not in start_node.childlen:
                        start_node.childlen.append(end_node)
                    if start_node not in end_node.parent:
                        end_node.parent.append(start_node)
            self.add_node("accept", False, True)
            for i in range(len(self.nodes)):
                if self.nodes[i].is_end and self.nodes[i].name != "accept":
                    self.add_edge(self.nodes[i].name, "accept", "")
                    self.nodes[i].is_end = False
                    self.nodes[i].childlen.append(self.nodes[-1])
                    self.nodes[-1].parent.append(self.nodes[i])

    def draw_graph(self, file_path="nfa_graph"):
        dot = graphviz.Digraph(format="png")
        for node in self.nodes:
            if node.is_start:
                dot.node(node.name, node.name, shape="point")
            elif node.is_end:
                dot.node(node.name, node.name, shape="doublecircle")
            else:
                dot.node(node.name, node.name)
        for edge in self.edges:
            dot.edge(edge.start, edge.end, label=edge.label)
        dot.render(file_path)

    def get_regular_expression(self):
        start_childlen_end_parent_num = 0
        for i in range(len(self.nodes)):
            if self.nodes[i].is_start:
                start_childlen_end_parent_num += len(self.nodes[i].childlen)
            if self.nodes[i].is_end:
                start_childlen_end_parent_num += len(self.nodes[i].parent)
        while len(self.nodes) > 2 + start_childlen_end_parent_num:
            # i = random.randint(0, len(self.nodes) - 1)
            edge_num = -1
            for i in range(len(self.nodes)):
                flg = True
                tmp_list = [len(self.nodes[i].childlen), len(self.nodes[i].parent)]
                min_tmp = min(tmp_list)
                if edge_num == -1 or min_tmp < edge_num:
                    if not self.nodes[i].is_start and not self.nodes[i].is_end:
                        for j in range(len(self.nodes[i].parent)):
                            if self.nodes[i].parent[j].is_start:
                                flg = False
                                break
                        for j in range(len(self.nodes[i].childlen)):
                            if self.nodes[i].childlen[j].is_end:
                                flg = False
                                break
                        if flg:
                            edge_num = min_tmp
                            self.remove_node(self.nodes.pop(i))
                            break
        while len(self.nodes) > 2:
            # i = random.randint(0, len(self.nodes) - 1)
            edge_num = -1
            tmp = -1
            for i in range(len(self.nodes)):
                 tmp_list = [len(self.nodes[i].childlen), len(self.nodes[i].parent)]
                 min_tmp = min(tmp_list)
                 if edge_num == -1 or min_tmp < edge_num:
                    if not self.nodes[i].is_start and not self.nodes[i].is_end:
                        edge_num = min_tmp
                        self.remove_node(self.nodes.pop(i))
                        break
            # if not self.nodes[i].is_start and not self.nodes[i].is_end:
                # self.remove_node(self.nodes.pop(i))
        return self.get_edge_label(self.nodes[0].name, self.nodes[1].name)


def main():
    nft_gp = graph()
    nft_gp.add_content_from_dot_file()
    nft_gp.print_graph()
    nft_gp.draw_graph()
    for i in range(len(nft_gp.edges)):
        print(nft_gp.edges[i])
    regex = nft_gp.get_regular_expression()
    print(regex)
    # nft_gp.print_graph()


if __name__ == "__main__":
    main()