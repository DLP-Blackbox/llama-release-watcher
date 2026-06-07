#!/usr/bin/env python3
import os
import sys

import requests

UPSTREAM_REPO = "ggerganov/llama.cpp"
VERSION_FILE = "last_release_version.txt"


def write_github_output(name: str, value: str) -> None:
    github_output = os.environ.get("GITHUB_OUTPUT")
    if not github_output:
        return
    with open(github_output, "a", encoding="utf-8") as handle:
        handle.write(f"{name}={value}\n")


def get_latest_release_tag() -> str:
    url = f"https://api.github.com/repos/{UPSTREAM_REPO}/releases/latest"
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    return response.json()["tag_name"]


def get_last_version() -> str | None:
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, encoding="utf-8") as handle:
            return handle.read().strip() or None
    return None


def main() -> None:
    try:
        latest_tag = get_latest_release_tag()
        last_tag = get_last_version()

        print(f"Latest upstream tag: {latest_tag}")
        print(f"Last seen tag: {last_tag}")

        if latest_tag != last_tag:
            print(f"New release detected: {latest_tag}!")
            write_github_output("new_release", "true")
            write_github_output("release_tag", latest_tag)
        else:
            print("No new release detected.")
            write_github_output("new_release", "false")
            write_github_output("release_tag", "")

    except Exception as exc:
        print(f"Error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
