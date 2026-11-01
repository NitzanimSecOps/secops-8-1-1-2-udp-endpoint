"""Local tester for server.py and client.py - not the hidden grader.

    python3 selftest.py

Copy your server.py and client.py from the previous exercise next to this file first. This creates
a files/ folder with an example file, starts your server.py in the background, and asks for the
file's size over UDP with your file_size, while a TCP client sits connected without sending anything.
"""
import os
import socket
import subprocess
import sys
import time

HOST = "127.0.0.1"
PORT = 2405


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    files = os.path.join(here, "files")
    os.makedirs(files, exist_ok=True)
    with open(os.path.join(files, "hello.txt"), "w") as f:
        f.write("meow\n")

    server = subprocess.Popen([sys.executable, os.path.join(here, "server.py")], cwd=here)
    try:
        time.sleep(1)
        sys.path.insert(0, here)
        from client import file_size

        idle = socket.create_connection((HOST, PORT), timeout=3)
        print("hello.txt - returned", file_size(HOST, PORT, "hello.txt"), "(expected 5)")
        print("missing file - returned", file_size(HOST, PORT, "nope.txt"), "(expected None)")
        idle.close()
    finally:
        server.kill()


if __name__ == "__main__":
    main()
