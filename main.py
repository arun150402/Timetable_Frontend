from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
import jwt
from functools import wraps

app = FastAPI()
SECRET_KEY = 'mistakeisnotamistakeunlessmistaken'
templates = Jinja2Templates(directory="templates")



def token_check(func):
    @wraps(func)
    def decorator(request:Request):
        
        cookies = request.cookies
        if cookies.get('token'):
            token = cookies.get('token')
            if validate_jwt(token):
                if request.url.path == '/student/login' or request.url.path == '/teacher/login':
                    response = RedirectResponse(url='/student/timetable')
                    return response
                return func(request)
        return RedirectResponse(url='/')
    return decorator



def generate_jwt(user_data):
    token = jwt.encode(user_data, SECRET_KEY, algorithm='HS256')
    #print(token)
    return token    


def validate_jwt(token):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        # print(data)
        return True
    except:
        return False



@app.get("/", response_class=HTMLResponse)

def home(request: Request):
   
    response =templates.TemplateResponse("Home.html",{"request": request})
    
    return response
   

@app.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request):
    return templates.TemplateResponse("Admin.html",{"request": request})

@app.route("/student/login",methods=['GET','POST'])
@token_check
async def student_login(request: Request):
    
    if request.method == 'POST':
        data = await (request.form())
        json={
            "username":data['id'],
            "password":data['psw']
        }
        #TODO call api ,success home,failure same
        success=True
        if success:
            token =generate_jwt(json)
            response = RedirectResponse(url='/student/timetable')
            response.set_cookie('token', token)
            return response
        else:
            return templates.TemplateResponse("Student_Login.html",{"request": request}) 

    else:
        return templates.TemplateResponse("Student_Login.html",{"request": request})

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

'''@app.route("/teacher",methods=['GET','POST'])
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
        return templates.TemplateResponse("Teacher_Login.html",{"request": request})'''


@app.get("/student_register", response_class=HTMLResponse)
def student_register(request: Request):
    return templates.TemplateResponse("Student_Registration.html",{"request": request})

@app.get("/teacher_register", response_class=HTMLResponse)
def teacher_call(request: Request):
    return templates.TemplateResponse("Teacher_Registration.html",{"request": request})

@app.route("/student/timetable")
@token_check
def timetable(request: Request):
    return templates.TemplateResponse("TimeTable.html",{"request": request})

@app.route("/student/logout",methods=['GET'])
@token_check
def student_logout(request: Request):
    response = RedirectResponse(url='/')
    response.delete_cookie('token')
    return response