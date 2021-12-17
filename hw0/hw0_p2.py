# 讀取Excel檔
with open('./IMDB-Movie-Data.csv', newline='') as csvfile:
    # myKey存入要當dictionary的key, myDict則是存放所有dict的list
    myKey, myDict = [], []

    totalData = csvfile.read()
    # 先將每個row分隔出來並刪除最後一個空list
    rows = totalData.split('\r\n')
    rows.pop()

    # 個別製作每個row的字典並存放進myDict
    for idx, row in enumerate(rows):
        if idx == 0:
            myKey = row.split(',')
        else:
            dict = {}

            # 連續出現兩個","代表該格沒有值，所以直接賦予其為0
            row = row.replace(',,', ',0,')
            data = row.split(',')
            for idx, value in enumerate(myKey):
                    dict[value] = data[idx]

            # 傳回myDict        
            myDict.append(dict)


# Question 1  
print("Q1: Top-3 movies with the highest ratings in 2016?")
# top1~3的資訊
top1, top2, top3 = ["movie_title", 0.0], ["movie_title", 0.0], ["movie_title", 0.0]

for data in myDict:
    if data["Year"] == "2016":
        title = data["Title"]
        rating = float(data["Rating"])

        # 比rating大小
        if rating > top1[1]:
            top1[0] = title
            top1[1] = rating
        elif rating > top2[1]:
            top2[0] = title
            top2[1] = rating
        elif rating > top3[1]:
            top3[0] = title
            top3[1] = rating

print("A1: %s, %s, %s." % (top1[0], top2[0], top3[0]))


# Question 2   
print("Q2: The actor generating the highest average revenue?")
myActor, topRevenue = [], ["actor_name", 0]

# 收集所有Actor的名字
for data in myDict:

    actors = data["Actors"].split("|")
    for newActor in actors:
        newActor = newActor.strip(" ")
        if len(myActor) == 0:
            myActor.append(newActor)
        else:
            for existActor in myActor:
                if existActor == newActor:
                    break
            else:
                myActor.append(newActor)

# 收集所有Actor的平均收益，並將目前最高平均收益的資料記錄在 topRevenue中
for actor in myActor:

    # 用來記錄目前的總收益及電影出演次數
    totalRevenue, times = 0.0, 0.0

    for data in myDict:
        if actor in data["Actors"]:
            if data["Revenue (Millions)"] == "0":
                pass
            else:
                totalRevenue += float(data["Revenue (Millions)"])
            times += 1
    
    averageRevenue = totalRevenue/times;
    if  averageRevenue > topRevenue[1]:
        topRevenue[0] = actor
        topRevenue[1] = averageRevenue

print("A2: %s. His average revenue is %.2f." % (topRevenue[0], topRevenue[1]))


# Question 3   
print("Q3: The average rating of Emma Watson’s movies?")
totalRating, times = 0.0, 0.0    

# 先加總所有Emma Watson出演過的電影評分再去平均
for data in myDict:
    if "Emma Watson" in data["Actors"]:
        totalRating += float(data["Rating"])
        times += 1

averageRating = totalRating/times
print("A3: %.2f" % averageRating)


# Question 4   
print("Q4: Top-3 directors who collaborate with the most actors?")
myDirector, top1, top2, top3 = [], [ "director_name", 0 ], [ "director_name", 0 ], [ "director_name", 0 ]

# 收集所有director的名字
for data in myDict:

    director = data["Director"]

    if len(myDirector) == 0:
        myDirector.append(director)
    else:
        for existDirector in myDirector:
            if existDirector == director:
                break
        else:
            myDirector.append(director)

# 收集各個director合作過的演員名字
for director in myDirector:

    # 用來記錄演員名字
    hisActors = []

    for data in myDict:
        if director == data["Director"]:
            actors = data["Actors"].split("|")

            if len(hisActors) == 0:
                for newActor in actors:
                    newActor = newActor.strip(" ")
                    hisActors.append(newActor)
            else:
                for newActor in actors:
                    if newActor in hisActors:
                        pass
                    else:
                        hisActors.append(newActor)
    
    # 比較合作演員數大小
    if len(hisActors) > top1[1]:
        top1[0] = director
        top1[1] = len(hisActors)
    elif len(hisActors) > top2[1]:
        top2[0] = director
        top2[1] = len(hisActors)
    elif len(hisActors) > top3[1]:
        top3[0] = director
        top3[1] = len(hisActors)

