from gen_hif import *
from nfa_to_regex import *
import subprocess
from tqdm import tqdm
import re

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

def main():
    for i in range(100):
        file_name = "smple" + str(i+1)
        while True:
            gen_random_hif(f"./output/hif_files/{file_name}.hif")
            state_num = glosem_hibou(file_name)
            nft_gp = graph()
            nft_gp.add_content_from_dot_file(f"./output/dot_files/{file_name}.dot")
            nft_gp.draw_graph(f"test")
            regex = nft_gp.get_regular_expression()
            cnt = 0
            for j in range(len(regex)):
                if regex[j] == "l":
                    cnt += 1
            if cnt >= 2 and cnt <= 15:
                break
        with open (f"./output/regex_files/{file_name}.txt", "w") as f:
            f.write(regex)
        if i == 0:
            with open (f"./output/regex_files/all_regex.txt", "w") as f:
                f.write(regex+"\n")
        else:
            with open (f"./output/regex_files/all_regex.txt", "a") as f:
                f.write(regex+"\n")
        print(f"{i+1} : {regex}", flush=True)

if __name__ == "__main__":
    main()