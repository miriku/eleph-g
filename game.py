class Game:
  id = -1
  text = ""
  message = -1 
  owner = -1
  ownerid = -1
  playerswanted = -1
  gamelength = -1
  currentPlayers = []
  timetoclose = -1
  post = 0

  def __init__(self, i):
    self.id = id
    i = i.split("\t")
    self.id=i[0]
    self.text=i[1]
    self.playerswanted=int(i[2])
    self.gamelength=i[3]
    self.ownerid=i[4]

  def setMessage(self, message):
    self.message = message

  def display(self):
    output = "(" + self.id + ") "
    output = output + self.text + " - "
    output = output + "Needs " + str(self.playerswanted-len(self.currentPlayers)) + " more. "
    output = output + "[[Timer code: " + str(self.timetoclose) + "]] "
    return output

  def debug(self):
    print("game")
