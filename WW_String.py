def get_translit_kirilica_to_latinica(text=""):
    tmp = list(text.lower())
    res = ""
    for i in tmp:
        if(i == "й"):
            res+="y"
        elif(i=="ц"):
            res+="c"
        elif (i == "у"):
            res += "u"
        elif (i == "к"):
            res += "k"
        elif (i == "е"):
            res += "e"
        elif (i == "н"):
            res += "n"
        elif (i == "г"):
            res += "g"
        elif (i == "ш"):
            res += "sh"
        elif (i == "щ"):
            res += "sh"
        elif (i == "з"):
            res += "z"
        elif (i == "х"):
            res += "h"
        elif (i == "ї"):
            res += "yi"
        elif (i == "ф"):
            res += "f"
        elif (i == "і"):
            res += "i"
        elif (i == "ы"):
            res += "y"
        elif (i == "в"):
            res += "v"
        elif (i == "а"):
            res += "a"
        elif (i == "п"):
            res += "p"
        elif (i == "р"):
            res += "r"
        elif (i == "о"):
            res += "o"
        elif (i == "л"):
            res += "l"
        elif (i == "д"):
            res += "d"
        elif (i == "ж"):
            res += "j"
        elif (i == "є"):
            res += "ye"
        elif (i == "э"):
            res += "e"
        elif (i == "я"):
            res += "ya"
        elif (i == "ч"):
            res += "ch"
        elif (i == "с"):
            res += "s"
        elif (i == "м"):
            res += "m"
        elif (i == "и"):
            res += "y"
        elif (i == "т"):
            res += "t"
        elif (i == "б"):
            res += "b"
        elif (i == "ю"):
            res += "yu"
        elif (i == "ё"):
            res += "yo"
        else:
            res+=i
    return res

def is_iqvals(txt2 = "", txt1_s = "", pp = 60):
    tmp1 = list(txt1_s.lower())
    tmp2 = list(txt2.lower())
    proc_per_symb = (1 / len(tmp2)) * 100
    proc = 0
    for i in tmp1:
        if i in tmp2:
            proc += proc_per_symb
            tmp2.remove(i)
    proc2 = 0
    tmp1 = list(txt1_s.lower())
    tmp2 = list(txt2.lower())
    new_tmp1 = []
    new_tmp2 = []
    for i in range(len(tmp1) - 1):
        if (i != len(tmp1) - 1):
            new_tmp1.append(tmp1[i] + tmp1[i + 1])
    for i in range(len(tmp2) - 1):
        if (i != len(tmp2) - 1):
            new_tmp2.append(tmp2[i] + tmp2[i + 1])
    proc_per_symb = (1 / len(new_tmp2)) * 100
    for i in new_tmp1:
        if (i in new_tmp2):
            proc2 += proc_per_symb
            new_tmp2.remove(i)
    a = round(((proc * 0.5) + (proc2 * 1.5)) / 2, 2)

    tmp1 = list(get_translit_kirilica_to_latinica(txt1_s.lower()))
    tmp2 = list(txt2.lower())
    proc_per_symb = (1 / len(tmp2)) * 100
    proc = 0
    for i in tmp1:
        if i in tmp2:
            proc += proc_per_symb
            tmp2.remove(i)
    proc2 = 0
    tmp1 = list(get_translit_kirilica_to_latinica(txt1_s.lower()))
    tmp2 = list(txt2.lower())
    new_tmp1 = []
    new_tmp2 = []
    for i in range(len(tmp1) - 1):
        if (i != len(tmp1) - 1):
            new_tmp1.append(tmp1[i] + tmp1[i + 1])
    for i in range(len(tmp2) - 1):
        if (i != len(tmp2) - 1):
            new_tmp2.append(tmp2[i] + tmp2[i + 1])
    proc_per_symb = (1 / len(new_tmp2)) * 100
    for i in new_tmp1:
        if (i in new_tmp2):
            proc2 += proc_per_symb
            new_tmp2.remove(i)
    a2 = round(((proc * 0.5) + (proc2 * 1.5)) / 2, 2)

    if(a2 > a):
        a = a2

    print(a, " > ",pp)
    return a >= pp

def is_iqvals_ret(txt2 = "", txt1_s = "", pp = 60):
    tmp1 = list(txt1_s.lower())
    tmp2 = list(txt2.lower())
    proc_per_symb = (1 / len(tmp2)) * 100
    proc = 0
    for i in tmp1:
        if i in tmp2:
            proc += proc_per_symb
            tmp2.remove(i)
    proc2 = 0
    tmp1 = list(txt1_s.lower())
    tmp2 = list(txt2.lower())
    new_tmp1 = []
    new_tmp2 = []
    for i in range(len(tmp1) - 1):
        if (i != len(tmp1) - 1):
            new_tmp1.append(tmp1[i] + tmp1[i + 1])
    for i in range(len(tmp2) - 1):
        if (i != len(tmp2) - 1):
            new_tmp2.append(tmp2[i] + tmp2[i + 1])
    proc_per_symb = (1 / len(new_tmp2)) * 100
    for i in new_tmp1:
        if (i in new_tmp2):
            proc2 += proc_per_symb
            new_tmp2.remove(i)
    a = round(((proc * 0.5) + (proc2 * 1.5)) / 2, 2)

    tmp1 = list(get_translit_kirilica_to_latinica(txt1_s.lower()))
    tmp2 = list(txt2.lower())
    proc_per_symb = (1 / len(tmp2)) * 100
    proc = 0
    for i in tmp1:
        if i in tmp2:
            proc += proc_per_symb
            tmp2.remove(i)
    proc2 = 0
    tmp1 = list(get_translit_kirilica_to_latinica(txt1_s.lower()))
    tmp2 = list(txt2.lower())
    new_tmp1 = []
    new_tmp2 = []
    for i in range(len(tmp1) - 1):
        if (i != len(tmp1) - 1):
            new_tmp1.append(tmp1[i] + tmp1[i + 1])
    for i in range(len(tmp2) - 1):
        if (i != len(tmp2) - 1):
            new_tmp2.append(tmp2[i] + tmp2[i + 1])
    proc_per_symb = (1 / len(new_tmp2)) * 100
    for i in new_tmp1:
        if (i in new_tmp2):
            proc2 += proc_per_symb
            new_tmp2.remove(i)
    a2 = round(((proc * 0.5) + (proc2 * 1.5)) / 2, 2)

    if (a2 > a):
        a = a2

    print(a, " > ", pp)
    return a
