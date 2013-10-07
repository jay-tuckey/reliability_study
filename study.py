import code, random

##### Classes
    
class Message:
  """ This class defines the structure for a message. It contains two properties, the sender's id, and the the message contents """
  def __init__(self, senderid, typeofmessage, contents):
    self.senderid = senderid
    self.typeofmessage = typeofmessage
    self.contents = contents
  
class Agent:
  def __init__(self, id):
    self.id = id
    self.currentmid = 1
    self.leaderID = id
    self.isLeader = False

    
  def receiveMessage(self, message):
    if message.senderid == self.id:
      return
    elif message.typeofmessage == "CAL":
      self.performCalculation(message)
    elif message.typeofmessage == "LEAD":
      returnMessage = Message(self.id, "LEADACK", [])
      organiser.passMessage(message.senderid, returnMessage)
    elif message.typeofmessage == "LEADACK":
      print("Leadack")
    elif message.typeofmessage == "ACK":
      return
    
    
  def performCalculation(self, message):
    calc = message.contents
    if calc[0] == "ADD":
      value = calc[1] + calc[2]
    elif calc[0] == "SUB":
      value = calc[1] - calc[2]
    if calc[0] == "MUL":
      value = calc[1] * calc[2]
    if calc[0] == "DIV":
      value = calc[1] / calc[2]
    self.findCurrentLeader();
    returnMessage = Message(self.id, "RES", [value, message.contents[3]])
    organiser.returnResult(returnMessage)
    
  def findCurrentLeader(self):
    message = Message(self.id, "LEAD", False)
    organiser.broadcastMessage(message)

  
class Organiser:
  def __init__(self):
    self.currentid = 1 # This is the id of a new agent to be created
    self.calccounter = 1
    self.agentlist = []
    self.messages = []
  def runstep(self):
    print("Running a step for all agents")
    for agent in self.agentlist:
      agent.runStep()
  
  def addAgent(self):
    # What this function does is it adds a new agent to the set of agents that are
    # running
    print("Adding new agent to list")
    randomnum = random.randint(1, 50)
    if randomnum <= 50:
      agent = Agent(self.currentid)
    self.currentid += 1
    self.agentlist.append(agent)
  
  """ A function to send a message to all agents on the network """
  def broadcastMessage(self, message):
    for agent in self.agentlist:
      agent.receiveMessage(message)
  
  def passMessage(self, toid, message):
    for agent in self.agentlist:
      if agent.id == toid:
        agent.receiveMessage(message)
  
  def returnResult(self, message):
    if message.typeofmessage == "RES":
      print(message.contents[0])
    else:
      print("Something tried to return a result")

  def createCalcProblem(self, typeofcalc, num1, num2):
    message = Message(0, "CAL", [typeofcalc, num1, num2, self.calccounter])
    self.calccounter += 1
    self.broadcastMessage(message)
  
##### End Classes
organiser = Organiser()


# Testing stuff
for i in range(4):
  organiser.addAgent()



code.interact(local=globals())
