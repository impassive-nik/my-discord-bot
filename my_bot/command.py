from .regex import RegexMatcher
from .permission import Permission, SingleOwnerPermission, GMPermission

class Command:
  def __init__(self, regex):
	  self.regex = regex
	
  def match(self, message):  
    matcher = RegexMatcher(message.content)
    if not matcher.match(self.regex):
      return None

    if not self.proper_context(message):
      return None
    
    return matcher
    
  def proper_context(self, message):
    return True


class RoleplayCommand(Command):    
  def proper_context(self, message):
    return message.channel.name.startswith("roleplay")

class AdminCommand(Command):
  def __init__(self, regex, permission=None):
    super(AdminCommand, self).__init__(regex)
    self.permission = permission

  def proper_context(self, message):
    if self.permission.permitted(message.author):
      return True

    print("Unathorized admin command request by ", message.author.id)
    return False

class GMCommand(RoleplayCommand):
  def __init__(self, regex, permission=None):
    super(GMCommand, self).__init__(regex)
    self.permission = permission

  def proper_context(self, message):
    if not super(GMCommand, self).proper_context(message):
      return False
    return self.permission.permitted(message.author)
