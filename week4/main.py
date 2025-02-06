from fastapi import FastAPI, Form, Request
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware 
from fastapi.responses import RedirectResponse, HTMLResponse 
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import Annotated
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="my_key")
templates= Jinja2Templates(directory="templates")
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html",{"request": request})
@app.get("/member", response_class=HTMLResponse)
async def member(request: Request):#test 
    if not request.session.get("SIGN-IN"):
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse("member.html", {"request": request})
@app.get("/error", response_class=HTMLResponse)
async def error(request: Request, message: str= "wrong"):
    return templates.TemplateResponse("error.html", {"request": request, "message": message})
@app.post("/signin")
async def signin(request: Request, account:Annotated[str, Form()], password: Annotated[str, Form()]):
        if account == "test" and password == "test":
            request.session["SIGN-IN"]= True
            return RedirectResponse("/member", status_code= 303)
        elif not account or not password:
            return  RedirectResponse("/error?message=請輸入帳號與密碼", status_code= 303)
        else:
             return RedirectResponse("/error?message=帳號或密碼錯誤", status_code=303)
@app.get("/signout")
async def signout(request: Request):
     request.session.clear()
     return RedirectResponse(url= "/") 


@app.get("/square/{num}")
async def square(num, request:Request):
    num= int(num)
    ans= num* num
    return templates.TemplateResponse("square.html", {"request":request, "ans":ans})
