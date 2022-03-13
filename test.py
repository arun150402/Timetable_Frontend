import requests as req
data = {
    "email":"19eucs107@skcet.ac.in",
    "password":"12345"
}
x = req.get('http://20.62.141.224/students/timetable/%22I%22/%22A%22')

print(x.text)