from regex import REMatcher

class Permission:
  def permitted(self, user):
    return True

class SingleOwnerPermission(Permission):
  def __init__(self, user_id=None):
    super(SingleOwnerPermission, self).__init__()
    self.user_id = int(user_id) if user_id else -1

  def permitted(self, user):
    return user.id == self.user_id

class Command:
  def __init__(self, regex):
	  self.regex = regex
	
  def match(self, message):  
    matcher = REMatcher(message.content)
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
    message.channel.send("Permission denied")
    return False
