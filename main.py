import subprocess
import json
import hashlib
import argparse


user = "-r jake"

with open('pass.json', 'r') as f:
    data = json.load(f)


def prompt():
    title = input("Title: ")
    desc = input("Desc: ")
    email = input("Email: ")
    password = input("Password: ")
    message = input("Message: ")

    myjson = {
        "title": title,
        "desc": desc,
        "email": email,
        "password": password,
        "message": message
    }

    return myjson


def write_pass():
    message_info = prompt()
    with open(message_info["title"], 'w') as fp:
        json.dump(message_info, fp)
    subprocess.run([
        f"gpg -e {user} --armor {message_info['title']}"],
        shell=True)

    mysave = {
        "title": message_info["title"],
        "desc": message_info["desc"],
    }
    sha = hashlib.sha1(
        (mysave["title"]).encode()
    ).hexdigest()
    mysave["sha"] = sha
    data["entries"].append(mysave)
    with open('pass.json', 'w') as fp:
        json.dump(data, fp)
    shred = input(f"Shred {message_info['title']} [Y/n]: ")
    if shred.upper() == "Y":
        subprocess.run([
            f"shred -u {message_info['title']}"],
            shell=True)


def search_pass(phrase):
    for x in data["entries"]:
        if phrase in x["desc"] or phrase in x["title"]:
            print(f"{x['title']} {x['sha']}\n> {x['desc']}\n")


def read_pass(_hash):
    for x in data["entries"]:
        if _hash == x["sha"]:
            check = subprocess.check_output(
                [f"gpg -d {x['title']}.asc"],
                shell=True).decode("utf-8")
            print(check)


def delete_pass(_hash):
    for x in data["entries"]:
        if _hash == x["sha"]:
            title = x["title"]
            data["entries"].remove(x)
            with open('pass.json', 'w') as fp:
                json.dump(data, fp)
            shred = input(f"Shred {title}.asc [Y/n]: ")
            if shred.upper() == "Y":
                subprocess.run([
                    f"shred -u {title}.asc"],
                    shell=True)


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s")
    parser.add_argument("-r")
    parser.add_argument("-d")
    parser.add_argument("-w", action='store_true')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    command = parse()
    if command.s is not None:
        search_pass(command.s)
    elif command.r is not None:
        read_pass(command.r)
    elif command.d is not None:
        delete_pass(command.d)
    elif command.w:
        write_pass()
