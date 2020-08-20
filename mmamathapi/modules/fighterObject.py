class FighterObject:
  def __init__(self, name='', nickname='', wins=[]):
    self.name = name
    self.nickname = nickname
    self.wins = wins

  def __str__(self):
      return f'NAME: {self.name}, NICKNAME: {self.nickname}, WINS: {self.wins}'