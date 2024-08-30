#!/usr/bin/env python3
import argparse
import shlex
import subprocess
import time


def _sp(*cmd, check=True):
    print("$ " + shlex.join(cmd))
    return subprocess.run(cmd, check=check)


IMAGE = "images:nixos/24.05"
NAME = "test"
CPUS = 12
MEM_GB = 2


def launch(name, configuration):
    _sp("incus", "launch",
        IMAGE,
        name,
        "--vm",
        "-c", "security.secureboot=false",
        "-c", f"limits.cpu={CPUS}",
        "-c", f"limits.memory={MEM_GB}GiB")
    wait(name)
    push_config(name, configuration)


def wait(name):
    while _sp("incus", "exec", name, "--", "uptime", check=False).returncode != 0:
        print("Waiting for agent...")
        time.sleep(5)


def pull_config(name, config_nix_out):
    _sp("incus", "file", "pull",
        f"{name}/etc/nixos/configuration.nix",
        config_nix_out)


def push_config(name, config_nix_in):
    _sp("incus", "file", "push",
        config_nix_in,
        f"{name}/etc/nixos/configuration.nix")
    rebuild(name)


def rebuild(name):
    _sp("incus", "exec", name, "--", "bash", "-l", "-c", "nixos-rebuild switch")


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True)

    subparser = subparsers.add_parser("launch")
    subparser.set_defaults(func=launch)
    subparser.add_argument("name")
    subparser.add_argument("configuration")

    subparser = subparsers.add_parser("wait")
    subparser.set_defaults(func=wait)
    subparser.add_argument("name")

    subparser = subparsers.add_parser("pull_config")
    subparser.set_defaults(func=pull_config)
    subparser.add_argument("name")
    subparser.add_argument("config_nix_out")

    subparser = subparsers.add_parser("push_config")
    subparser.set_defaults(func=push_config)
    subparser.add_argument("name")
    subparser.add_argument("config_nix_in")

    args = parser.parse_args()
    args = vars(args)
    func = args.pop("func")
    func(**args)


if __name__ == "__main__":
    main()
