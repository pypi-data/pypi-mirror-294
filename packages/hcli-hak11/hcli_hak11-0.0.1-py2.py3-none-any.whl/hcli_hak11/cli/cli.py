import json
import io
import os
import inspect
import sys
import io
import service


class CLI:
    commands = None
    inputstream = None
    service = None

    def __init__(self, commands, inputstream):
        self.commands = commands
        self.inputstream = inputstream
        self.service = service.Service()

    def execute(self):

        if len(self.commands) == 1:
            self.service.test()
            return None

        # a named job
        elif self.commands[1] == "admin":
            return None

        elif self.commands[1] == "logs":
            return self.service.tail()

        return None
