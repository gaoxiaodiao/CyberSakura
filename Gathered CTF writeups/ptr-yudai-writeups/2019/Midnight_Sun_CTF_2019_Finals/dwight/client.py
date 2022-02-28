#!/usr/bin/python -Btt

import aux
import json

from dh import DHkey
from protocol import Protocol


class Client(Protocol):

    def send(self, command):
        packet = {
            "command": command,
            "mac": self.mac(command)
        }
        encrypted = self.encrypt(
            json.dumps(packet)
        )
        return encrypted.encode("hex")


if __name__ == "__main__":
    
    try:
        client = Client(DHkey())

        share = client.init_kex()
        aux._write(share)
        client.sharedkey(int(aux._read()))

        aux._write(client.send(
            "echo [redacted] > flag.txt")
        )
        aux._write(client.send("echo bye"))

    except KeyboardInterrupt:
        print(e)
        aux._write("Something went wrong.")
