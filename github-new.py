import argparse
from helpers import cprint, sinput
from json import dump, dumps, load
from os import system, path
from requests import get, post
from sys import exit

CONFIG_PATH = path.join(path.dirname(__file__), "config.txt")


# Basic Response Handler
# Limits the number of accepted response codes
def response_handler(action, response, accepted):
    status = response.status_code
    if status not in accepted:
        msg = response.json()["message"]
        cprint(f"\tError: {action} failed with code {status} ({msg})",
               color="Red")
        exit()
    else:
        cprint(f"\t{action} Status: {status} (Successful)", color="Green")


# Uses oauth token to create a repo
# on github
# Auto Initializes the repo with README.MD
# Returns Name as the main function
# will not have access to the name
# if not included in command line argument
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

    # Don't Read the Config File in Config Mode
    # (ONLY WRITE IN THIS MODE)
    if args.config is True:
        # Don't allow repository creation data
        # to be passed into th program in
        # Config mode
        if (not args.name and args.private is not None) or \
           (args.oauth and not args.save):
            cprint("\tError: Cannot Create Repositories in Config Mode",
                   color="Red")
            cprint("\t       Run program without the c flag!", color="Red")
            exit()
    elif args.oauth is None:
        # Read the config file for token
        # if user hasn't provided token
        # as a command line argument
        with open(CONFIG_PATH, "r") as c:
            config = load(c)
            args.oauth = config["token"]

    if args.oauth:
        # Make sure the token provided actually works
        response = get('https://api.github.com/user',
                       headers={'Authorization': f'token {args.oauth}'})
        response_handler("OAUTH Authorization", response, (200,))

        if args.save:
            # Write token to save file if s flag is included
            config = {"token": args.oauth}
            with open(CONFIG_PATH, "w") as c:
                dump(config, c)

        args.name = create_rep(args.name, args.private, args.oauth)

        if args.local:
            # Clone repo if the local flag is included
            username = response.json()["login"]
            system(f"git clone https://github.com/{username}/{args.name}.git")


if __name__ == "__main__":
    try:
        cprint("Ctrl-Z to Exit Program", color="Cyan")
        main()
    except EOFError as e:
        # Don't do anything for EOFError
        # that is passed in when Ctrl-Z
        # is passed in as input
        pass
    finally:
        cprint("Encountered End of Program", color="Magenta")
        exit()
