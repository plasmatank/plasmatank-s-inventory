from pypinyin import pinyin,Style
import re
import json
import openpyxl
wb = openpyxl.load_workbook(r"C:/Users/Plasmatank/Downloads/wb.xlsx")
ws = wb.active
dic = {}
for i in ws:
    py = " ".join(["".join(i) for i in pinyin(re.sub("·", "", re.sub("（.*）", "", i[1].value)), style=Style.FIRST_LETTER, heteronym=True)])
    if (py not in dic):
        dic[py] = [i[1].value, i[2].value]
    else:
        if (type(dic[py][0]) is str):
            dic[py] = [dic[py]]
        dic[py].append([i[1].value, i[2].value])
json.dump(dic, open("dataset.json", encoding="utf-8", mode="w"), ensure_ascii=False)
while ((p := input(">>")) != "0"):
    for namepy in dic:
        flag = 0
        for i in range(len(p)):
            l = namepy.split()
            if (len(p) <= len(l)):
                if (p[i] in l[i]):
                    flag+=1
        if (flag >= min(len(l), 3)):
            print(dic[namepy] if type(dic[namepy][0]) is str else "\n".join(str(i) for i in dic[namepy]))