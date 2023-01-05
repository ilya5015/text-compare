import ast
import sys
import argparse

# 1 аргумент - список пар документов, 2 аргумент - путь до выходного файла

def levenstein_distance(str1, str2):

    n, m = len(str1), len(str2)

    if n > m:
        str1, str2 = str2, str1
        n, m = m, n

    currentRow = range(n + 1)
    for i in range(1, m + 1):
        previousRow, currentRow = currentRow, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, replace = previousRow[j] + 1, currentRow[j - 1] + 1, previousRow[j - 1]
            if str1[j-1] != str2[i-1]:
                m = 1
            else:
                m = 0
            replace += m
            currentRow[j] = min(add, delete, replace)

    distance = str(round((1 - currentRow[n]/max(len(str1), len(str2))), 3))

    print('distance is', distance)
    return distance

parser = argparse.ArgumentParser(prog = 'TextCompare', description = 'Programm compares 2 different texts using levenshtein distance')
parser.add_argument('inputFile')
parser.add_argument('outputFile')
args = parser.parse_args()
file1 = args.inputFile
file2 = args.outputFile

print('args are', file1, file2)

filePairs = []

with open(file2, 'wb'):
    pass

with open(file1) as f1:
    while True:
        line = f1.readline()
        if not line:
            break
        pair = line.split()
        filePairs.append(pair)
        print(pair)

for pair in filePairs:
    with open(f'./files/{pair[0]}', encoding='UTF8') as f1, open(f'./files/{pair[1]}', encoding='UTF8') as f2, open(file2, 'a') as f3:
        code1 = f1.read()
        code2 = f2.read()
        node1 = ast.parse(code1)
        node2 = ast.parse(code2)
        node_str1 = ast.dump(node1, annotate_fields=False, indent=4).splitlines()
        node_str2 = ast.dump(node2, annotate_fields=False, indent=4).splitlines()

        for i in range(len(node_str1)):
            node_str1[i] = node_str1[i].strip()

        for i in range(len(node_str2)):
            node_str2[i] = node_str2[i].strip()

        distance = levenstein_distance(node_str1, node_str2)

        f3.write(distance + '\n')


