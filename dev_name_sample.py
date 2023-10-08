import random

dic_file = 'data/files/names.txt'
eng_names = list()
with open(dic_file, mode='r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        
        line_list = line.replace('\n', '').split(' ')
        eng_names.append(line_list[0])

def get_random_eng_names(num):
    return random.sample(eng_names, num)