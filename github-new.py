from sys import exit
from getpass import getpass
from helper import sinput
from json import dumps
from requests import get, post


def response_handler(action, response, accepted):
    status = response.status_code
    if status not in accepted:
        msg = response.json()["message"]
        print(f"Error {action} failed with code {status} ({msg})")
    else:
        print(f"{action} Status: {status}")


def easy_mode():
    username = input("Username: ")
    password = getpass()

    response = get("https://api.github.com/user", auth=(username, password))

    response_handler("Authentication", response, (200))

    name = input("Enter Repository Name: ")
    private = bool(sinput("Private (True/False): ", ("true", "false")))
    payload = {"name": name, "private": private, "autoinit": true}

    response = post("https://api.github.com/user/repos",
                    data=dumps(payload), auth=(username, password))

    response_handler("Repository Creation", response, (200, 201))


def main():
    easy_mode()

if __name__ == "__main__":
    main()
