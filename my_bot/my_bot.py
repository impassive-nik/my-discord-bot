import discord
import random
import os
import threading
import asyncio

from .command import AdminCommand, RoleplayCommand, Permission, GMPermission, GMCommand

class DiscordWrapper(discord.Client):
  def __init__(self, admin : Permission = None, pipe : str = None):
    super(DiscordWrapper, self).__init__()
    self.admin = admin
    self.admin_user = None
    self.reboot_flag = False

    self.pipe_file = pipe
    self.pipe_thread = None

    if self.pipe_file is not None:
      self.pipe_thread = threading.Thread(target=self.pipe_responder)
      self.pipe_thread.daemon = True
      self.pipe_thread.start()
  
  def pipe_responder(self):
      if os.path.exists(self.pipe_file):
        os.unlink(self.pipe_file)
      os.mkfifo(self.pipe_file)

      while True:
        with open(self.pipe_file) as fifo:
          while True:
            data = fifo.read()
            if len(data) == 0:
              break
            #print('Read: "{0}"'.format(data))
            self.loop.create_task(self.inform_admin(str(data)))
  
  async def inform_admin(self, message : str):
    if self.admin_user is None:
      if self.admin is None:
        return
      self.admin_user = await self.fetch_user(self.admin.user_id)
    
    if self.admin_user.dm_channel is None:
      await self.admin_user.create_dm()

    await self.admin_user.dm_channel.send(message)

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
        chosen = variants[random.randrange(0, len(variants))]
        await message.channel.send("**" + chosen + "**  ||из " + str(len(variants)) + " вариантов||")