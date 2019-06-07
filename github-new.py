from getpass import getpass
from requests import get, post

username = input("Username : ")
password = getpass()

response = get("https://api.github.com/user", auth=(username, password))

print(f"Authentication Status : {response}")

name = input("Enter Repository Name : ")
private = input("Private (True/False) : ")

reponse = post("https://api.github.com/user/repos",
               data={"name": name, "private": private})

print(f"Repository Creation Status : {response}")
