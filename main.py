from pathlib import Path
from fastapi import FastAPI, File, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import jwt
from functools import wraps
from starlette import status
from fastapi.staticfiles import StaticFiles
import requests

import pandas
from constants import *
from io import BytesIO


# star = Starlette(routes=routes)
app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")

SECRET_KEY = "mistakeisnotamistakeunlessmistaken"
templates = Jinja2Templates(directory="templates")


def token_check(func):
    @wraps(func)
    async def decorator(request: Request):

        cookies = request.cookies
        if cookies.get("token"):
            token = cookies.get("token")
            if validate_jwt(token):
                if request.url.path == "/student/login" or request.url.path == "/admin/login":
                    response = RedirectResponse(url="/student/timetable")
                    return response
                return func(request)
        else:
            print(request.url.path)
            if request.url.path == "/student/login" or request.url.path == "/admin/login":
                return await func(request)
        return RedirectResponse(url="/")

    return decorator


def generate_jwt(user_data):
    token = jwt.encode(user_data, SECRET_KEY, algorithm="HS256")
    # print(token)
    return token


def validate_jwt(token):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return True
    except:
        return False


def token_to_data(token):

    data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

    return data


@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    response = templates.TemplateResponse("Home.html", {"request": request})

    return response


@app.get("/admin", response_class=HTMLResponse)
@token_check
def admin_page(request: Request):
    return templates.TemplateResponse("Admin.html", {"request": request})


@app.route("/student/login", methods=["GET", "POST"])
@token_check
async def student_login(request: Request):

    if request.method == "POST":
        data = await (request.form())

        login_data = {"email": data["id"], "password": data["psw"]}

        response = requests.post(STUDENT_LOGIN_ENDPOINT, json=login_data)
        response_json = response.json()
        isSuccess = response_json["success"]
        if isSuccess:
            token = generate_jwt(response_json["user"])
            response = RedirectResponse(
                url="/student/timetable", status_code=status.HTTP_302_FOUND
            )
            response.set_cookie("token", token)
            return response
        else:
            return templates.TemplateResponse("Student_Login.html", {"request": request})

    else:
        return templates.TemplateResponse("Student_Login.html", {"request": request})


# @app.route("/teacher/login",methods=['GET','POST'])
# def teacher_login(request: Request):
#     if request.method == 'POST':
#         data = (request.form())
#         print(data)
#         #TODO call api ,success home,failure same
#         success=False
#         if success:
#             return templates.TemplateResponse("Home.html",{"request":request})
#         else:
#             return templates.TemplateResponse("Teacher_Login.html",{"request": request})

#     else:
#         return templates.TemplateResponse("Teacher_Login.html",{"request": request})

"""@app.route("/teacher",methods=['GET','POST'])
def teacher_login(request: Request):
    if request.method == 'POST':
        data = (request.form())
        print(data)
        #TODO call api ,success home,failure same
        success=False
        if success:
            return templates.TemplateResponse("Home.html",{"request":request})
        else:
            return templates.TemplateResponse("Teacher_Login.html",{"request": request}) 

    else:
        return templates.TemplateResponse("Teacher_Login.html",{"request": request})"""


@app.route("/student/register", methods=["GET", "POST"])
@token_check
async def student_register(request: Request):
    if request.method == "POST":
        data = await (request.form())
        print(data)
        pass
    return templates.TemplateResponse("Student_Registration.html", {"request": request})


@app.get("/teacher_register", response_class=HTMLResponse)
def teacher_register(request: Request):

    return templates.TemplateResponse("Teacher_Registration.html", {"request": request})


@app.route("/student/timetable")
@token_check
def timetable(request: Request):
    student_data = token_to_data(request.cookies.get("token"))
    request_url = (
        GET_TIMETABLE_ENDPOINT
        + "/%22"
        + student_data["std"]
        + "%22/%22"
        + student_data["section"]
        + "%22"
    )
    response = requests.get(request_url)
    timetable = response.json()
    return templates.TemplateResponse(
        "TimeTable.html", {"request": request, "timetable": timetable["timetable"]}
    )


@app.route("/admin/login", methods=["GET", "POST"])
@token_check
async def admin_login(request: Request):
    if request.method == "POST":
        data = await (request.form())
        if data["id"] == "admin" and data["psw"] == "admin":
            token = generate_jwt({"id": data["id"], "password": data["psw"]})

            response = RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)
            response.set_cookie("token", token)
            return response
        return templates.TemplateResponse("Admin_Login.html", {"request": request})
    else:
        return templates.TemplateResponse("Admin_Login.html", {"request": request})


@app.post("/admin/upload")
def upload(request: Request, file: bytes = File(...)):
    df = pandas.read_csv(BytesIO(file))
    resp = requests.post(
        "http://middle.npc203.ml/admin/upload_csv", json=df.to_json()
    )  # TODO remove HARCODED URL
    return str(resp.status_code)


@app.route("/teacher/login")
def teacher_login(request: Request):
    return templates.TemplateResponse("Teacher_Login.html", {"request": request})


@app.route("/student/logout", methods=["GET"])
@token_check
def student_logout(request: Request):
    response = RedirectResponse(url="/")
    response.delete_cookie("token")
    return response


@app.route("/admin/logout", methods=["GET"])
@token_check
def admin_logout(request: Request):
    response = RedirectResponse(url="/")
    response.delete_cookie("token")
    return response
