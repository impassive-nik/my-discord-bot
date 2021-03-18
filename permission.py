class Permission:
  def permitted(self, user):
    return True

class SingleOwnerPermission(Permission):
  def __init__(self, user_id=None):
    super(SingleOwnerPermission, self).__init__()
    self.user_id = int(user_id) if user_id else -1

  def permitted(self, user):
    return user.id == self.user_id

class GMPermission(SingleOwnerPermission):  
  gm_ids = dict()

  @staticmethod
  async def create(channel):
    if channel.id in GMPermission.gm_ids:
      gm_id = GMPermission.gm_ids[channel.id]
    else:
      messages = await channel.history().flatten()     
      for msg in messages:
        first = msg
      gm_id = first.author.id
      GMPermission.gm_ids[channel.id] = gm_id

    return GMPermission(user_id=gm_id)