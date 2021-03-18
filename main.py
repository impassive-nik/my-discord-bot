#!/usr/bin/env python3

import sys
import os
import discord
import random

from command import AdminCommand, RoleplayCommand, SingleOwnerPermission, GMPermission, GMCommand

class DiscordWrapper(discord.Client):
  def __init__(self):
    super(DiscordWrapper, self).__init__()
    self.reboot_flag = False

  async def on_ready(self):
    print("Ready! ")

  async def on_message(self, message):
    if message.author == self.user:
      return

    m = AdminCommand(r"/(?:die|(腹切り))", permission = self.admin).match(message)
    if m:
      if m.get_str():
        await message.channel.send("仰せのままに！")
      print("Woe me, I am dead")
      await self.close()
      return

    m = AdminCommand(r"/reboot", permission = self.admin).match(message)
    if m:
      print("Reboot requested")
      self.reboot_flag = True
      await self.close()
      return

    gm_perm = await GMPermission.create(message.channel)

    m = GMCommand(r"/gm_check", permission = gm_perm).match(message)
    if m:
      await message.channel.send("You are the master of this channel!")

    m = RoleplayCommand(r"[^/]*"
                        r"/(?:roll +|dice +)?"
                        r"([0-9]*)d([0-9]+) *"
                        r"([0-9]*)(\+|\-)? *").match(message)
    if m:
      num  = m.get_int(default=1)
      size = m.get_int()
      threshold = m.get_int()
      plus = m.get_str()

      if num in range(1, 11) and size in range(2, 101):
        sum = 0
        rolls = []
        for i in range(0, num):
          r = random.randrange(0, size) + 1
          sum += r
          rolls.append(r)
        if threshold is not None and plus is not None:
          if (plus == "+" and sum >= threshold) or (plus == "-" and sum <= threshold):
            await message.channel.send("**Успех!**   ||" + str(sum) + "||")
          else:
            await message.channel.send("**Провал!**   ||" + str(sum) + "||")
        else:
          await message.channel.send("**" + str(sum) + "** из " + str(num * size) + ". ||" + str(rolls) + "||")
      print("Roll: ", num, size, threshold)
      
    m = RoleplayCommand(r"[^/]*"
                        r"/(?:choose +|pick +)"
                        r"\{ *([^\};]+;[^\}]+) *\} *").match(message)
    if m:
      variants = list(map(str.strip, m.get_str().split(";")))
      if len(variants) > 1:
        chosen = variants[random.randrange(0, len(variants) + 1)]
        await message.channel.send("**" + chosen + "**  ||из " + str(len(variants)) + " вариантов||")


if __name__ == "__main__":
  if len(sys.argv) not in range(2, 4):
    print("Error: unexpected number of arguments", file=sys.stderr)
    #TODO: accept the token via environment variables?
    sys.exit(1)

  client = DiscordWrapper()
  client.admin = SingleOwnerPermission(sys.argv[2] if (len(sys.argv) > 2) else None)
  client.run(sys.argv[1])

  if client.reboot_flag:
    os.execv(sys.executable, ['python3'] + sys.argv)
  print("Have you finished already? Well, OK")

