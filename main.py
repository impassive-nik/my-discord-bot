#!/usr/bin/env python3

import sys
import os
from my_bot import DiscordWrapper, SingleOwnerPermission

if len(sys.argv) not in range(2, 4):
  print("Error: unexpected number of arguments", file=sys.stderr)
  #TODO: accept the token via environment variables?
  sys.exit(1)

client = DiscordWrapper(admin = SingleOwnerPermission(sys.argv[2] if (len(sys.argv) > 2) else None))
client.run(sys.argv[1])

if client.reboot_flag:
  os.execv(sys.executable, ['python3'] + sys.argv)
print("Have you finished already? Well, OK")
