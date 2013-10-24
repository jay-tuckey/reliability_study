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
      self.performCALDONE(message)
    elif message.typeofmessage == "LEAD":
      returnMessage = Message(self.id, "LEADACK", [])
      organiser.passMessage(message.senderid, returnMessage)
    elif message.typeofmessage == "LEADACK":
      if self.leaderID > message.senderid:
        self.leaderID = message.senderid
      elif self.secondInCommandID > message.senderid:
        self.secondInCommandID = message.senderid
        
    elif message.typeofmessage == "RES":
      self.currentCalculation.append([message.senderid, message.contents[0]])
      
  def performCALDONE(self, message):  
    if self.isLeader or self.isSecondInCommand:
        comparray = []
        for val in self.currentCalculation:
          added = False
          for index in range(len(comparray)):
            if comparray[index][1] == val[1]:
              comparray[index][0] += 1
              added = True
          if not added:
            comparray.append([1, val[1]])
        comparray.sort(reverse=True)
        returnMessage = Message(self.id, "CALDONE", [comparray[0][1]])
      
        # Now try to kill agents that are causing errors
        for agent in self.currentCalculation:
          if agent[1] != comparray[0][1]:
            organiser.reportAgent(agent[0])
            
        self.currentCalculation = []
        
        
        organiser.returnResult(returnMessage)
        
  def returnAnswer(self, calc):
    if calc[0] == "ADD":
      value = calc[1] + calc[2]
    elif calc[0] == "SUB":
      value = calc[1] - calc[2]
    if calc[0] == "MUL":
      value = calc[1] * calc[2]
    if calc[0] == "DIV":
      value = calc[1] / calc[2]
    return value
  
  def performCalculation(self, message):
    calc = message.contents
    value = self.returnAnswer(calc)
      
    # This section is all about finding who is the current leading agent
    #  and current second in command
    self.findCurrentLeader()
    
    # And now we return the result of the calculation
    returnMessage = Message(self.id, "RES", [value])
    if self.isLeader:
      organiser.passMessage(self.secondInCommandID, returnMessage)
      self.currentCalculation.append([self.id, value])
    elif self.isSecondInCommand:
      organiser.passMessage(self.leaderID, returnMessage)
      self.currentCalculation.append([self.id, value])
    else:
      organiser.passMessage(self.leaderID, returnMessage)
      organiser.passMessage(self.secondInCommandID, returnMessage)
    
  def findCurrentLeader(self):
    self.leaderID = self.id
    self.secondInCommandID = organiser.getLargestAgentID()
    message = Message(self.id, "LEAD")
    organiser.broadcastMessage(message)
    if self.leaderID == self.id:
      self.isLeader = True
    elif self.secondInCommandID > self.id:
      self.secondInCommandID = self.id
      self.isSecondInCommand = True
    
class AgentPlusone(Agent):
  """ This agent is exactly the same as the main agent, except that it
  adds 1 to the result of every computation it performs. This is common in programming,
  and is known as an off-by-one error. """
  def returnAnswer(self, calc):
    if calc[0] == "ADD":
      value = calc[1] + calc[2] + 1
    elif calc[0] == "SUB":
      value = calc[1] - calc[2] + 1
    if calc[0] == "MUL":
      value = calc[1] * calc[2] + 1
    if calc[0] == "DIV":
      value = calc[1] / calc[2] + 1
    return value
    

class AgentRandomError(Agent):
  def returnAnswer(self, calc):
    temp = random.randint(1,10)
    if temp > 8:
      addOne = random.randint(-1,1)
    else:
      addOne = 0
    
    if calc[0] == "ADD":
      value = calc[1] + calc[2] + addOne
    elif calc[0] == "SUB":
      value = calc[1] - calc[2] + addOne
    if calc[0] == "MUL":
      value = calc[1] * calc[2] + addOne
    if calc[0] == "DIV":
      value = calc[1] / calc[2] + addOne
    return value

class AgentRoundingError(Agent):
  def returnAnswer(self, calc):
    temp = random.randint(1,10)
    if temp > 9:
      addOne = random.randint(-1,1)
    else:
      addOne = 0
    
    if calc[0] == "ADD":
      value = calc[1] + calc[2] + addOne
    elif calc[0] == "SUB":
      value = calc[1] - calc[2] + addOne
    if calc[0] == "MUL":
      value = calc[1] * calc[2] + addOne
    if calc[0] == "DIV":
      value = calc[1] / calc[2] + addOne
    value = round(value, 3)
    return value
  
