# 將輸入的string分割並分別放入array中
def segment(str):
    # 將不必要的 "(", ")" 去除
    if "(" in str:
        str = str.strip('()')
        str = str.replace('(', '')
        str_arr = str.split(')')

        # 利用 + 分割variable
        for i in range(len(str_arr)):
            str_arr[i] = str_arr[i].replace('-', '+-')
            str_arr[i] = str_arr[i].split('+')
        return str_arr
    else:
        str = str.replace('-', '+-')
        str = str.split('+')
        return str

# 切割係數及變數
def cof_split(str):
    if "*" in str:
        return str.split("*")
    else:
        if "-" in str:
            return [-1 , str.strip('-')]
        else:
            return [1 , str]

# 切割變數及次方項
def exp_split(str):
    if "^" in str:
        # exp[0]=變數, exp[1]=次方項
        exp = str.split("^")

        if len(exp) == 2:
            # 處理xy^2的情況
            if len(exp[0]) == 2:
                var1 = exp[0][0]
                var2 = exp[0][1]
                return [var1, 1, var2, exp[1]]
            # 處理x^2y的情況
            elif exp[1].isdigit() == False:
                var = exp[1][-1]
                exp[1] = exp[1].replace(var, "")
                return [exp[0], exp[1], var, 1]
            # 正常狀況，如x^3
            else:
                return [exp[0], exp[1]]
        
        # 處理x^2y^2的狀況
        elif len(exp) == 3:
            var = exp[1][-1]
            exp[1] = exp[1].replace(var, "")
            return [exp[0], exp[1], var, exp[2]]

    else:
        # 處理xy的情況
        if len(str) == 2:
            return [str[0] , 1, str[1], 1]
        else:
            return [str , 1]
    

# 兩兩配對做處理
def mult(var1, var2):
    var1_cof = cof_split(var1)
    var2_cof = cof_split(var2)

    #係數計算
    cof = str(int(var1_cof[0]) * int(var2_cof[0]))

    var1_exp = exp_split(var1_cof[1])
    var2_exp = exp_split(var2_cof[1])

    # 變數及次方項處理
    var = "variable"
    # 正常情況
    if len(var1_exp) == 2 and len(var2_exp) == 2:
        if var1_exp[0] == var2_exp[0]:
            exp = str(int(var1_exp[1]) + int(var2_exp[1]))
            var = var1_exp[0] + "^"+ exp
        else:
            # 利用ASCII碼排序變數，避免有像yx的狀況出現，造成後續同類項合併的問題
            if ord(var1_exp[0]) < ord(var2_exp[0]):
                var = var1_cof[1] + var2_cof[1]
            else:
                var = var2_cof[1] + var1_cof[1]

    # var1裡面還有兩個變數，像是xy^2或是x^2y這種
    elif len(var1_exp) == 4:
        if var1_exp[0] == var2_exp[0]:
            exp = str(int(var1_exp[1]) + int(var2_exp[1]))
            if var1_exp[3] == 1:
                var = var1_exp[0] + "^"+ exp + var1_exp[2] 
            else:
                var = var1_exp[0] + "^"+ exp + var1_exp[2] + "^" + var1_exp[3]

        elif var1_exp[2] == var2_exp[0]:
            exp = str(int(var1_exp[3]) + int(var2_exp[1]))
            if var1_exp[1] == 1:
                var = var1_exp[0] + var1_exp[2] + "^" + exp
            else:
                var = var1_exp[0] + "^" + var1_exp[1] + var1_exp[2] + "^" + exp
        else:
            # 利用ASCII碼排序變數，避免有像yx的狀況出現，造成後續同類項合併的問題
            if ord(var1_exp[2]) < ord(var2_exp[0]):
                var = var1_cof[1] + var2_cof[1]
            elif ord(var1_exp[0]) < ord(var2_exp[0]):
                if var1_exp[1] == 1 and var1_exp[3] == 1:
                    var = var1_exp[0] + var2_cof[1] + var1_exp[2]
                elif var1_exp[1] == 1:
                    var = var1_exp[0] + var2_cof[1] + var1_exp[2] + "^" + var1_exp[3]
                elif var1_exp[3] == 1:
                    var = var1_exp[0] + "^" + var1_exp[1] + var2_cof[1] + var1_exp[2]
                else:
                    var = var1_exp[0] + "^" + var1_exp[1] + var2_cof[1] + var1_exp[2] + "^" + var1_exp[3]    
            else:
                var = var2_cof[1] + var1_cof[1]

    # var2裡面還有兩個變數，像是xy^2或是x^2y這種
    elif len(var2_exp) == 4:
        if var2_exp[0] == var1_exp[0]:
            exp = str(int(var2_exp[1]) + int(var1_exp[1]))
            if var2_exp[3] == 1:
                var = var2_exp[0] + "^"+ exp + var2_exp[2] 
            else:
                var = var2_exp[0] + "^"+ exp + var2_exp[2] + "^" + var2_exp[3]

        elif var2_exp[2] == var1_exp[0]:
            exp = str(int(var2_exp[3]) + int(var1_exp[1]))
            if var2_exp[1] == 1:
                var = var2_exp[0] + var2_exp[2] + "^" + exp
            else:
                var = var2_exp[0] + "^" + var2_exp[1] + var2_exp[2] + "^" + exp
        else:
            # 利用ASCII碼排序變數，避免有像yx的狀況出現，造成後續同類項合併的問題
            if ord(var2_exp[2]) < ord(var1_exp[0]):
                var = var2_cof[1] + var1_cof[1]
            elif ord(var2_exp[0]) < ord(var1_exp[0]):
                if var2_exp[1] == 1 and var2_exp[3] == 1:
                    var = var2_exp[0] + var1_cof[1] + var2_exp[2]
                elif var2_exp[1] == 1:
                    var = var2_exp[0] + var1_cof[1] + var2_exp[2] + "^" + var2_exp[3]
                elif var2_exp[3] == 1:
                    var = var2_exp[0] + "^" + var2_exp[1] + var1_cof[1] + var2_exp[2]
                else:
                    var = var2_exp[0] + "^" + var2_exp[1] + var1_cof[1] + var2_exp[2] + "^" + var2_exp[3]    
            else:
                var = var1_cof[1] + var2_cof[1]



    # 回傳的字串處理
    if cof == "1":
        return var
    elif cof == "-1":
        return "-" + var
    else:
        return cof + "*" + var

