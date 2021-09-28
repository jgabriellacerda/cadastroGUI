import re
emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
dateRegex = r'[0-9]{2}/[0-9]{2}/[0-9]{4}'

def checkEmail(email):
    if re.fullmatch(emailRegex, email):
        return True
    return False;

def checkName(name):
    if len(name):
        return True
    return False

def checkDate(date):
    if re.fullmatch(dateRegex, date):
        return True
    return False
def checkCargo(cargo):
    if len(cargo):
        return True
    return False

