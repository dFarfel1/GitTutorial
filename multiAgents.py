# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        #print(legalMoves)
        #print(legalMoves)
        return legalMoves[chosenIndex]


    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        minDist = float('inf')
        #print(newFood.asList())
        #for 

        #print(type(newFood))
        count = 0
        for food in newFood:
            count = count + 1
            manD = abs((newPos[0] - food[0]) + (newPos[1] - food[1]))
            if manD < minDist:
                minDist = manD
                
        #print(count)
        #print(type(action))

        ghostDist = 5
        for ghost in newGhostStates:
            ghostPos = ghost.getPosition()
            manD = abs((newPos[0] - ghostPos[0]) + (newPos[1] - ghostPos[1]))
            if manD < ghostDist:
                ghostDist = manD
    
        #if ghostDist
        #print(ghostDist)
        ghostDist = 0
        #print(action)
        if action == 'Stop':
            #print('here')
            return float('-inf')
        return 1
        #return successorGameState.getScore() + 1/(1+minDist) #+ ghostDist*2

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    #minDep = 0

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def maxVal(state,depth):
            legalActions = state.getLegalActions(0)
            #v = self.evaluationFunction(state)
            v = (float('-inf'))
            #print v
            if state.isWin() or state.isLose() or depth == 0 or len(legalActions) == 0:
                return self.evaluationFunction(state)
            for suc in [state.generateSuccessor(0,action) for action in legalActions]:
                v = max(v, value(suc,1 % gameState.getNumAgents(), depth))

            #print(str(depth) + ' ' + str(v))
            return v
        
        def minVal(state,ghostId,depth):
            legalActions = state.getLegalActions(ghostId)
            #v = self.evaluationFunction(state)

            if state.isWin() or state.isLose() or depth == 0 or len(legalActions) == 0:
                return self.evaluationFunction(state)
            v = float('inf')
            for suc in [state.generateSuccessor(ghostId,action) for action in legalActions]:
                v = min(v, value(suc,(ghostId+1)%gameState.getNumAgents(),depth))
                
            return v

        def value(state, agentId, depth):
            legalActions = state.getLegalActions()
            
            if state.isWin() or state.isLose() or depth == 0 or len(legalActions) == 0:
                return self.evaluationFunction(state)
            
            if agentId == 0:
                #print("max {}".format(depth))
                return maxVal(state, depth-1)

            if agentId > 0:
                #print("min {}".format(depth))
                return minVal(state, agentId, depth)

        
            
        legalActions = gameState.getLegalActions(0)
        v = (float("-inf"))
        action = None
        for act in legalActions:
            temp = value(gameState.generateSuccessor(0,act),1 % gameState.getNumAgents(),self.depth)
            #print(temp) 
            if  temp > v:
                action = act
                v = temp
                
        #print("Resul: {}".format(v))
        return action

        #minDep = 0
        util.raiseNotDefined()

    
    
    

    
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxVal(state,depth,a,b):
            legalActions = state.getLegalActions(0)
            #v = self.evaluationFunction(state)
            v = (float('-inf'))
            #print v
            if state.isWin() or state.isLose() or depth == 0 or len(legalActions) == 0:
                v = self.evaluationFunction(state)

                #print(v)
                return v
            for action in legalActions:
                suc = state.generateSuccessor(0,action)
                v = max(v, value(suc,1 % gameState.getNumAgents(), depth,a,b))
                if v > b:
                    return v
                a = max(a,v)
                #print("Alpha updated to {}".format(a))

            #print(str(depth) + ' ' + str(v))
            return v
        
        def minVal(state,ghostId,depth,a,b):
            legalActions = state.getLegalActions(ghostId)
            #v = self.evaluationFunction(state)

            if state.isWin() or state.isLose() or depth == 0 or len(legalActions) == 0:
                v = self.evaluationFunction(state)
                #print(v)
                return v
            v = float('inf')
            for action in legalActions:
                suc = state.generateSuccessor(ghostId,action)
                v = min(v, value(suc,(ghostId+1)%gameState.getNumAgents(),depth,a,b))
                #print("Alpha: {} V: {} ".format(a,v))
                if v < a:
                    return v
            
                b = min(b,v)
                #print("Beta updated to {}".format(b))
                
            return v

        def value(state, agentId, depth,a,b):
            legalActions = state.getLegalActions()
            
            if state.isWin() or state.isLose() or depth == 0 or len(legalActions) == 0:
                v = self.evaluationFunction(state)
                #print(v)
                return v
            
            if agentId == 0:
                #print("Alpha: {} Beta: {}".format(a,b))
                return maxVal(state, depth-1,a,b)

            if agentId > 0:
                #print("Alpha: {} Beta: {}".format(a,b))
                return minVal(state, agentId, depth, a, b)

        
            
        legalActions = gameState.getLegalActions(0)
        v = (float("-inf"))
        action = None
        a = float('-inf')
        b = float('inf')
        for act in legalActions:
            temp = value(gameState.generateSuccessor(0,act),1 % gameState.getNumAgents(),self.depth,a,b)
            #print(temp) 
            if  temp > v:
                action = act
                v = temp
            if v > b:
                return action
            a = max(a,v)
        #print("Resul: {}".format(v))
        return action
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def maxVal(state,depth):
            legalActions = state.getLegalActions(0)
            #v = self.evaluationFunction(state)
            v = (float('-inf'))
            #print v
            if state.isWin() or state.isLose() or depth == 0 or len(legalActions) == 0:
                return self.evaluationFunction(state)
            for suc in [state.generateSuccessor(0,action) for action in legalActions]:
                v = max(v, value(suc,1 % gameState.getNumAgents(), depth))

            #print(str(depth) + ' ' + str(v))
            return v
        
        def expVal(state,ghostId,depth):
            legalActions = state.getLegalActions(ghostId)
            #v = self.evaluationFunction(state)

            if state.isWin() or state.isLose() or depth == 0 or len(legalActions) == 0:
                return self.evaluationFunction(state)
            v = 0
            for suc in [state.generateSuccessor(ghostId,action) for action in legalActions]:
                v += value(suc,(ghostId+1)%gameState.getNumAgents(),depth)
                
            return v/len(legalActions)

        def value(state, agentId, depth):
            legalActions = state.getLegalActions()
            
            if state.isWin() or state.isLose() or depth == 0 or len(legalActions) == 0:
                return self.evaluationFunction(state)
            
            if agentId == 0:
                #print("max {}".format(depth))
                return maxVal(state, depth-1)

            if agentId > 0:
                #print("min {}".format(depth))
                return expVal(state, agentId, depth)

        
            
        legalActions = gameState.getLegalActions(0)
        v = (float("-inf"))
        action = None
        for act in legalActions:
            temp = value(gameState.generateSuccessor(0,act),1 % gameState.getNumAgents(),self.depth)
            #print(temp) 
            if  temp > v:
                action = act
                v = temp
                
        #print("Resul: {}".format(v))
        return action
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: 
    close Food: The score associated with the distance to the nearest food pellet, 
    we want to decrease this distance (thus moving us closer to the nearest pellet) 
    and should incentivize decreasing the distance We can do this by taking the 
    recipricol of the distance (+1 in case its 0)

    food left: The score associated with the amount of food left. Again we want to decrease this so we
    take the recipricol. Since game states with less food items are closer to winning (as opposed to games closer)
    to the nearest pellet) we want to make this score worth more so we multiply it by 100.

    We then take these two values and the score of that state and add them together. 
    """
    "*** YOUR CODE HERE ***"

    
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood().asList()
    ghostPos = currentGameState.getGhostPositions()
    #newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    minDist = float('inf')
    
    #Distance to nearest pellet
    #count = 0
    for food in newFood:
        #count = count + 1
        manD = manhattanDistance(food,newPos)
        if manD < minDist:
            minDist = manD
    
    closeFood = 1.0/(1+minDist) 

    foodLeft = 100.0/(len(newFood)+1)

                
    #print(count)
    #print(type(action))
    
    return  currentGameState.getScore()  + closeFood + foodLeft
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