# 同類項合併
def sameVariable(vars):

    totalVariable, output = [], []

    # 先分割所有變數部分並過濾重複的
    for var in vars:
        if "*" in var:
            var = var.split("*")[1]
            if var not in totalVariable:
                totalVariable.append(var)
        elif "-" in var:
            var = var.strip("-")
            if var not in totalVariable:
                totalVariable.append(var)
        else:
            if var not in totalVariable:
                totalVariable.append(var)

    # 合併相同變數的
    for var in totalVariable:
        # 將相同變數的存進cof_arr中
        cof, cof_arr, temp = 0, [], ""

        # 尋找同類項
        for data in vars:  
            if "*" in data:
                temp = data.split("*")[1]
            elif "-" in data:
                temp = data.strip("-")
            else:
                temp = data
            
            if temp == var:
                cof_arr.append(data)

        # 將所有相同變數之係數相加
        for data in cof_arr:
            data = data.replace("*", "")
            data = data.replace(var, "")
            if data == "":
                cof += 1
            elif data == "-":
                cof -= 1
            else:
                cof += int(data)
        
        # 根據係數(cof)的值決定output時的狀況
        if cof == 1:
            output.append(var)
        elif cof == 0:
            pass
        elif cof == -1:
            output.append("-" + var)
        else:
            output.append(str(cof)+ "*" + var)

    return output
        

# 輸入區
print("Input the polynomials: ")
poly = segment(input())
output = "" #output則是輸出要print的東西

while len(poly) >= 2:
    # outcome則是會記錄所有變數互相運算的結果/ output則是輸出要print的東西
    outcomes, output = [], ""

    # 執行運算(每次都是取前兩個list的東西來做運算)
    vars = [] #記錄前兩個list的變數
    for idx in range(2):
        for var in poly[idx]:
            vars.append(var)

    # num紀錄從第幾個變數開始做運算(目的:讓第一陣列的變數不會互相做運算)
    num = len(poly[0])

    for var in poly[0]:
        for idx in range(num,len(vars)):
            outcomes.append(mult(var, vars[idx]))

    outcomes = sameVariable(outcomes)

    # 處理output字串
    for idx, outcome in enumerate(outcomes):
        if idx == 0:
            output += outcome
        else:
            if "-" in outcome:
                output += outcome
            else:
                output += "+" + outcome

    del poly[0:2]
    if len(poly) == 0:
        break
    else:
        output = segment(output)
        poly.insert(0, output)
        print(poly)


# 輸出區
print("Output Result: " + output) 