class AgentRandomDeath(Agent):
  def __init__(self, id):
    self.id = id
    self.leaderID = id
    self.isLeader = False
    self.secondInCommandID = id
    self.isSecondInCommand = False
    self.currentCalculation = []
    self.dieAt = random.randint(10,100)
    self.currentCycles = 0
  
  def performCALDONE(self, message):  
    if self.isLeader or self.isSecondInCommand:
        comparray = []
        for val in self.currentCalculation:
          added = False
          for index in range(len(comparray)):
            if comparray[index][1] == val[1]:
              comparray[index][0] += 1
              added = True
          if not added:
            comparray.append([1, val[1]])
        comparray.sort(reverse=True)
        returnMessage = Message(self.id, "CALDONE", [comparray[0][1]])
      
        # Now try to kill agents that are causing errors
        for agent in self.currentCalculation:
          if agent[1] != comparray[0][1]:
            organiser.reportAgent(agent[0])
            
        self.currentCalculation = []
        
        
        organiser.returnResult(returnMessage)
    if self.currentCycles == self.dieAt:
      organiser.killAgent(self.id)
    else:
      self.currentCycles += 1

class Organiser:
  def __init__(self, numAgents=5, argHeuristic=False):
    self.currentid = 1 # This is the id of a new agent to be created
    self.agentlist = [] # This is the list of agents that perform the calculations
    self.calcBuffer = [] # This is the list used to group the calculations before returning
    self.reportedAgents = [] # This list is used to keep track of the agents that have
                             # returned incorrect results.
                             
    if numAgents < 2:
      self.numAgents = 2
    else:
      self.numAgents = numAgents
    while len(self.agentlist) < self.numAgents:
      self.addAgent()
    if argHeuristic == (False or "NONE"):
      self.argHeuristic = False
    elif argHeuristic == "INSTAKILL":
      self.argHeuristic = "INSTAKILL"
    elif argHeuristic == "FIVETOKILL":
      self.argHeuristic = "FIVETOKILL"
    elif argHeuristic == "FIVETOKILL-LDR-2IC":
      self.argHeuristic = "FIVETOKILL-LDR-2IC"
   
  def addAgent(self):
    # This function adds a new agent to the set of agents that are
    # running
    print("Adding new agent to list")
    randomnum = random.randint(1, 100)
    if randomnum <= 70:
      agent = Agent(self.currentid)
    elif randomnum <= 80:
      agent = AgentRandomError(self.currentid)
    elif randomnum <= 90:
      agent = AgentRoundingError(self.currentid)
    elif randomnum <= 100:
      agent = AgentPlusone(self.currentid)
    self.currentid += 1
    self.agentlist.append(agent)

  
  def killAgent(self, agentid):
    for agent in self.agentlist:
      if agent.id == agentid:
        self.agentlist.remove(agent)
  
  def killRandomAgent(self):
    randomnum = random.randint(0, len(self.agentlist) - 1)
    del self.agentlist[randomnum]
  
  def killMisbehavingAgents(self):
    if self.argHeuristic == False:
      return
    elif self.argHeuristic == "INSTAKILL":
      print("Testing.... INSTAKILL")
      for a in self.reportedAgents:
        self.killAgent(a[0])
        self.reportedAgents.remove(a)
        
    while len(self.agentlist) < self.numAgents:
      self.addAgent()
  
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

  def reportAgent(self, agentID):
    reported = False
    for a in self.reportedAgents:
      if a[0] == agentID:
        a[1] += 1
        reported = True
    if reported == False:
      self.reportedAgents.append([agentID, 1])

  def createCalcProblem(self, typeofcalc, num1, num2):
    self.killMisbehavingAgents() # Kill misbehaving agents. Also confirm there are enough agents to run the calculation
    
    message = Message(0, "CAL", [typeofcalc, num1, num2])
    self.broadcastMessage(message)
    message = Message(0, "CALDONE")
    self.broadcastMessage(message)
    
    # Check the results are the same, and if not, report the agents
    reportLead2ic = False
    if len(self.calcBuffer) <= 2:
      if self.calcBuffer[0] == self.calcBuffer[1]:
        val = self.calcBuffer[0]
        self.calcBuffer = []
        return val
      else:
        reportLead2ic = True
    else:
      print("Result invalid: Not enough agents returned computation")
      reportLead2ic = True
    if reportLead2ic:
      reportId = self.agentlist[0].id
      self.reportAgent(reportId)
      reportId = self.agentlist[1].id
      self.reportAgent(reportId)
      
    self.calcBuffer = []
    #self.createCalcProblem(typeofcalc, num1, num2)
    
  
##### End Classes
organiser = False
def run():
  global organiser
  organiser = Organiser(5, "INSTAKILL")

  correctCounter = 0
  incorrectCounter = 0
  noReturnCounter = 0

  for i in range(1000):
    val = organiser.createCalcProblem("ADD", i, 3)
    if (3 + i) == val:
      correctCounter += 1
    else:
      if type(val) == int:
        incorrectCounter += 1
      else:
        noReturnCounter += 1
    organiser.killRandomAgent()
  print("Correct: " + str(correctCounter))
  print("Incorrect: " + str(incorrectCounter))
  print("No Return: " + str(noReturnCounter))


code.interact(local=globals())