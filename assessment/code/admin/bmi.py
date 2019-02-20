def bmi(weight,height):
    class A:
        def __init__(self):
            
            self.a = 2
    
    bmi=weight/((height/100)**2)
    a = A()
    if bmi<18.5:    
        return "過輕" 
    elif bmi<24:
        return "正常體重"
    elif bmi<27:
        return "過重"    
    else:
        return a.a  