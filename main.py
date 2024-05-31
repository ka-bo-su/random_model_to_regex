from gen_hif_rev import *
from nfa_to_regex import *
import subprocess
from tqdm import tqdm
import re
import argparse
import signal
from contextlib import contextmanager

MIN_ACTION_NUM = 6
MAX_ACTION_NUM = 12

# タイムアウト例外クラス
class TimeoutException(Exception):
    pass

# タイムアウトハンドラ
def handler(signum, frame):
    raise TimeoutException()

# タイムアウトコンテキストマネージャ
@contextmanager
def timeout(seconds):
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

def glosem_hibou(file_name = "test"):
    subprocess.run(f"./hibou_label.exe glosem ./model/hibou_para.hsf ./output/hif_files/{file_name}.hif > output.txt", shell=True)
    subprocess.run(f"cp {file_name}_orig_nfa.dot ./output/dot_files/{file_name}.dot", shell=True)
    subprocess.run(f"cp {file_name}_orig_nfa.png ./output/nfa_files/{file_name}.png", shell=True)
    subprocess.run("rm *.png", shell=True)
    subprocess.run("rm *.dot", shell=True)
    subprocess.run("rm *.svg", shell=True)
    with open("./output.txt", "r") as f:
        output = f.read()
    output = output.split("\n")
    for i in range(len(output)):
        if output[i][23:31]=="orig NFA":
            tmp = output[i][23:]
            break
    tmp = re.split("\s|\t|,|:", tmp)
    return int(tmp[-1])

def glosem_hibou_example(file_name, hsf_file, dot_file, hif_file, nfa_file):
    subprocess.run(f"./hibou_label.exe glosem {hsf_file} {hif_file} > output.txt", shell=True)
    subprocess.run(f"cp {file_name}_orig_nfa.dot {dot_file}", shell=True)
    subprocess.run(f"cp {file_name}_orig_nfa.png {nfa_file}", shell=True)
    subprocess.run("rm *.png", shell=True)
    subprocess.run("rm *.dot", shell=True)
    subprocess.run("rm *.svg", shell=True)
    with open("./output.txt", "r") as f:
        output = f.read()
    output = output.split("\n")
    for i in range(len(output)):
        if output[i][23:31]=="orig NFA":
            tmp = output[i][23:]
            break
    tmp = re.split("\s|\t|,|:", tmp)
    return int(tmp[-1])

def draw_sd_tt(hif_file, sd_file, tt_file):
    file_name = hif_file.split("/")[-1].split(".")[0] + "_repr.png"
    subprocess.run(["./hibou_label.exe", "draw", "-r", "sd", "./model/hibou_para.hsf", hif_file])
    subprocess.run(["mv", file_name, sd_file])
    subprocess.run(["./hibou_label.exe", "draw", "-r", "tt", "./model/hibou_para.hsf", hif_file])
    subprocess.run(["mv", file_name, tt_file])

def draw_sd_tt_example(hif_file, hsf_file, sd_file, tt_file):
    file_name = hif_file.split("/")[-1].split(".")[0] + "_repr.png"
    subprocess.run(["./hibou_label.exe", "draw", "-r", "sd", hsf_file, hif_file])
    subprocess.run(["mv", file_name, sd_file])
    subprocess.run(["./hibou_label.exe", "draw", "-r", "tt", hsf_file, hif_file])
    subprocess.run(["mv", file_name, tt_file])

def convert_action_to_num(path_to_all_regex):
    with open(path_to_all_regex, "r") as f:
        all_regex = f.read()
    regex_list = all_regex.split("\n")
    regex_num_list = []
    for regex in regex_list:
        action_dic = {}
        action_num = 0
        for i in range(len(regex)):
            if regex[i] == "(":
                start = -1
                end = -1
            elif regex[i] == "l":
                start = i
            elif regex[i] == ")" and start != -1:
                end = i
                action = regex[start:end]
                start = -1
                end = -1
                if action not in list(action_dic.keys()):
                    action_dic[action] = action_num
                    action_num = action_num + 1
        if action_num >= 10:
            regex_num_list.append("Error : The alphabet size is over 10.")
        else:
            for action in list(action_dic.keys()):
                regex = regex.replace(f"{action}", str(action_dic[action]))
            regex_num_list.append(regex)
    path_to_all_regex_num = path_to_all_regex.replace(".txt","_num.txt")
    with open(path_to_all_regex_num, "w") as f:
        for regex in regex_num_list:
            f.write(regex+"\n")
    path_to_all_regex_num_clear = path_to_all_regex.replace(".txt","_num_clear.txt")
    with open(path_to_all_regex_num_clear, "w") as f:
        for regex in regex_num_list:
            if "Error" not in regex:
                f.write(regex+"\n")

