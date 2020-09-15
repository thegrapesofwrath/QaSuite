def captureExceptions(func):
    def wrapper(*args,**kwargs):
        try:
           return func(*args,**kwargs)
        except Exception as e:
            return e