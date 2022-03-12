from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_item(request: Request):
    return templates.TemplateResponse("Home.html",{"request": request})

@app.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request):
    return templates.TemplateResponse("Admin.html",{"request": request})

@app.route("/student",methods=['GET','POST'])
def student_login(request: Request):
    if request.method == 'POST':
        data = (request.form())
        print(data)
        #TODO call api ,success home,failure same
        success=False
        if success:
            return templates.TemplateResponse("Home.html",{"request":request})
        else:
            return templates.TemplateResponse("Student_Login.html",{"request": request}) 

    else:
        return templates.TemplateResponse("Student_Login.html",{"request": request})

@app.route("/teacher",methods=['GET','POST'])
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
        return templates.TemplateResponse("Teacher_Login.html",{"request": request})

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




