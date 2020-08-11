def func(strings, fix):
    temp = []
    try:
        for k in strings:
            temp.append(k)
            count = 0
            for j in range(len(temp)):
                if temp[j] == strings[len(temp) + j]:
                    count += 1
            if count == len(temp):
                return temp
    except IndexError:
        return [f"{fix}不存在"]

while True:
    string = input(">>")
    string_list = string
    print("".join(temps := func(string, "前缀")), end=" : ")
    print(string.count("".join(temps)))
    for i in temps:
        string = string.replace(i, "")
    print("".join(double_temps := list(reversed(func("".join(reversed(string_list)), "后缀")))), end=" : ")
    print(string.count("".join(double_temps)))
    for i in double_temps:
        string = string.replace(i, "")
    print(string)

