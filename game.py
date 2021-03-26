class Game:
  id = -1
  text = ""
  message = -1 
  owner = -1
  maxPlayers = -1
  currentPlayers = []
  timeClose = -1
  post = 0

  def __init__(self, id, message, text):
    self.id = id
    self.message = message
    self.text = text

  def debug():
    print("game")
