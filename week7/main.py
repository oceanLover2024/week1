from fastapi import FastAPI, Form, Query, Request, Body
from starlette.middleware.sessions import SessionMiddleware 
from fastapi.responses import RedirectResponse, HTMLResponse 
from fastapi.templating import Jinja2Templates
from typing import Annotated
import mysql.connector
import json
def get_mysql():
    con= mysql.connector.connect( user= "root",password= "1234", host= "localhost", database= "website")
    mycursor= con.cursor()
    return con, mycursor
app= FastAPI()
app.add_middleware(SessionMiddleware, secret_key= "my_key")
templates= Jinja2Templates(directory= "templates")
@app.post("/signup")
async def sign_up(membername: Annotated[str, Form()], username: Annotated[str, Form()], password: Annotated[str, Form()]):
    con, mycursor= get_mysql()
    try:
        mycursor.execute("SELECT * FROM member WHERE username= %s",(username,)) 
        exising_username= mycursor.fetchone()
        if exising_username:
            return RedirectResponse("/error?message=Repeated username", status_code=303)
        mycursor.execute("INSERT INTO member (name, username, password) VALUES(%s,%s,%s)",(membername, username, password))
        con.commit()
        return RedirectResponse("/", status_code=303)
    finally:
        mycursor.close()
        con.close()
@app.post("/signin")
async def signin(request: Request, username:Annotated[str, Form()], password: Annotated[str, Form()]):
    con, mycursor= get_mysql()
    try:
        mycursor.execute("SELECT id, name FROM member WHERE username= %s AND password= %s",(username, password))
        user_data= mycursor.fetchone()
        if user_data:
            request.session["id"]=user_data[0]
            request.session["name"]=user_data[1]
            request.session["username"]=username
            return RedirectResponse("/member", status_code= 303)
        else:
            return RedirectResponse("/error?message=帳號或密碼錯誤", status_code= 303)  
    finally:
        mycursor.close()
        con.close()

@app.get("/member", response_class=HTMLResponse)
async def member(request: Request):
    con, mycursor= get_mysql()
    try:
        if not request.session.get("id"):
            return RedirectResponse("/", status_code=303)
        membername= request.session.get("name")
        mycursor.execute("SELECT member.name, message.content, message.id FROM message INNER JOIN member ON member.id = message.member_id")
        messages= mycursor.fetchall()   
        return templates.TemplateResponse("member.html", {"request": request, "membername": membername, "messages": messages})   
    finally:
        mycursor.close()
        con.close()
@app.post("/createMessage", response_class=HTMLResponse)
async def createMessage(request: Request, new_message: Annotated[str, Form()]):
    con, mycursor= get_mysql()
    id=request.session.get("id")
    try:
        mycursor.execute("INSERT INTO message(member_id, content)VALUES(%s,%s)",(id,new_message))
        con.commit()
        return RedirectResponse("/member", status_code=303)
    finally:
        mycursor.close()
        con.close()
@app.post("/deleteMessage", response_class=HTMLResponse)
async def deleteMessage(request: Request, message_id: Annotated[int, Form()]):
    con, mycursor= get_mysql()
    try:
        if not request.session.get("id"):
            return RedirectResponse("/signout", status_code=303)
        mycursor.execute("SELECT member_id FROM message WHERE id = %s", (message_id,))
        member_id= mycursor.fetchone()
        if member_id[0] == request.session.get("id"):
            mycursor.execute("DELETE FROM message WHERE id = %s", (message_id,))
            con.commit()    
            return RedirectResponse("/member", status_code=303)
        else:
            return RedirectResponse("/signout", status_code=303)    
    finally:
        mycursor.close()
        con.close()
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
@app.get("/api/member")
async def api(request: Request,username: Annotated[str,Query]):
    con, mycursor= get_mysql()
    try:
        if not request.session.get("username"):
            return{"data":"null"}
        mycursor.execute("SELECT id, name, username FROM member WHERE username= %s", (username,))   
        user_data= mycursor.fetchone() 
        if user_data:
            return {"data":{"id":user_data[0],"name":user_data[1],"username":user_data[2] }}
        else:
            return{"data":"null"}
    finally:
        mycursor.close()
        con.close()
@app.patch("/api/member")
async def api(request: Request,body: dict= Body(...)):  
    con, mycursor= get_mysql()
    if  not request.session.get("id"):
        return {"error": True}
    else:
        try:
            user_id= request.session.get("id")
            user_name= body.get("name"); 
            mycursor.execute("UPDATE member SET name = %s WHERE id = %s", (user_name, user_id))
            con.commit()
            request.session["name"]= user_name            
            return{"ok": True}
        except:
            return {"error": True}
        finally:
            mycursor.close()
            con.close()