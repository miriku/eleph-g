class Game:
  id = -1
  name = ""
  owner = -1
  maxPlayers = -1
  currentPlayers = []
  timeClose = -1
  post = 0

  def __init__(self, id):
    self.id = id

  def debug():
    print("game")
