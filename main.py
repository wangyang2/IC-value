# python version = 3.5
import jieba
import re
import itertools
import math
import jieba.posseg as pseg


def is_number(num):
    regex = re.compile(r'^(-?\d+)(\.\d*)?$')
    if re.match(regex, num):
        return True
    else:
        return False


def is_alphabet(alpha):
    if re.match(r'[a-z]+', alpha, re.I):
        return True
    else:
        return False


def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8-sig').readlines()]
    return stopwords


def seg_sentence(sentence):
    sentence_seged = jieba.cut(sentence.strip())
    stopwords = stopwordslist(r'C:\Users\viruser.v-desktop\Desktop\IC-value\stopwords-utf8.txt')
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t' and is_number(word) == 0 and is_alphabet(word) == 0:
                outstr += word
    return outstr

inputs1 = open(r'C:\Users\viruser.v-desktop\Desktop\IC-value\single-txt.txt', 'r', encoding='utf-8-sig')
outputs1 = open(r'C:\Users\viruser.v-desktop\Desktop\IC-value\result.txt', 'w', encoding='utf-8-sig')
for line in inputs1:
    line_seg = seg_sentence(line)
    for str in line_seg:
        outputs1.write(str)
outputs1.close()
inputs1.close()

inputs2 = open(r'C:\Users\viruser.v-desktop\Desktop\IC-value\result.txt', 'r', encoding='utf-8-sig')
word_list = inputs2.read().strip()
theta = 3
dic = {}
del_list1 = []
del_list2 = []
pairs_word_list = []
pairs_tag_list = []

for i in range(1, len(word_list)+1):
    for index in range(0, len(word_list)):
        if i + index <= len(word_list):
            a_list = list(word_list)
            b = a_list[index:index+i]
            s = ''.join(itertools.chain(*b))
            if word_list.count(s) >= theta:
                dic[s] = word_list.count(s)

keys_list = list(dic.keys())
for t in keys_list:
    for k in dic.keys():
        if len(t) > len(k) and k in t:
            del_list1.append(k)

del_list1 = set(del_list1)
for i in del_list1:
    keys_list.remove(i)
print(keys_list)

for term in keys_list:
    pairs = pseg.cut(term)
    for word, tag in pairs:
        pairs_word_list.append(word)
        pairs_tag_list.append(tag)
    if len(pairs_word_list) == 1 and tag.startswith('n') == 0:
        del_list2.append(term)
    if tag.startswith('w') == 1:
        del_list2.append(term)
    if pairs_tag_list[-1].startswith(('m', 'f', 'p', 'c')) == 1:
        del_list2.append(term)
    pairs_word_list = []
    pairs_tag_list = []

del_list2 = set(del_list2)
for i in del_list2:
    keys_list.remove(i)
print(keys_list)

IC_dic = {}
N = 20
in_list = []
in_dic = {}
all_txt_list = []
del_key = []

for i in keys_list:
    for j in keys_list:
        if i != j and i in j:
            in_list.append(j)
    in_dic[i] = in_list
    in_list = []
print(in_dic)

all_txt = open(r'C:\Users\viruser.v-desktop\Desktop\IC-value\all-txt.txt', 'r', encoding='utf-8-sig')
for line in all_txt.readlines():
    curLine = line.strip()
    all_txt_list.append(curLine)

for key, value in in_dic.items():
    if len(value) == 0:
        g_a = 1
        for txt in all_txt_list:
            if key in txt:
                g_a += 1
        IC = len(key) * word_list.count(key) * math.log(N / g_a, 2)
        IC_dic[key] = IC
    else:
        sum_b = 0
        g_a = 1
        for txt in all_txt_list:
            if key in txt:
                g_a += 1
        for i in value:
            sum_b += word_list.count(i)
        IC = len(key) * (word_list.count(key) - sum_b) * math.log(N / g_a, 2)
        IC_dic[key] = IC

for key, value in IC_dic.items():
    if len(key) == 1:
        del_key.append(key)

for key in del_key:
    IC_dic.pop(key)
print(IC_dic)
