import io
import json
import sys
import os
import re
import time
import inspect
import logger
import threading
from relay import relay
from datetime import datetime
from collections import OrderedDict

# from realay import controller as c

logging = logger.Logger()
logging.setLevel(logger.INFO)


class Service:
    controller = None
    relays = None
    root = os.path.dirname(inspect.getfile(lambda: None))

    def __init__(self):
#        self.controller = c.Controller()

        # 1 2 3 4 5 6 7 8 9 * 0 #
        self.relays = [relay.Relay(2),
                       relay.Relay(3),
                       relay.Relay(4),
                       relay.Relay(17),
                       relay.Relay(27),
                       relay.Relay(22),
                       relay.Relay(10),
                       relay.Relay(9),
                       relay.Relay(11),
                       relay.Relay(5),
                       relay.Relay(6),
                       relay.Relay(13)]

        return

    def test(self):
        for relay in self.relays:
            relay.on()
            time.sleep(0.25)
            relay.off()

    def tail(self):
         yield logging.tail()
