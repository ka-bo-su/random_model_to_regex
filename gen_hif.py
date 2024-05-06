"""
model_gen.py ver.1.0.

Copyright 2024 Kazuma Ikesaka.
All rights reserved.
"""

import random
import sys
from time import sleep
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.setrecursionlimit(10000)

config = {
        "node_type":{
            "action":3,
            "bin_operation":6,
            "un_operation":2
        },
        "bin_operation":{
            "seq":10,
            "strict":1,
            "par":2,
            "alt":2
        },
        "un_operation":{
            "loopS":2
        },
        "life_line":{
            "l1":100,
            "l2":100,
            "l3":100,
            "l4":1,
            "l5":1,
        },
        "message":{
            "m1":100,
            "m2":100,
            "m3":100,
            "m4":1,
            "m5":1,
        }
    }

BIN_OPERATION = ["seq", "strict", "par", "alt"]
UN_OPERATION = ["loopS"]

depth = 7

class node :
    def __init__(self):
        global config
        self.is_action = False
        self.is_bin_operation = False
        self.is_un_operation = False
        self.action = ""
        self.bin_operation = ""
        self.un_operation = ""
        self.next_node1 = None
        self.next_node2 = None
        self.depth = 1
        self.select = select()

    def __str__(self):
        tab = ""
        for i in range(self.depth-1):
            tab += "    "
        
        if self.is_action:
            return tab + self.action
        elif self.is_bin_operation:
            return tab +self.bin_operation + "(\n" +str(self.next_node1)+ ",\n" + str(self.next_node2) + "\n" + tab +")"
        elif self.is_un_operation:
            return tab +self.un_operation + "(\n" + tab +str(self.next_node1) + "\n" + tab +")"

    def add_node(self, node_type, node_info):
        if node_type == "action":
            self.is_action = True
            self.action = node_info
        elif node_type == "bin_operation":
            self.is_bin_operation = True
            self.bin_operation = node_info
            self.next_node1 = node()
            self.next_node1.depth = self.depth + 1
            self.next_node2 = node()
            self.next_node2.depth = self.depth + 1
        elif node_type == "un_operation":
            self.is_un_operation = True
            self.un_operation = node_info
            self.next_node1 = node()
            self.next_node1.depth = self.depth + 1

    def add_random_node(self, max_depth):
        node_type = select.node_type(self)
        if node_type == "action" or max_depth == self.depth:
            node_type = "action"
            node_info_lifeline_from = select.life_line(self)
            while True:
                node_info_lifeline_to = select.life_line(self)
                if node_info_lifeline_from != node_info_lifeline_to:
                    break
            node_info_message = select.message(self)
            node_info = node_info_lifeline_from + " -- " + node_info_message + " ->" + node_info_lifeline_to
            self.add_node(node_type, node_info)
        elif node_type == "bin_operation":
            node_info = select.bin_operation(self)
            self.add_node(node_type, node_info)
            self.next_node1.add_random_node(max_depth - 1)
            self.next_node2.add_random_node(max_depth - 1)
        elif node_type == "un_operation":
            node_info = select.un_operation(self)
            self.add_node(node_type, node_info)
            self.next_node1.add_random_node(max_depth - 1)

    def gen_random_tree(self, max_depth):
        if max_depth == 0:
            print("max_depth is 0")
            return None
        else:
            self.add_random_node(max_depth)

class select:
    def __init__(self):
        global config
        self.config = config

    def node_type(self):
        tmp_action = config["node_type"]["action"]
        tmp_bin_operation = config["node_type"]["bin_operation"]
        tmp_un_operation = config["node_type"]["un_operation"]
        tmp = tmp_action + tmp_bin_operation + tmp_un_operation
        random_number = random.randint(1,tmp)
        if random_number <= tmp_action:
            return "action"
        elif random_number <= tmp_action + tmp_bin_operation:
            return "bin_operation"
        else:
            return "un_operation"
        
    def bin_operation(self):
        tmp_seq = config["bin_operation"]["seq"]
        tmp_strict = config["bin_operation"]["strict"]
        tmp_par = config["bin_operation"]["par"]
        tmp_alt = config["bin_operation"]["alt"]
        tmp = tmp_seq + tmp_strict + tmp_par + tmp_alt
        random_number = random.randint(1,tmp)
        if random_number <= tmp_seq:
            return "seq"
        elif random_number <= tmp_seq + tmp_strict:
            return "strict"
        elif random_number <= tmp_seq + tmp_strict + tmp_par:
            return "par"
        else:
            return "alt"
        
    def un_operation(self):
        tmp_loopS = config["un_operation"]["loopS"]
        tmp = tmp_loopS
        random_number = random.randint(1,tmp)
        if random_number <= tmp_loopS:
            return "loopS"
        
    def life_line(self):
        tmp_arr = []
        key_arr = list(config["life_line"].keys())
        sum = 0
        for key in key_arr:
            tmp_arr.append(config["life_line"][key])
            sum += config["life_line"][key]
        random_number = random.randint(1,sum)
        tmp_sum = 0
        for key in key_arr:
            tmp_sum += config["life_line"][key]
            if random_number <= tmp_sum:
                return key
        
    def message(self):
        tmp_arr = []
        key_arr = list(config["message"].keys())
        sum = 0
        for key in key_arr:
            tmp_arr.append(config["message"][key])
            sum += config["message"][key]
        random_number = random.randint(1,sum)
        tmp_sum = 0
        for key in key_arr:
            tmp_sum += config["message"][key]
            if random_number <= tmp_sum:
                return key

def gen_random_hif(file_name = "hibou_para.hif"):
    nodeA = node()
    nodeA.gen_random_tree(depth)
    f = open(file_name, 'w',encoding='UTF-8')
    f.write(nodeA.__str__())

if __name__ == "__main__":
    gen_random_hif()