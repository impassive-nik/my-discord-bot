import re

class REMatcher(object):
  def __init__(self, matchstring):
    self.matchstring = matchstring

  def match(self,regexp):
    self.rematch = re.match(regexp, self.matchstring)
    self.group_no = 1
    return bool(self.rematch)

  def group(self,i):
    return self.rematch.group(i)

  def get_str(self, group=None, default=None):
    if not group:
      group = self.group_no
      self.group_no += 1
      
    res = self.rematch.group(group)
    return res if res else default

  def get_int(self, group=None, default=None):
    res = self.get_str(group)
    return int(res) if res else default