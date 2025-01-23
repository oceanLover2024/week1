import csv
import json
import urllib.request as request
src1="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
src2="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"
with request.urlopen(src2)as response2:
    data2= json.load(response2)
mrtList=data2["data"]

def findDistrict(num):
    for mrt in mrtList:
        districtList={mrt["SERIAL_NO"]:mrt["address"][5:8]}    
        if num in districtList:
            return(districtList[num]) 

with request.urlopen(src1)as response:
    data= json.load(response)
attractionsList=data["data"]["results"]

with open("spot.csv", mode="w", newline="", encoding="utf-8")as file:
    writer=csv.writer(file)
    for attraction in attractionsList:
        num=attraction["SERIAL_NO"]
        writer.writerow([attraction["stitle"], findDistrict(num), attraction["longitude"], attraction["latitude"],"https"+attraction["filelist"].split("https")[1]])

def findSerial(num):
    for a in attractionsList:
        if a["SERIAL_NO"] == num:
           return(a["stitle"])   

total=[]
for station in mrtList:
    stationList={"mrt":station["MRT"],"serial":findSerial(station["SERIAL_NO"])}
    total.append(stationList)
newList={}
for t in total:
    mrt= t["mrt"]
    serial=t["serial"]
    if mrt in newList:
        newList[mrt].append(serial)
    else:
        newList[mrt]= [serial]
processedList={}
for key,value in newList.items():
    processedList[key]= ", ".join(value) 

with open("mrt.csv", mode="w", newline="", encoding="utf-8")as file2:
    for key,value in processedList.items():
        answer=f"{key},{value}\n"
        file2.write(answer)
        
   
       
    
        



     
           
    