#ecoding:utf-8
def rightStr(string, split = ' '):
    end_index = string.rfind(split)
    res = string
    while end_index != -1 and end_index == len(res) - 1:
        res = res[:end_index]
        end_index = res.rfind(split)
    return res, end_index

if __name__ == '__main__':
    print  rightStr('s s s   ')