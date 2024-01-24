def is_unique(str1) -> bool:
    dict_chars = dict()
    for i in range(len(str1)):
        if str1[i] in dict_chars.keys():
            return False
        dict_chars[str1[i]] = 1
    return True


def is_permutation(str1: str, str2: str) -> bool:
    if (len(str1) != len(str2)):
        return False
    sorted_str1 = sorted(str1)
    sorted_str2 = sorted(str2)
    return sorted_str1 == sorted_str2

def is_perm(str1:str,str2:str)->bool:
    if (len(str1) != len(str2)):
        return False
    dict1,dict2={},{}
    for i in range (len(str1)):
        helper_func(dict1, i, str1)
        helper_func(dict2,i,str2)

    for i in range(len(str1)):
        if (str1[i] not in dict2.keys()) or (dict2[str1[i]]!=dict1[str1[i]]):
            return False
    return True


def helper_func(dict1, i, str1):
    if str1[i] in dict1.keys():
        dict1[str1[i]] += 1
    else:
        dict1[str1[i]] = 1


if __name__ == '__main__':
    # print(is_unique("ab"))
    print(is_permutation("aba","baa"))
    print(is_perm("abbc",""))
