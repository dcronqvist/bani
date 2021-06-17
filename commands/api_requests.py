import logging
import requests as req
import config as conf

def read_token():
    token_file = "token"
    with open(token_file, "r") as f:
        return f.read()

def save_token(token):
    token_file = "token"
    with open(token_file, "w") as f:
        f.write(token)

def get_new_token():
    username = conf.get_setting("restberry-api-username")
    password = conf.get_setting("restberry-api-password")

    result = req.post("https://api.dcronqvist.se/v1/auth/login", json={ "username": username, "password": password })

    save_token(result.json()["token"]["token"])
    return read_token()

def use_token(func):
    def wrapper(*args, **kwargs):
        result = req.get("https://api.dcronqvist.se/v1/pihole/status")

        if result.status_code == 200:
            return func(*args, **kwargs)    
        else:
            get_new_token()
            return func(*args, **kwargs)  

    wrapper.__name__ = func.__name__
    return wrapper