def main():
    for i in range(2000000):
        file_name = "sample" + str(i+1)
        while True:
            hif_file = f"./output/hif_files/{file_name}.hif"
            sd_file = f"./output/sd_files/{file_name}.png"
            tt_file = f"./output/tt_files/{file_name}.png"
            dot_file = f"./output/dot_files/{file_name}.dot"
            regex_file = f"./output/regex_files/{file_name}.txt"
            all_regex_file = f"./output/regex_files/all_regex.txt"
            gen_random_hif(hif_file)
            draw_sd_tt(hif_file, sd_file, tt_file)
            state_num = glosem_hibou(file_name)
            state_num_file = f"./state_num.txt"
            with open(state_num_file, "a") as f:
                f.write(f"{i+1} : {state_num}\n")
            if  state_num <= 20:
                nft_gp = graph()
                nft_gp.add_content_from_dot_file(dot_file)
                nft_gp.draw_graph(f"test")
                regex = nft_gp.get_regular_expression()
                cnt = 0
                for j in range(len(regex)):
                    if regex[j] == "l":
                        cnt += 1
                break
        with open (regex_file, "w") as f:
            f.write(regex)
        if i == 0:
            with open (all_regex_file, "w") as f:
                f.write(regex+"\n")
        else:
            with open (all_regex_file, "a") as f:
                f.write(regex+"\n")
        print(f"{i+1} : {regex}", flush=True)

def main_example():
    all_regex_file = f"./example/all_regex.txt"
    is_one_example = False
    if is_one_example:
        example_num = 25
        start = example_num - 1
        end = example_num
    else:
        start = 0
        end = 25
    for i in range(start, end, 1):
        try:
            with timeout(120):
                file_name = "ex" + str(i+1).zfill(2)
                hif_file = f"./example/{file_name}/{file_name}.hif"
                hsf_file = f"./example/{file_name}/{file_name}.hsf"
                sd_file = f"./example/{file_name}/{file_name}_sd.png"
                tt_file = f"./example/{file_name}/{file_name}_tt.png"
                nfa_file = f"./example/{file_name}/{file_name}_nfa.png"
                dot_file = f"./example/{file_name}/{file_name}.dot"
                regex_file = f"./example/{file_name}/{file_name}.txt"
                graph_image_path = f"./example/{file_name}/nfa_merge"

                draw_sd_tt_example(hif_file, hsf_file, sd_file, tt_file)
                state_num = glosem_hibou_example(file_name, hsf_file, dot_file, hif_file, nfa_file)
                nft_gp = graph()
                nft_gp.add_content_from_dot_file(dot_file)
                nft_gp.draw_graph(f"test")
                regex = nft_gp.get_regular_expression(True, graph_image_path)
                with open (regex_file, "w") as f:
                    f.write(regex)
                if i == 0:
                    with open (all_regex_file, "w") as f:
                        f.write(regex+"\n")
                else:
                    with open (all_regex_file, "a") as f:
                        f.write(regex+"\n")
                print(f"{i+1} : {regex}", flush=True)
        except TimeoutException:
            if i == 0:
                with open (all_regex_file, "w") as f:
                    f.write('Error : The operation timed out.'+"\n")
            else:
                with open (all_regex_file, "a") as f:
                    f.write('Error : The operation timed out.'+"\n")
            try:
                subprocess.run("rm *.png", shell=True)
                subprocess.run("rm *.dot", shell=True)
                subprocess.run("rm *.svg", shell=True)
            except:
                pass
            print('The operation timed out.')
    convert_action_to_num(all_regex_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--example', action='store_true')
    args = parser.parse_args()
    if args.example:
        main_example()
    else:
        main()
    # subprocess.run("reset", shell=True)