import random
# 关键代码位于第85行

# -------------------------- 初始化数据 ---------------------------- #
# 标准化文件中的数独数据，存放于standard中
def receive_information(infor):
    standard_line = [[], [], [], [], [], [], [], [], []]  # 九个区域分别进行划分
    if len(infor) == 81:
        for i in range(9):
            b = infor[i * 9:i * 9 + 9]
            for j in range(9):
                standard_line[i].append(int(b[j]))
        return standard_line
    return False


# 检查数据存储后是否合理
def check_fault(sudoku):
    if len(sudoku) != 9:
        return False
    for i in range(9):
        if len(sudoku[i]) != 9:
            return False
        if sudoku[i].count([]) > 0:
            return False
        for j in range(1, 10):
            if sudoku[i].count(j) > 1:
                return False
    return True


# 备份数据，以防在破解中失败而无法找到数据
def backups(a):
    copy = [[], [], [], [], [], [], [], [], []]
    for i in range(9):
        for j in range(9):
            if type(a[i][j]) == int:
                copy[i].append(a[i][j])
            elif type(a[i][j]) == list:
                copy[i].append([])
                for k in a[i][j]:
                    copy[i][j].append(k)
    return copy


# -------------------------- 数据定位与还原 ---------------------------- #
# 定位特定数独数据所在的大区域的位置
def locate_section(x, y):
    location_section = (x // 3) * 3 + y // 3
    return location_section


# 定位特定数独数据
def locate_relative(x, y):
    location_relative = (x % 3) * 3 + y % 3
    return location_relative


# 还原绝对坐标值x
def return_absolute_x(location_section, location_relative):
    x = (location_section // 3) * 3 + location_relative // 3
    return x


# 还原绝对坐标值y
def return_absolute_y(location_section, location_relative):
    y = (location_section % 3) * 3 + location_relative % 3
    return y


# 转换行形式的数据为列
def convert(a):
    b = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    c = [[], [], [], [], [], [], [], [], []]
    for i in range(9):
        for j in range(9):
            if a[i][j] == 0:
                a[i][j] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            b[j][i] = a[i][j]
            s = locate_section(i, j)
            c[s].append(a[i][j])
    return b, c


# -------------------------- 数独解密 ---------------------------- #
# 唯一候选数法
# 当某个单元格的候选数排除到只有一个数的时候，那么这个数就是该宫格的唯一的一个候选数，这个候选数就是解
def only_cadidate(a, b, c, i, j, change):
    def num_abc():
        num_a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        num_b = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        num_c = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for k in range(1, 10):
            if k in a[i]:
                num_a.remove(k)
            if k in b[j]:
                num_b.remove(k)
            if k in c[s]:
                num_c.remove(k)
        return num_a, num_b, num_c

    s = locate_section(i, j)
    num_a, num_b, num_c = num_abc()
    for n in num_a:
        t = 0
        for k in range(9):
            if type(a[i][k]) == list and n in a[i][k]:
                t += 1
        if t == 1:
            for k in range(9):
                if type(a[i][k]) == list and n in a[i][k]:
                    a[i][k] = n
                    b[k][i] = n
                    c[locate_section(i, k)][locate_relative(i, k)] = n
                    num_a, num_b, num_c = num_abc()
            change = True
    for n in num_b:
        t = 0
        for k in range(9):
            if type(b[j][k]) == list and n in b[j][k]:
                t += 1
        if t == 1:
            for k in range(9):
                if type(b[j][k]) == list and n in b[j][k]:
                    a[k][j] = n
                    b[j][k] = n
                    c[locate_section(k, j)][locate_relative(k, j)] = n
                    num_a, num_b, num_c = num_abc()
            change = True
    for n in num_c:
        t = 0
        for k in range(9):
            if type(c[s][k]) == list and n in c[s][k]:
                t += 1
        if t == 1:
            for k in range(9):
                if type(c[s][k]) == list and n in c[s][k]:
                    a[return_absolute_x(s, k)][return_absolute_y(s, k)] = n
                    b[return_absolute_y(s, k)][return_absolute_x(s, k)] = n
                    c[s][k] = n
            change = True
    return a, b, c, change


# 将笔记中同行、同列及同宫的笔记里删除已知数字，并将唯一可能的格子变成已知数字
def delete_known(a, b, c, i, j, change):
    s = locate_section(i, j)
    for num in range(1, 10):
        for k in range(9):
            if type(a[i][k]) == list and num in a[i] and num in a[i][k]:
                a[i][k].remove(num)
                change = True
                if len(a[i][k]) == 1:
                    n = a[i][k][0]
                    a[i][k] = n
                    b[k][i] = n
                    c[locate_section(i, k)][locate_relative(i, k)] = n
                    change = True
            if type(b[j][k]) == list and num in b[j] and num in b[j][k]:
                b[j][k].remove(num)
                change = True
                if len(b[j][k]) == 1:
                    n = b[j][k][0]
                    a[k][j] = n
                    b[j][k] = n
                    c[locate_section(k, j)][locate_relative(k, j)] = n
                    change = True
            if type(c[s][k]) == list and num in c[s] and num in c[s][k]:
                c[s][k].remove(num)
                change = True
                if len(c[s][k]) == 1:
                    n = c[s][k][0]
                    a[return_absolute_x(s, k)][return_absolute_y(s, k)] = n
                    b[return_absolute_y(s, k)][return_absolute_x(s, k)] = n
                    c[s][k] = n
                    change = True
    return a, b, c, change


# 链数删减法
# 找出某一行/列/九宫格中的某三个单元格候选数中，不相同的数字不超过3个的情形， 进而将这3个数字在其它宫格的候选数中删减掉。因为这三个数字只可以填在这三个单元格内。
def chain_number_deletion(a, b, c, i, j, change):
    list_a = []
    list_b = []
    list_c = []
    s = locate_section(i, j)
    for k in range(9):
        if type(a[i][k]) == list:
            list_a.append(a[i][k])
    for k in range(9):
        if type(b[j][k]) == list:
            list_b.append(b[j][k])
    for k in range(9):
        if type(c[s][k]) == list:
            list_c.append(c[s][k])
    for k in range(3, len(list_a) + 1):
        l = []
        n = 0
        for m in list_a:
            if len(m) < k:
                for p in m:
                    if p not in l:
                        l.append(p)
                n += 1
        if len(l) == n:
            for m in list_a:
                for p in m:
                    if p not in l:
                        for q in l:
                            if q in m:
                                m.remove(q)
                                change = True
    for k in range(3, len(list_b) + 1):
        l = []
        n = 0
        for m in list_b:
            if len(m) < k:
                for p in m:
                    if p not in l:
                        l.append(p)
                n += 1
        if len(l) == n:
            for m in list_b:
                for p in m:
                    if p not in l:
                        for q in l:
                            if q in m:
                                m.remove(q)
                                change = True
    for k in range(3, len(list_c) + 1):
        l = []
        n = 0
        for m in list_c:
            if len(m) < k:
                for p in m:
                    if p not in l:
                        l.append(p)
                n += 1
        if len(l) == n:
            for m in list_c:
                for p in m:
                    if p not in l:
                        for q in l:
                            if q in m:
                                m.remove(q)
                                change = True
    return a, b, c, change


# 区块摒除法
# 利用宫内摒除法在某个宫内形成一个区块，利用该区块的排除再结合其他已知数共同确定某宫内只有一个格出现该数字
def block_exclusion(a, b, c, change):
    for i in range(3):
        m = [[], [], [], [], [], [], [], [], []]
        for k in range(3):
            for j in range(9):
                if type(a[i * 3 + k][j]) == list:
                    for n in a[i * 3 + k][j]:
                        if n not in m[k * 3 + j // 3]:
                            m[k * 3 + j // 3].append(n)
        for p in range(3):
            o = []
            for q in range(3):
                if m[p * 3 + q]:
                    for k in m[p * 3 + q]:
                        if k not in o:
                            o.append(k)
            if o:
                for s in o:
                    t = 0
                    for q in range(3):
                        if s in m[p * 3 + q]:
                            t += 1
                    if t == 1:
                        for q in range(3):
                            if s in m[p * 3 + q]:
                                if p == 0:
                                    l = [1, 2]
                                elif p == 1:
                                    l = [0, 2]
                                else:
                                    l = [0, 1]
                                for k in l:
                                    for j in range(3):
                                        if type(a[i * 3 + k][q * 3 + j]) == list and s in a[i * 3 + k][q * 3 + j]:
                                            a[i * 3 + k][q * 3 + j].remove(s)
                                            change = True
    for i in range(3):
        m = [[], [], [], [], [], [], [], [], []]
        for k in range(3):
            for j in range(9):
                if type(b[i * 3 + k][j]) == list:
                    for n in b[i * 3 + k][j]:
                        if n not in m[k * 3 + j // 3]:
                            m[k * 3 + j // 3].append(n)
        for p in range(3):
            o = []
            for q in range(3):
                if m[p * 3 + q]:
                    for k in m[p * 3 + q]:
                        if k not in o:
                            o.append(k)
            if o:
                for s in o:
                    t = 0
                    for q in range(3):
                        if s in m[p * 3 + q]:
                            t += 1
                    if t == 1:
                        for q in range(3):
                            if s in m[p * 3 + q]:
                                if p == 0:
                                    l = [1, 2]
                                elif p == 1:
                                    l = [0, 2]
                                else:
                                    l = [0, 1]
                                for k in l:
                                    for j in range(3):
                                        if type(b[i * 3 + k][q * 3 + j]) == list and s in b[i * 3 + k][q * 3 + j]:
                                            b[i * 3 + k][q * 3 + j].remove(s)
                                            change = True
    return a, b, c, change


# 假设法
# 一些位置填的数字可能就两三种情况，那我们可以结合这个可能性，进行假设与猜想，由猜想的数字再往后填写，如果后续没有出现矛盾，那么这个假设就是正确的，反之就是假设有问题，须复原回去，用其他可能来填写。
def hypothesis(a, b, c, change, examine, a_copy):
    if examine:
        for l in range(2, 10):
            for i in range(9):
                for j in range(9):
                    if type(a[i][j]) == list and len(a[i][j]) == l:
                        a_copy = backups(a)
                        n = a[i][j][random.randint(0, len(a[i][j]) - 1)]
                        a_copy[i][j].remove(n)
                        if len(a_copy[i][j]) == 1:
                            a_copy[i][j] = a_copy[i][j][0]
                        a[i][j] = n
                        b[j][i] = n
                        c[locate_section(i, j)][locate_relative(i, j)] = n
                        change = True
                        return a, b, c, change, examine, a_copy
    if examine == False and check_fault(a_copy) == True:
        a = a_copy
        b, c = convert(a)
        change = True
        examine = True
        return a, b, c, change, examine, a_copy
    examine = False
    return a, b, c, change, examine, a_copy


# j结合以上几种方法进行计算
def combination(a, b, c, change, examine, a_copy, d):
    for i in range(9):
        for j in range(9):
            a, b, c, change = delete_known(a, b, c, i, j, change)
    if not change:
        for i in range(9):
            for j in range(9):
                a, b, c, change = only_cadidate(a, b, c, i, j, change)
        if d < 1 and change == True:
            if not check_over(a):
                d = 1
    if not change:
        for i in range(9):
            for j in range(9):
                a, b, c, change = chain_number_deletion(a, b, c, i, j, change)
        if d < 2 and change == True:
            if not check_over(a):
                d = 2
    if not change:
        a, b, c, change = block_exclusion(a, b, c, change)
        if d < 3 and change == True:
            if not check_over(a):
                d = 3
    if not change:
        examine = check_fault(a)
        a, b, c, change, examine, a_copy = hypothesis(a, b, c, change, examine, a_copy)
        if d < 4 and change == True:
            if not check_over(a):
                d = 4
    return a, b, c, change, examine, a_copy, d


# -------------------------- 数据可视化 ---------------------------- #
def screen_division(a):  # 用于输出方便阅读的结果
    for temp_1 in range(9):
        if temp_1 % 3 == 0:
            print(' ------- ------- ------- ')
        for temp_2 in range(9):
            if temp_2 % 3 == 0:
                print('|', end=' ')
            print(a[temp_1][temp_2], end=' ')
        print('|', end='\n')
    print(' ------- ------- ------- ')
    return


# -------------------------- 程序的执行 ---------------------------- #
# 计算数独的主体
def calculation(a):
    if not check_fault(a):
        return False
    b, c = convert(a)
    if not check_fault(b):
        return False
    if not check_fault(c):
        return False
    change = True  # 初始化change
    examine = True  # 初始化examine
    a_copy = []  # 初始化a_copy
    d = 0
    while change:
        change = False
        a, b, c, change, examine, a_copy, d = combination(a, b, c, change, examine, a_copy, d)
        examine = check_fault(a) & check_fault(b) & check_fault(c)
    if not check_over(a):
        return None, 4
    return a, d


def check_over(sample):  # 用于检测数独是否完成
    for i in range(9):
        for j in range(9):
            if type(sample[i][j]) != int or sample[i][j] == 0:
                return False
    return True


if __name__ == "__main__":
    f = open('original.txt', 'r')
    a = f.read()
    a = receive_information(a)
    if not a:
        print('数值输入错误')
    else:
        a, d = calculation(a)
        screen_division(a)
