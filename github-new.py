import argparse
from json import dump, dumps, load
from requests import get, post
from sys import exit


def response_handler(action, response, accepted):
    status = response.status_code
    if status not in accepted:
        msg = response.json()["message"]
        print(f"Error {action} failed with code {status} ({msg})")
        exit()
    else:
        print(f"{action} Status: {status} (Successful)")


def create_rep(name, private, token):
    name = input("Enter Repository Name: ") if name is None else name

    if private is None:
        private = bool(sinput("Private (True/False): ", ("true", "false")))

    payload = {"name": name, "private": private, "autoinit": true}

    response = post("https://api.github.com/user/repos",
                    data=dumps(payload),
                    header={"Authorization": f"token {token}"})

    response_handler("Repository Creation", response, (200, 201))


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
    parser.add_argument("-p", "--private", action="store_true", default=False,
                        help="Sets repository to be Private")

    args = parser.parse_args()

    print(args.private)
    if args.config is False:
        pass

    if args.oauth is None:
        with open("config.txt", "r") as c:
            config = load(c)
            args.oauth = config["token"]

    if args.oauth:
        response = get('https://api.github.com/user',
                       headers={'Authorization': f'token {args.oauth}'})
        response_handler("OAUTH Authorization", response, (200,))
        if args.save:
            config = {"token": args.oauth}
            with open("config.txt", "w") as c:
                dump(config, c)

        create_rep(args.name, args.private, args.oauth)


if __name__ == "__main__":
    main()
