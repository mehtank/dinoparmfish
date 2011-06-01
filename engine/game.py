import random
import card
import copy

MAXTURNS = 1000

class game:
  score = [0, 0]

  def debug(self, s):
    print "Game message: ", 
    print s

  def __init__(self, team0, team1):
    # XXX TODO: check to make sure teams are valid
    self.team0 = team0
    self.team1 = team1
    self.teamSize = min(len(self.team0), len(self.team1))
    self.numPlayers = 2 * self.teamSize

  def go(self):
    self.setup()
    self.play()
    return self.score

  def setup(self):
    deck = [ card.card(value=value,suit=suit) 
                for value in range(card.NUMVALUES) 
                for suit in range(card.NUMSUITS) ]

    # shuffle the deck
    random.shuffle(deck)

    # seat the players randomly
    random.shuffle(self.team0)
    random.shuffle(self.team1)

    self.players = []
    self.hands = []

    for i in range(self.teamSize):
      self.players += [ self.team0[i], self.team1[i] ]
      # deal out the cards
      self.hands += [ deck[2*i :: self.numPlayers], deck[2*i+1 :: self.numPlayers] ]

    # tell the players their position and starting hand
    for i in range(self.numPlayers):
      self.players[i].setup(i, self.numPlayers, copy.deepcopy(self.hands[i])) # PLAYER CALL

  def play(self):
    # determine which team starts
    currentPlayer = 0
    if random.random > 0.5:
      currentPlayer = 1

    turns = 0

    while not self.gameOver():
      # if the current player has no hand, he passes to anyone on his team
      while len(self.hands[currentPlayer]) == 0:
        newPlayer = self.players[currentPlayer].passTo() # PLAYER CALL
        if ((currentPlayer - newPlayer) % 2) == 0 and len(self.hands[newPlayer]) > 0:
          currentPlayer = newPlayer
        else:
          currentPlayer = (currentPlayer + 2) % self.teamSize

      currentPlayer = self.turn(currentPlayer)
      self.getDeclarations(currentPlayer)

      # prevent endless loops
      turns += 1
      if turns > MAXTURNS:
        break

  def turn(self, currentPlayer):
    # get the current player to ask for a card from a target
    (target, ask) = self.players[currentPlayer].getAsk() # PLAYER CALL

    # make sure the ask is legal
    if self.isValidAsk(currentPlayer, target, ask):
      # determine whether the target has the card or not
      askSuccessful = self.resolveAsk(currentPlayer, target, ask)
      # tell everyone what happened
      for p in self.players:
        p.tellAsk(currentPlayer, target, copy.copy(ask), askSuccessful) # PLAYER CALL

      # return the next player
      if not askSuccessful:
        # failed ask, play passes to target
        return target

      # successful ask, player keeps going
      return currentPlayer

    else:
      # an illegal ask forfeits the turn to the next player
      return (currentPlayer + 1) % self.numPlayers

  def isValidAsk(self, currentPlayer, target, ask):
    # invalid target: wrong team
    if (currentPlayer - target) % 2 == 0: return False
    # invalid target: no cards
    if len(self.hands[target]) == 0: return False
    # invalid suit
    if not self.hasSuit(currentPlayer, ask.suit): return False
    # invalid card
    if self.hasCard(currentPlayer, ask): return False

    # valid
    return True

  def resolveAsk(self, currentPlayer, target, ask):
    try:
      index = self.hands[target].index(ask)
      self.hands[currentPlayer].append(self.hands[target].pop(index))
      return True
    except ValueError:
      return False

  def hasSuit(self, player, suit):
    for c in self.hands[player]:
      if c.suit == suit:
        return True
    return False

  def hasCard(self, player, ask):
    for c in self.hands[player]:
      if c == ask:
        return True
    return False
  
  def getDeclarations(self, currentPlayer):
    lastDeclaration = 0
    # ends at two times around the circle without anyone declaring anything 
    while (lastDeclaration < self.numPlayers*2):
      # get the current player to declare a suit
      (suit, attrib) = self.players[currentPlayer].getDeclaration() # PLAYER CALL
      # determine whether the target has the card or not
      declarationSuccessful = self.resolveDeclaration(currentPlayer, suit, attrib)

      # tell everyone what happened
      for p in self.players:
        p.tellDeclaration(currentPlayer, suit, copy.copy(attrib), declarationSuccessful) # PLAYER CALL

      if declarationSuccessful:
        # correct declaration: reset counter, keep on same player
        lastDeclaration = 0
      else:
        # incorrect or no declaration: increment counter, go to next player
        lastDeclaration += 1
        currentPlayer = (currentPlayer + 1) % len(self.players)

  def resolveDeclaration(self, currentPlayer, suit, attrib):
    if suit is None:
      # no declaration
      return None

    team = currentPlayer % 2
    opponents = 1 - team
    self.debug ("Player " + repr(currentPlayer) + " on team " + repr(team) + " declared suit " + repr(suit))

    trueAttrib = self.killSuit(suit)

    if len(attrib) != card.NUMVALUES:
      # invalid attributation
      self.debug ("attrib not right length")
      self.score[opponents] += 1
      return False

    for player in trueAttrib:
      if (currentPlayer - player) % 2 == 1:
        # card held by opposing team
        self.debug ("Player " + repr(player) + " has a card")
        self.score[opponents] += 1
        return False

    if attrib == trueAttrib:
      # correct declaration
      self.debug ("Success!")
      self.score[team] += 1
      return True

    # incorrect attributions
    self.debug ("Failure:")
    self.debug (repr(attrib))
    self.debug (repr(trueAttrib))
    self.score[opponents] += 1
    return False

  def killSuit(self, suit):
    trueAttrib = [-1] * card.NUMVALUES
    for i in range(self.numPlayers):
      hand = self.hands[i]
      topop = []
      for c in hand:
        if c.suit == suit:
          trueAttrib[c.value] = i
          topop.append(c)
      for c in topop:
        hand.pop(hand.index(c))

    return trueAttrib

  def gameOver(self):
    team0count = sum(map(len, self.hands[0::2]))
    team1count = sum(map(len, self.hands[1::2]))

    # game over when one team has no more cards
    return (team0count * team1count) == 0
