from fastapi import FastAPI, Form, Request
from starlette.middleware.sessions import SessionMiddleware 
from fastapi.responses import RedirectResponse, HTMLResponse 
from fastapi.templating import Jinja2Templates
from typing import Annotated
import mysql.connector
con= mysql.connector.connect( user= "root",password= "1234", host= "localhost", database= "website")
mycursor= con.cursor()
app= FastAPI()
app.add_middleware(SessionMiddleware, secret_key= "my_key")
templates= Jinja2Templates(directory= "templates")
@app.post("/signup")
async def sign_up(membername: Annotated[str, Form()], username: Annotated[str, Form()], password: Annotated[str, Form()]):
    mycursor.execute("SELECT * FROM member WHERE username= %s",(username,)) 
    exising_username= mycursor.fetchone()
    if exising_username:
         return RedirectResponse("/error?message=Repeated username", status_code=303)
    mycursor.execute("INSERT INTO member (name, username, password) VALUES(%s,%s,%s)",(membername, username, password))
    con.commit()
    return RedirectResponse("/", status_code=303)    
@app.post("/signin")
async def signin(request: Request, username:Annotated[str, Form()], password: Annotated[str, Form()]):
    mycursor.execute("SELECT id, name FROM member WHERE username= %s AND password= %s",(username, password))
    user_data= mycursor.fetchone()
    if user_data:
        request.session["id"]=user_data[0]
        request.session["name"]=user_data[1]
        request.session["username"]=username
        return RedirectResponse("/member", status_code= 303)
    else:
        return RedirectResponse("/error?message=帳號或密碼錯誤", status_code= 303)    
@app.get("/member", response_class=HTMLResponse)
async def member(request: Request):
    if not request.session.get("id"):
        return RedirectResponse("/", status_code=303)
    membername= request.session.get("name")
    mycursor.execute("SELECT member.name, message.content, message.id FROM message INNER JOIN member ON member.id = message.member_id")
    messages= mycursor.fetchall()   
    return templates.TemplateResponse("member.html", {"request": request, "membername": membername, "messages": messages})   
@app.post("/createMessage", response_class=HTMLResponse)
async def createMessage(request: Request, new_message: Annotated[str, Form()]):
    id=request.session.get("id")
    mycursor.execute("INSERT INTO message(member_id, content)VALUES(%s,%s)",(id,new_message))
    con.commit()
    return RedirectResponse("/member", status_code=303)
@app.post("/deleteMessage", response_class=HTMLResponse)
async def deleteMessage(request: Request, messageId: Annotated[int, Form()]):
    if not request.session.get("id"):  
            return RedirectResponse("/", status_code=303)
    mycursor.execute("DELETE FROM message WHERE id =%s", (messageId,))
    con.commit()    
    return RedirectResponse("/member", status_code=303)    
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html",{"request": request})
@app.get("/error", response_class=HTMLResponse)
async def error(request: Request, message: str= "wrong"):
    return templates.TemplateResponse("error.html", {"request": request, "message": message})
@app.get("/signout")
async def signout(request: Request):
     request.session.clear()
     return RedirectResponse(url= "/") 
@app.get("/returnhome")
async def returnhome():
     return RedirectResponse(url= "/")






