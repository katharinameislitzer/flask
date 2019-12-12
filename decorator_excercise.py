
def restrict_access(func):
    def wrapper(*args, **kwargs):
        name = args[0]
        if name.startswith("K"):
            return "Access Denied"
        else:
            result = func(*args, **kwargs)
        return result
    return wrapper          #funktion ohne klammern

@restrict_access
def treasurebox(username):
    return f"Granted access to {username}"

@restrict_access
def bank_safe(username):
    return f"Granted Access to rich bank safe {username}"

if __name__ == '__main__':
    print (treasurebox("Kathi"))
    print(bank_safe("Paul"))