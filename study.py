import code, random

##### Classes
    
class Message:
  """ This class defines the structure for a message. It contains two properties, the sender's id, and the the message contents """
  def __init__(self, senderid, typeofmessage, contents=False):
    self.senderid = senderid
    self.typeofmessage = typeofmessage
    self.contents = contents

class Agent:
  def __init__(self, id):
    self.id = id
    self.currentmid = 1
    self.leaderID = id
    self.isLeader = False
    self.secondInCommandID = id
    self.isSecondInCommand = False
    self.currentCalculation = []

    
  def receiveMessage(self, message):
    if message.senderid == self.id:
      return
    elif message.typeofmessage == "CAL":
      self.performCalculation(message)
    elif message.typeofmessage == "CALDONE":
      if self.isLeader or self.isSecondInCommand:
        comparray = []
        for val in self.currentCalculation:
          added = False
          for index in range(len(comparray)):
            if comparray[index][1] == val:
              comparray[index][0] += 1
              added = True
          if not added:
            comparray.append([1, val])
            print("Successfully added value")
        print("Original: " + str(comparray))
        comparray.sort()
        print("Sorted: " + str(comparray))
        returnMessage = Message(self.id, "CALDONE", [comparray[0][1]])
        organiser.returnResult(returnMessage)
      
        self.currentCalculation = []
    elif message.typeofmessage == "LEAD":
      returnMessage = Message(self.id, "LEADACK", [])
      organiser.passMessage(message.senderid, returnMessage)
    elif message.typeofmessage == "LEADACK":
      if self.leaderID > message.senderid:
        print("Setting leader")
        self.leaderID = message.senderid
      elif self.secondInCommandID > message.senderid:
        print("Setting 2ic")
        self.secondInCommandID = message.senderid
        
    elif message.typeofmessage == "RES":
      print("I received a result message from " + str(message.senderid) + ". It's value was: " + str(message.contents[0]) + ". My id is: " + str(self.id))
      self.currentCalculation.append(message.contents[0])
      
    
    
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
      
    # This section is all about finding who is the current leading agent
    #  and current second in command
    self.findCurrentLeader()
    
    # And now we return the result of the calculation
    returnMessage = Message(self.id, "RES", [value, message.contents[3]])
    if self.isLeader:
      organiser.passMessage(self.secondInCommandID, returnMessage)
      self.currentCalculation.append(value)
    elif self.isSecondInCommand:
      organiser.passMessage(self.leaderID, returnMessage)
      self.currentCalculation.append(value)
    else:
      organiser.passMessage(self.leaderID, returnMessage)
      organiser.passMessage(self.secondInCommandID, returnMessage)
    
  def findCurrentLeader(self):
    self.leaderID = self.id
    self.secondInCommandID = organiser.getLargestAgentID()
    message = Message(self.id, "LEAD")
    organiser.broadcastMessage(message)
    if self.leaderID == self.id:
      print("I am leader")
      self.isLeader = True
    elif self.secondInCommandID > self.id:
      self.secondInCommandID = self.id
      print("I am 2ic")
      self.isSecondInCommand = True
    
      
      

  
class Organiser:
  def __init__(self):
    self.currentid = 1 # This is the id of a new agent to be created
    self.calccounter = 1 # This is the id of the current calculation being run
    self.agentlist = [] # This is the list of agents that perform the calculations
    self.calcBuffer = [] # This is the list used to group the calculations before returning
  def runstep(self):
    print("Running a step for all agents")
    for agent in self.agentlist:
      agent.runStep()
  
  def addAgent(self):
    # This function adds a new agent to the set of agents that are
    # running
    print("Adding new agent to list")
    randomnum = random.randint(1, 50)
    if randomnum <= 50:
      agent = Agent(self.currentid)
    self.currentid += 1
    self.agentlist.append(agent)
  
  def killAgent(self, agentid):
    for agent in self.agentlist:
      if agent.id == agentid:
        self.agentlist.remove(agent)
  
  """ This function is to get an id greater than any current agents """
  def getLargestAgentID(self):
    return self.currentid    
  
  """ A function to send a message to all agents on the network """
  def broadcastMessage(self, message):
    for agent in self.agentlist:
      agent.receiveMessage(message)
  
  def passMessage(self, toid, message):
    for agent in self.agentlist:
      if agent.id == toid:
        agent.receiveMessage(message)
  
  def returnResult(self, message):
    if message.typeofmessage == "CALDONE":
      self.calcBuffer.append(message.contents[0])
    else:
      print("Something tried to return a result")

  def createCalcProblem(self, typeofcalc, num1, num2):
    message = Message(0, "CAL", [typeofcalc, num1, num2, self.calccounter])
    self.calccounter += 1
    self.broadcastMessage(message)
    message = Message(0, "CALDONE")
    self.broadcastMessage(message)
    if len(self.calcBuffer) == 2:
      if self.calcBuffer[0] == self.calcBuffer[1]:
        val = self.calcBuffer[0]
        self.calcBuffer = []
        return val
    else:
      print("Result invalid: Not enough agents returned computation")
    self.calcBuffer = []
  
##### End Classes
organiser = Organiser()


# Testing stuff
for i in range(2):
  organiser.addAgent()

correctCounter = 0
incorrectCounter = 0
for i in range(1000):
  if organiser.createCalcProblem("ADD", i, 3) == (3 + i):
    correctCounter += 1
  else:
    incorrectCounter += 1


code.interact(local=globals())
