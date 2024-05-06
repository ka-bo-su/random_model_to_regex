"""
model_gen_rev.py ver.1.0.

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

M_ENV = []
M_BROADCAST = []
M_PAIR = []
M_ALL = []
MAX_DEPTH = 4

class conf:
    def __init__(self) -> None:        
        self.config_replace_holl = {
            "seq": 1,
            "strict": 0,
            "par": 0,
            "alt": 0,
            "loopS": 1,
            "hole": 1,
            "sum": 0
            }
        for key in self.config_replace_holl.keys():
            if key != "sum":
                self.config_replace_holl["sum"] += self.config_replace_holl[key]

        self.config_message = {
            "pair":10,
            "env":3,
            "broadcast":1,
            "sum": 0
        }
        for key in self.config_message.keys():
            if key != "sum":
                self.config_message["sum"] += self.config_message[key]

        self.lifeline_num = 3

class node :
    def __init__(self, depth = 0):
        global MAX_DEPTH
        self.depth = depth
        if depth >= MAX_DEPTH:
            self.is_leaf = True
        else:
            self.is_leaf = False
        self.is_hole = True
        self.name = ""
        self.is_in_loopS = False
        self.child = []

    def __str__(self):
        tab = ""
        for i in range(self.depth):
            tab += "    "
        
        if len(self.child) == 0:
            return tab + self.name
        elif len(self.child) == 1:
            return tab +self.name + "(\n" + tab +str(self.child[0]) + "\n" + tab +")"
        else:
            return tab +self.name + "(\n" +str(self.child[0])+ ",\n" + str(self.child[1]) + "\n" + tab +")"


    def replace_hole(self):
        config = conf()
        # if self.depth==0:
        #     self.name = "strict"
        #     self.is_hole = False
        #     self.child.append(node(self.depth+1))
        #     self.child.append(node(self.depth+1))
        #     for child in self.child:
        #         child.replace_hole()
        #     return
        if self.is_hole and not self.is_leaf:
            while True:
                rand_int = random.randint(0, self.depth)
                if rand_int > 2:
                    self.is_leaf = True
                    return
                else:
                    rand_int = random.randint(0,config.config_replace_holl["sum"])
                    threshold = config.config_replace_holl["seq"]
                    if rand_int < threshold:
                        self.name = "seq"
                        self.is_hole = False
                        self.child.append(node(self.depth+1))
                        self.child.append(node(self.depth+1))
                        if self.is_in_loopS:
                            self.child[0].is_in_loopS = True
                            self.child[1].is_in_loopS = True
                        return
                    threshold += config.config_replace_holl["strict"]
                    if rand_int < threshold:
                        self.name = "strict"
                        self.is_hole = False
                        self.child.append(node(self.depth+1))
                        self.child.append(node(self.depth+1))
                        if self.is_in_loopS:
                            self.child[0].is_in_loopS = True
                            self.child[1].is_in_loopS = True
                        return
                    threshold += config.config_replace_holl["par"]
                    if rand_int < threshold:
                        self.name = "par"
                        self.is_hole = False
                        self.child.append(node(self.depth+1))
                        self.child.append(node(self.depth+1))
                        if self.is_in_loopS:
                            self.child[0].is_in_loopS = True
                            self.child[1].is_in_loopS = True
                        return
                    threshold += config.config_replace_holl["alt"]
                    if rand_int < threshold:
                        self.name = "alt"
                        self.is_hole = False
                        self.child.append(node(self.depth+1))
                        self.child.append(node(self.depth+1))
                        if self.is_in_loopS:
                            self.child[0].is_in_loopS = True
                            self.child[1].is_in_loopS = True
                        return
                    threshold += config.config_replace_holl["loopS"]
                    if rand_int < threshold:
                        if self.is_in_loopS:
                            pass
                        else:
                            self.name = "loopS"
                            self.is_hole = False
                            self.child.append(node(self.depth+1))
                            self.child[0].is_in_loopS = True
                            return
                    else: # hole again
                        return
        else:
            for child in self.child:
                child.replace_hole()
                
    def replace_hole_with_action(self):
        config = conf()
        if self.is_hole or self.is_leaf:
            rand_int = random.randint(0, config.config_message["sum"])
            threshold = config.config_message["pair"]
            if rand_int < threshold:
                self.is_hole = False
                source = random.randint(1, config.lifeline_num)
                dest = random.randint(1, config.lifeline_num)
                while source == dest:
                    dest = random.randint(1, config.lifeline_num)
                message = f"m{len(M_ALL)+1}"
                self.name = f"l{source} -- {message} -> l{dest}"
                if message not in M_ALL:
                    M_ALL.append(message)
                    M_PAIR.append(message)
                return
            threshold += config.config_message["env"]
            if rand_int < threshold:
                self.is_hole = False
                rand_int1 = random.randint(0, 1)
                rand_int2 = random.randint(1, config.lifeline_num)
                message = f"m{len(M_ALL)+1}"
                if rand_int1 == 0:
                    self.name = f"l{rand_int2} -- {message}-> |"
                else:
                    self.name = f"{message} -> l{rand_int2}"
                if message not in M_ALL:
                    M_ALL.append(message)
                    M_ENV.append(message)
                return
            else: # broadcast
                self.is_hole = False
                dest_num = random.randint(2, config.lifeline_num-1)
                source = random.randint(1, config.lifeline_num)
                dest_list = []
                while len(dest_list) < dest_num:
                    dest = random.randint(1, config.lifeline_num)
                    if dest not in dest_list and dest != source:
                        dest_list.append(dest)
                dest_list.sort()
                message = f"m{len(M_ALL)+1}"
                self.name = "strict"
                self.child.append(node(self.depth+1))
                self.child.append(node(self.depth+1))
                self.child[0].name = f"l{source} -- {message} -> |"
                self.child[0].is_leaf = True
                self.child[0].is_hole = False
                self.child[1].add_broadcast_dest(dest_list, message)
                if message not in M_ALL:
                    M_ALL.append(message)
                    M_BROADCAST.append(message)
                return
        else:
            for child in self.child:
                child.replace_hole_with_action()

    def add_broadcast_dest(self, dest_list, message):
        dest = dest_list.pop(0)
        self.name = "seq"
        self.child.append(node(self.depth+1))
        self.child.append(node(self.depth+1))
        self.child[0].name = f"{message} -> l{dest}"
        self.child[0].is_leaf = True
        self.child[0].is_hole = False
        if len(dest_list) > 1:
            self.child[1].add_broadcast_dest(dest_list, message)
        else:
            dest = dest_list.pop(0)
            self.child[1].name = f"{message} -> l{dest}"
            self.child[1].is_leaf = True
            self.child[1].is_hole = False

                    
def gen_random_hif(file_name = "/home/kazuma/work/random_model_to_regex/hibou_para.hif"):
    global M_ALL, M_PAIR, M_ENV, M_BROADCAST
    M_ALL = []
    M_PAIR = []
    M_ENV = []
    M_BROADCAST = []
    random_tree = node()
    for i in range(MAX_DEPTH):
        random_tree.replace_hole()
    random_tree.replace_hole_with_action()
    f = open(file_name, "w")
    f.write(str(random_tree))

if __name__ == "__main__":
    gen_random_hif()