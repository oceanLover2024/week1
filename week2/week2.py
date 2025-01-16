def find_and_print(messages, current_station):
# your code here
    mrt={   
    "Xindian": 0,
    "Xindian City Hall": 1,
    "Qizhang": 2,
    "Xiaobitan": 2,
    "Dapingling": 3,
    "Jingmei": 4,
    "Wanlong": 5,
    "Gongguan": 6,
    "Taipower Building": 7,
    "Guting": 8,
    "Chiang Kai-Shek Memorial Hall": 9,
    "Xiaonanmen": 10,
    "Ximen": 11,
    "Beimen": 12,
    "Zhongshan": 13,
    "Shongjiang Nanjing": 14,
    "Nanjing Fuxing": 15,
    "Taipei Arena": 16,
    "Nangjing Sanmin": 17,
    "Songshan": 18
    }
    myPoint= mrt[current_station]
    nearFriend= None
    short= float('inf')
    for name, talk in messages.items():
        for station in mrt:#for是取得字典的key值
            if station in talk:
                friendPoint= mrt[station]                
                distance= abs(myPoint-friendPoint)
                if station== "Xiaobitan":
                    distance= abs(myPoint-friendPoint)+1
                if distance < short:
                    short= distance
                    nearFriend= name
    if nearFriend:
        print(nearFriend) 

             
messages={
"Leslie":"I'm at home near Xiaobitan station.",
"Bob":"I'm at Ximen MRT station.",
"Mary":"I have a drink near Jingmei MRT station.",
"Copper":"I just saw a concert at Taipei Arena.",
"Vivian":"I'm at Xindian station waiting for you."
} 

find_and_print(messages, "Wanlong") # print Mary
find_and_print(messages, "Songshan") # print Copper
find_and_print(messages, "Qizhang") # print Leslie
find_and_print(messages, "Ximen") # print Bob
find_and_print(messages, "Xindian City Hall") # print Vivian

#分隔線 以下是Task2
print("==============================================")
# your code here, maybe
#建立一個顧問時間表的字典
schedule={ "John": [], "Bob": [], "Jenny": []}
def book(consultants, hour, duration, criteria):
# your code here
#定義一個函式來檢查顧問是否有空堂,若有,把時間加入shedule物件中,並回傳是哪個顧問有空
    def available(name, hour, duration):
        for s in schedule[name]:#取出顧問的時段來做比較
            start, end= s
            if hour < end and (hour+duration) > start:
                return None
        schedule[name].append((hour, hour+duration))
        return name
#比較price跟rate,調整遍歷顧問空堂的順序
    def getPrice(x):
        return x["price"]
    def getRate(x):
        return x["rate"]
    if criteria == "price":
        consultants.sort(key= getPrice)
    elif criteria == "rate":
        consultants.sort(key= getRate, reverse= True)
#遍歷所有顧問,呼叫 是否有空 的函式,把函式傳入參數算出結果,印出結果
    for c in consultants:
        result= available(c["name"], hour, duration)
        if result:
            print(result)
            return
    print("No Service")
consultants=[
    {"name":"John", "rate":4.5, "price":1000},
    {"name":"Bob", "rate":3, "price":1200},
    {"name":"Jenny", "rate":3.8, "price":800}
]
book(consultants, 15, 1, "price") # Jenny
book(consultants, 11, 2, "price") # Jenny
book(consultants, 10, 2, "price") # John
book(consultants, 20, 2, "rate") # John
book(consultants, 11, 1, "rate") # Bob
book(consultants, 11, 2, "rate") # No Service
book(consultants, 14, 3, "price") # John

#分隔線 以下是Task3
print("===========================================")
def func(*data):
# your code here
    realName=list(data)   
    name=[] 
    result=[] 
    for middle in data:           
        if len(middle)==2:
            middle=middle[1:]
        elif len(middle)==3:
            middle=middle[1:]
        else: 
            middle=middle[2:]
        middle=set(middle)    
        name.append(middle)
    for i in range(len(name)):
        same=False
        for j in range(len(name)):
            if i!=j and (name[i]&name[j]):
                same=True
                break
        if same==False:  
            result.append(realName[i])
        
    if len(result)>0 :
        print(''.join(result))
    else:
        print("沒有")  

func("彭大牆", "陳王明雅", "吳明") # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花") # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆") # print 夏曼藍波安

#分隔線 以下是Task3
print("===========================================")
def get_number(index):
# your code here
    answer=0
    for i in range(index+1):
        if i==0:
            answer+=0
        elif i%3 !=0:
            answer+=4
        else:
            answer-=1 
    print(answer)
get_number(1) # print 4
get_number(5) # print 15
get_number(10) # print 25
get_number(30) # print 70