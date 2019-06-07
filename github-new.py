from getpass import getpass
from helper import sinput
from json import dumps
from requests import get, post

username = input("Username: ")
password = getpass()

response = get("https://api.github.com/user", auth=(username, password))

print(f"Authentication Status : {response.status_code}")

name = input("Enter Repository Name: ")
private = bool(sinput("Private (True/False): ", ("true", "false")))
payload = {"name": name, "private": private, "autoinit": true}

response = post("https://api.github.com/user/repos",
                data=dumps(payload), auth=(username, password))

print(f"Repository Creation Status : {response.status_code}")
