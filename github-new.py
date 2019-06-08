import argparse
from helpers import cprint, sinput
from json import dump, dumps, load
from os import system, path
from requests import get, post
from sys import exit

CONFIG_PATH = path.join(path.dirname(__file__), "config.txt")


def response_handler(action, response, accepted):
    status = response.status_code
    if status not in accepted:
        msg = response.json()["message"]
        cprint(f"\tError: {action} failed with code {status} ({msg})",
               color="Red")
        exit()
    else:
        cprint(f"\t{action} Status: {status} (Successful)", color="Green")


def create_rep(name, private, token):
    name = input("\tEnter Repository Name: ") if name is None else name

    if private is None:
        private = bool(sinput("\tPrivate (True/False): ", ("true", "false")))

    payload = {"name": name, "private": private, "auto_init": True}

    response = post("https://api.github.com/user/repos",
                    data=dumps(payload),
                    headers={"Authorization": f"token {token}"})

    response_handler("Repository Creation", response, (200, 201))
    return name


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--oauth", type=str, default=None,
                        help=("Use Oauth Token instead of username and "
                              "password credentials"))
    parser.add_argument("-s", "--save", action="store_true",
                        help=("Save the Oauth Token provided by using the o "
                              "flag"))
    parser.add_argument("-c", "--config", action="store_true",
                        help="Alter configs only")
    parser.add_argument("-n", "--name", type=str, default=None,
                        help="Give repository Name")
    parser.add_argument("-p", "--private", type=bool, default=None,
                        help="Sets repository to be Private")
    parser.add_argument("-l", "--local", action="store_true", default=False,
                        help=("Clone the Created Repository to the Local "
                              "Directory"))

    args = parser.parse_args()

    if args.config is True:
        if (not args.name and args.private is not None) or \
           (args.oauth and not args.save):
            cprint("\tError: Cannot Create Repositories in Config Mode",
                   color="Red")
            cprint("\t       Run program without the c flag!", color="Red")
            exit()
    elif args.oauth is None:
        with open(CONFIG_PATH, "r") as c:
            config = load(c)
            args.oauth = config["token"]

    if args.oauth:
        response = get('https://api.github.com/user',
                       headers={'Authorization': f'token {args.oauth}'})
        response_handler("OAUTH Authorization", response, (200,))

        if args.save:
            config = {"token": args.oauth}
            with open(CONFIG_PATH, "w") as c:
                dump(config, c)

        args.name = create_rep(args.name, args.private, args.oauth)

        if args.local:
            username = response.json()["login"]
            system(f"git clone https://github.com/{username}/{args.name}.git")


if __name__ == "__main__":
    try:
        cprint("Ctrl-Z to Exit Program", color="Cyan")
        main()
    except EOFError as e:
        cprint("Encountered End of Program", color="Magenta")
        exit()
