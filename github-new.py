import requests
from getpass import getpass

username = input("Enter your Username for Github : ")
password = getpass()

response = requests.get("https://api.github.com/user",
                        auth=(username, password))

print(f"Authentication Status : {response}")

name = input("Enter Repository Name : ")
private = input("Private (True/False) : ")

reponse = requests.post("https://api.github.com/user/repos",
                        data={"name": name, "private": private})

print(f"Repository Creation Status : {response}")
