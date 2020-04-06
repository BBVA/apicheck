"""
This file build the docker images
"""
import os
import sys
import uuid
import configparser

HERE = os.path.abspath(os.path.dirname(__file__))

TOOLS_PATH = os.path.join(HERE, "tools")

META_KEYS = ("name", "short-command", "version", "description",
             "home", "author")

DOCKER_HUB_REPO = "bbvalabs"


def main():
    docker_images = dict()

    #
    # Getting README from plugin
    #
    for d in os.listdir(TOOLS_PATH):

        # Get META file
        meta_path = os.path.join(TOOLS_PATH, d, "META")

        try:
            with open(meta_path, "r") as meta_handler:
                cf = configparser.ConfigParser()
                cf.read_string(f"[DEFAULT]\n {meta_handler.read()}")

                meta = dict(cf["DEFAULT"])

                # Check that META contains all needed keys
                if not all(x in meta.keys() for x in META_KEYS):
                    print(f"[!] Missing keys in META \"{d}\". "
                          f"Needed keys: \"{', '.join(META_KEYS)}\"",
                          file=sys.stderr)
                    exit(1)

                #
                # Check that 'name' and 'short-command' are unique
                #
                name = meta["name"]
                version = meta["version"]
                docker_file_path = os.path.join(
                    TOOLS_PATH,
                    d,
                    meta.get("docker-file", "Dockerfile"))

                if not os.path.exists(docker_file_path):
                    print(f"[!] Can't Dockerfile for tool '{name}'",
                          file=sys.stderr)
                    continue

                if name in docker_images.keys():
                    print(f"[!] Tool name '{name}' already exits used "
                          f"for other tool",
                          file=sys.stderr)
                    exit(1)
                else:

                    docker_images[name] = (
                        version,
                        os.path.join(TOOLS_PATH, d),
                        f'./{meta.get("docker-file", "Dockerfile")}'
                    )

        except OSError:
            print(f"[!] Tool \"{d}\" doesnt has README.md file",
                  file=sys.stderr)
            continue

    try:
        docker_user = os.environ["DOCKER_USERNAME"]
    except KeyError:
        print("[!] Environment var 'DOCKER_USERNAME' needed",
              file=sys.stderr)
        exit(1)

    try:
        docker_password = os.environ["DOCKER_PASSWORD"]
    except KeyError:
        print("[!] Environment var 'DOCKER_PASSWORD' needed",
              file=sys.stderr)
        exit(1)

    # Dump password to temporal file
    password_file = f"/tmp/{uuid.uuid4().hex}"
    with open(password_file, "w") as f:
        f.write(docker_password)

    #
    # Build Docker commands
    #
    commands = []

    # Do login
    commands.append(" ".join([
        f"cat {password_file}",
        "|",
        f"docker login --username {docker_user} --password-stdin"
    ]))

    # Add build command for each image
    for image, (version, docker_file_path, docker_file) in docker_images.items():

        # Go to the tool home for each building
        commands.append(f"cd {docker_file_path}")

        # Docker command
        commands.append(" ".join([
            f"docker build",
            f" -t {DOCKER_HUB_REPO}/{image}:{version}",
            f" -t {DOCKER_HUB_REPO}/{image}:latest",
            f" {os.path.dirname(docker_file)}"
        ]))

        commands.append(f"docker push {DOCKER_HUB_REPO}/{image}:{version}")
        commands.append(f"docker push {DOCKER_HUB_REPO}/{image}:latest")

        # Go script base path
        commands.append(f"cd {HERE}")

    # Remove password file
    commands.append(f"rm -rf {password_file}")

    print("\n".join(commands))


if __name__ == '__main__':
    main()