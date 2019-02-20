def bmi(weight, height):
    bmi=weight/((height/100)**2)
    if bmi<18.5:    
        return "過輕" 
    elif bmi<24:
        return "正常體重"
    elif bmi<27:
        return "過重"    
    else:
        return "肥胖"  