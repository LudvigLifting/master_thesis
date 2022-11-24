import math
import os
import time
import csv
from matplotlib import pyplot as plt

class Node:
    def __init__(self, value, left=None, right=None):
      self.left = left
      self.right = right
      self.value = value

def char_counter(file) -> dict:
    
    #Count every occurence of each char in the text and add to dict
    counts = {}
    for line in file:
        for char in line:
            if char in counts:
                counts[char] += 1
            else:
                counts[char] = 1
                
    total_chars = sum([item[1] for item in counts.items()])

    #Sort in descending frequencies
    counts = {k:v for k, v in sorted(counts.items(), key=lambda item: item[1], reverse=True)}
    
    #Calculate probabilities from the frequencies 
    for key in counts:
        counts[key] /= total_chars

    return counts

def nbr_counter() -> dict:

    with open(os.path.join(os.sys.path[0], 'numbers.csv'), newline='') as csvfile:
        
        nbrs = list(csv.reader(csvfile, delimiter=' ', quotechar='|'))[0]

        # plt.hist(nbrs, histtype="step")
        # plt.show()
        #Count every occurence of each number in the csv
        counts = {}

        #Make sure every possible intensity is in the list and give the missing intensities the longest code
        missing_nbrs = [missing_nbr for missing_nbr in range(256) if missing_nbr not in nbrs]
        for m_n in missing_nbrs:
            counts[str(m_n)] = 1
            
        for nbr in nbrs:
            if nbr in counts:
                counts[nbr] += 1
            else:
                counts[nbr] = 1
                
    total_chars = sum([item[1] for item in counts.items()])

    #Sort in descending frequencies
    counts = {k:v for k, v in sorted(counts.items(), key=lambda item: item[1], reverse=True)}

    #Calculate probabilities from the frequencies 
    for key in counts:
        counts[key] /= total_chars

    return counts

def Entropy(P: list) -> float:
            
    return (-1 * sum([x * math.log2(x) if x != 0 else 0 for x in P]))

def code_tree(probs: list) -> Node:

    #Base case for function (last element must be the root)
    if len(probs) == 1:
        return probs.pop()
    
    #pop the two lowest probabilities
    prob_0 = probs.pop()
    prob_1 = probs.pop()

    #combine the probabilities for the new node value (as well as the symbols)
    node = Node((prob_0.value[0] + prob_1.value[0], prob_0.value[1] + prob_1.value[1]))

    #assign node.right and left
    node.right, node.left = (prob_1, prob_0)

    #Insert new node in the right place (descending probability)
    if len(probs) > 0:
        for index, item in enumerate(probs):
            if item.value[1] < node.value[1]:
                probs.insert(index, node)
                break
            elif index == len(probs) - 1:
                probs.append(node)
                break
    else:
        probs.append(node)
    
    return code_tree(probs)

def assign_codes(node: Node, code_map: dict={}, code: str="") -> None:
    
    #not a node
    if not node:
        return

    #leaf node
    if not node.left and not node.right:
        code_map[node.value[0]] = code
    
    assign_codes(node.left, code_map, code + "0")
    assign_codes(node.right, code_map, code + "1")

def calc_avg_code_len(node: Node, code_map: dict={}, level: int=0):
    
    if not node.right and not node.left:
        return

    if level in code_map:
        code_map[level] += node.value[1]
    else:
        code_map[level] = node.value[1]

    calc_avg_code_len(node.left, code_map, level + 1)
    calc_avg_code_len(node.right, code_map, level + 1)

    return sum(list(code_map.values()))

def encode_nbrs(mapping: dict={}, coded_text: str="", counter=0) -> tuple:

    with open(os.path.join(os.sys.path[0], 'numbers.csv'), newline='') as csvfile:
        
        nbrs = list(csv.reader(csvfile, delimiter=' ', quotechar='|'))[0]
        for nbr in nbrs:
            counter += 1
            if nbr in mapping.keys():
                coded_text += mapping[nbr]
    return coded_text, counter

def encode_text(mapping: dict={}, coded_text: str="", counter=0) -> tuple:

    with open(os.path.join(os.sys.path[0], "Alice29.txt"), "r") as file:
        for line in file:
            for char in line:
                counter += 1
                if char in mapping.keys():
                    coded_text += mapping[char]

    return coded_text, counter


if __name__ == '__main__':

    start = time.time()
    #Open the text and calculate the probability distribution for each char
    # with open(os.path.join(os.sys.path[0], "Alice29.txt"), "r") as file:
    #     counts = char_counter(file)
    # print(len(counts))
    counts = nbr_counter()
    
    #The root of the binary tree
    root = code_tree([Node(val) for val in list(counts.items())])

    #Assign each symbol a code and store them in mapping
    mapping = {}
    assign_codes(root, mapping)

    #Sort code mapping and counts for easy comparison (sorted by symbol)
    sorted_map = sorted(mapping.items(), key=lambda item: int(item[0]))
    sorted_counts = sorted(counts.items(), key=lambda item: item[0])

    #Encode the text with the generated codes
    coded_text, uncoded_len = encode_nbrs(mapping)
    coded_len = len(coded_text)
    uncoded_len *= 8 #nbr of bits per symbol

    #Results
    print("\nCode table & Distribution of letters: ")
    for index, entry in enumerate(sorted_map):
        if entry[0] == '\n':
            print("Character: \"\\n\" probability: {: <22} {: <5} {}".format(sorted_counts[index][1], "code:", entry[1]))
        else:
            print("Character: \"{:3}\"  probability: {: <22} {: <5} {}".format(entry[0], sorted_counts[index][1], "code:", entry[1]))
    
    print("\nLength of the uncoded text = ", uncoded_len)
    print("Length of the coded text = {}, compression ratio = {:.4f}".format(coded_len, uncoded_len / coded_len))

    entropy_uncoded = Entropy([prob for prob in list(counts.values())])
    print("Entropy of text file = ", entropy_uncoded)

    average_code_len = calc_avg_code_len(root)
    print("Average code length = {}".format(average_code_len))
    print("H < avgerage code len < H + 1: ", average_code_len > entropy_uncoded and average_code_len < entropy_uncoded + 1)
    print(f"Elapsed time: {time.time() - start}s")