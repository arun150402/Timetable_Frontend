def check(func):
    def inside(a,b):
        if b == 0:
            print("cant divide")
            return
        func(a,b)
    return inside

@check
def div(a,b):
    print(a/b)

div(10,9)