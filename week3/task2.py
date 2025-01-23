import urllib.request as req
import bs4
import csv
def time(entry):
    request= req.Request(entry, headers={
        "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36",
        "cookie":"over18=1"})
    with req.urlopen(request)as response:
        entryData= response.read().decode("utf-8")
    entryRoot= bs4.BeautifulSoup(entryData, "html.parser")
    entryValue= entryRoot.find_all("span", class_= "article-meta-value")
    if len(entryValue)>=4:
        return entryValue[3].text
    else:
        return "無"

def getData(url):
    request= req.Request(url, headers={
        "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36",
        "cookie":"over18=1"})
    with req.urlopen(request)as response:
        data= response.read().decode("utf-8")

    root= bs4.BeautifulSoup(data, "html.parser")
    articals= root.find_all("div", class_= "r-ent") 
       
    for a in articals:
        title= a.find("div", class_= "title")
        if title.a!= None:
            title=title.a.string
        else:
            continue
        popular= a.find("div", class_= "nrec")
        if popular and popular.span:
            popular= popular.span.text
        else:
            popular=0
        entry= a.find("a")
        if entry:
            entry= "https://www.ptt.cc"+entry["href"]
        realTime= time(entry)
        answer= f"{title},{popular},{realTime}"
        answers.append(f"{answer}")
    
        
    
    nextLink= root.find("a", string= "‹ 上頁")
    return nextLink["href"]
answers= []

pageUrl="https://www.ptt.cc/bbs/Lottery/index.html"
count=1
while count<=3:
    pageUrl= "https://www.ptt.cc"+ getData(pageUrl)
    count+=1
with open("article.csv", mode="w", encoding="utf-8")as file:
        for result in answers:
            file.write(result)
            file.write("\n")

