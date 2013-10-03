import code, random

##### Classes

class TestClass:
  """ This is just a test class. It has one property:
    test
  and one function
    testfunc()"""
  test = "test property"
  def testfunc(self):
    print("running test function")
    
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

  def runStep(self):
    print("Running from inside agent. Id is: " + str(self.id))
    
  def receiveMessage(self, message):
    if message.senderid == self.id:
      return
    elif message.typeofmessage == "CAL":
      value = self.performCalculation(message.contents);
      returnMessage = Message(self.id, "RES", [value, message.contents[3]])
      organiser.returnResult(returnMessage)
    elif message.typeofmessage == "ACK":
      return
    
    
  def performCalculation(self, calc):
    if calc[0] == "ADD":
      return calc[1] + calc[2]
    elif calc[0] == "SUB":
      return calc[1] - calc[2]
    if calc[0] == "MUL":
      return calc[1] * calc[2]
    if calc[0] == "DIV":
      return calc[1] / calc[2]

  
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
    
  def returnResult(self, message):
    print("Something tried to return a result")

  def createCalcProblem(self, typeofcalc, num1, num2):
    message = Message(0, "CAL", [typeofcalc, num1, num2, self.calccounter])
    self.calccounter += 1
    self.broadcastMessage(message)

##### End Classes
organiser = Organiser()


# Testing stuff
organiser.addAgent()
organiser.addAgent()

code.interact(local=globals())