# print("A4: %s, %s and %s." % (top1[0], top2[0], top3[0]))
print("A4: %s(%d), %s(%d) and %s(%d)." % (top1[0], top1[1], top2[0], top2[1], top3[0], top3[1]))


# Question 5   
print("Q5: Top-2 actors playing in the most genres of movies?")
top1, top2 = [ "actor_name", 0 ], [ "actor_name", 0 ]

# 收集每個演員演過的電影種類
for actor in myActor:

    # 用來記錄目前的總收益及電影出演次數
    totalGenre = [] 

    for data in myDict:
        if actor in data["Actors"]:
            genres = data["Genre"].split("|")
            if len(totalGenre) == 0:
                for genre in genres:
                    totalGenre.append(genre)
            else:
                for genre in genres:
                    if genre not in totalGenre:
                        totalGenre.append(genre)
    
    # 比較合作演員數大小
    if len(totalGenre) > top1[1]:
        top1[0] = actor
        top1[1] = len(totalGenre)
    elif len(totalGenre) > top2[1]:
        top2[0] = actor
        top2[1] = len(totalGenre)    
            
print("A5: %s(%d) and %s(%d)." % (top1[0], top1[1], top2[0], top2[1]))


# Question 6   
print("Q6: All actors whose movies lead to the largest maximum gap of years?")
top, maxGapList = [ "actor_name", 0 ], []

# 收集所有演員參與過的電影年份，利用sort排序再相減頭尾
for actor in myActor:

    # 用來記錄參與電影的年份
    totalyear = [] 

    for data in myDict:
        if actor in data["Actors"]:
            totalyear.append(int(data["Year"])) 
    
    totalyear.sort()
    gap = totalyear[-1] - totalyear[0]

    # 比較合作演員數大小
    if gap > top[1]:
        top[0] = actor
        top[1] = gap

# 找出所有最大gap year的演員
for actor in myActor:
    # 用來記錄參與電影的年份
    totalyear = [] 

    for data in myDict:
        if actor in data["Actors"]:
            totalyear.append(int(data["Year"])) 
    
    totalyear.sort()
    gap = totalyear[-1] - totalyear[0]

    if gap == top[1]:
        maxGapList.append(actor)

print("A6: 最大GAP YEAR的演員共有%d個" % len(maxGapList))
print(maxGapList)


# Question 7   
print("Q7: Find all actors who collaborate with Johnny Depp in direct and indirect ways.")
# 將所有和Johnny Depp存入totalActor
totalActor = ["Johnny Depp"]

# 找和Johnny Depp有直接關係的
for data in myDict:
    if "Johnny Depp" in data["Actors"]:
        actors = data["Actors"].split("|")

        for actor in actors:
            actor = actor.strip(" ")
            if actor not in totalActor:
                totalActor.append(actor)

# 找和Johnny Depp有間接關係的
# num1會放入上一次的list長度，num2存入現在的，當兩者相等時，代表不再將有間階關係的人漏掉
num1 = 1
num2 = len(totalActor)
while num1 < num2:
    # 用每筆電影的演員名稱去核對是否有出現在totalActor裡
    for data in myDict:
        for idx in range(num1, num2):
            if totalActor[idx] in data["Actors"]:
                actors = data["Actors"].split("|")

                for actor in actors:
                    actor = actor.strip(" ")
                    if actor not in totalActor:
                        totalActor.append(actor)
                # 已將這部電影有關係的演員加入totalActor內      
                break
            

    # 每做完一次更新num1, num2
    num1 = num2 
    num2 = len(totalActor)

# 最後刪掉Johnny Depp自己
totalActor.pop(0)    

print("A7: 總共有%d個演員和Johnny Depp有關係~~" % len(totalActor))          
print(totalActor)