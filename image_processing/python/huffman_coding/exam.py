import math
import os

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

def encode_text(mapping: dict={}, coded_text: str="", counter=0) -> tuple:

    with open(os.path.join(os.sys.path[0], "Alice29.txt"), "r") as file:
        for line in file:
            for char in line:
                counter += 1
                if char in mapping.keys():
                    coded_text += mapping[char]

    return coded_text, counter

def printTree(node, level=0):
    if node != None:
        printTree(node.left, level + 1)
        if not node.right and not node.left:
            print(' ' * 4 * level + '-> ' + str(node.value[0]))
        else:
            print(' ' * 4 * level + '-> ' + "{:.2f}".format(node.value[1]))
        printTree(node.right, level + 1)


if __name__ == '__main__':

    exam_counts = {1: 1/40, 2: 2/10, 3: 1/20, 4: 1/40, 5: 3/10, 6: 1/40, 7: 1/20, 8: 2/10, 9: 1/10, 10: 1/40}
    exam_counts = {k:v for k, v in sorted(exam_counts.items(), key=lambda item: item[1], reverse=True)}
    root_exam = code_tree([Node(val) for val in list(exam_counts.items())])
    mapping_exam = {}
    assign_codes(root_exam, mapping_exam)
    sorted_map_exam = sorted(mapping_exam.items(), key=lambda item: item[0])
    sorted_exam_counts = sorted(exam_counts.items(), key=lambda item: item[0])
    for index, entry in enumerate(sorted_map_exam):
        print("Character: \"{}\"  probability: {: <22} {: <5} {}".format(entry[0], sorted_exam_counts[index][1], "code:", entry[1]))
    entropy_uncoded = Entropy([prob for prob in list(exam_counts.values())])
    print("Entropy of text file = ", entropy_uncoded)
    average_code_len = calc_avg_code_len(root_exam)
    print("Average code length = {}".format(average_code_len))
    print("H < avgerage code len < H + 1: ", average_code_len > entropy_uncoded and average_code_len < entropy_uncoded + 1)
    printTree(root_exam)
