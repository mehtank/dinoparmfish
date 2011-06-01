import random

VALUE = 0
SUIT = 1

NUMVALUES = 6
NUMSUITS = 8

MAXTURNS = 10000

def newCard(suit, value):
  card = [0, 0]
  card[SUIT] = suit
  card[VALUE] = value
  return card

class game:
  deck = [ newCard(value=value,suit=suit) for value in range(NUMVALUES) for suit in range(NUMSUITS) ]
  score = [0, 0]

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
    # shuffle the deck
    random.shuffle(self.deck)

    # seat the players randomly
    random.shuffle(self.team0)
    random.shuffle(self.team1)

    self.players = []
    self.hands = []

    for i in range(self.teamSize)
      self.players += [ self.team0[i], self.team1[i] ]
      # deal out the cards
      self.hands += [ deck[2*i :: self.numPlayers], deck[2*i+1 :: self.numPlayers] ]

    # tell the players their position and starting hand
    for i in range(self.numPlayers):
      self.players[i].setup(i, self.hands[i]) # PLAYER CALL

  def play(self):
    # determine which team starts
    currentPlayer = 0
    if random.random > 0.5:
      currentPlayer = 1

    turns = 0

    while not self.gameOver():
      # if the current player has no hand, he passes to anyone on his team
      while len(self.hands[currentPlayer]) == 0:
        newPlayer = self.players[currentPlayers].passTo() # PLAYER CALL
        if ((currentPlayer - newPlayer) % 2) == 0 and 
                len(self.hands[newPlayer]) > 0:
          currentPlayer = newPlayer
        else:
          currentPlayer = (currentPlayer + 2) % self.teamSize

      currentPlayer = self.turn(currentPlayer)
      getDeclarations(currentPlayer)

      # prevent endless loops
      turns += 1
      if turns > MAXTURNS:
        break

  def turn(self, currentPlayer):
    # get the current player to ask for a card from a target
    (target, card) = self.players[currentPlayer].getAsk() # PLAYER CALL

    # make sure the ask is legal
    if self.isValidAsk(currentPlayer, target, card):
      # determine whether the target has the card or not
      askSuccessful = self.resolveAsk(currentPlayer, target, card)
      # tell everyone what happened
      for (p : self.players):
        p.tellAsk(currentPlayer, target, card, askSuccessful) # PLAYER CALL

      # return the next player
      if !askSuccessful:
        # failed ask, play passes to target
        return target

      # successful ask, player keeps going
      return currentPlayer

    else:
      # an illegal ask forfeits the turn to the next player
      return (currentPlayer + 1) % self.numPlayers

  def isValidAsk(self, currentPlayer, target, card):
    # invalid target: wrong team
    if (currentPlayer - target) % 2 == 0: return False
    # invalid target: no cards
    if len(hands[target]) == 0: return False
    # invalid suit
    if not self.hasSuit(currentPlayer, card[SUIT]): return False
    # invalid card
    if self.hasCard(currentPlayer, card): return False

    # valid
    return True

  def resolveAsk(self, currentPlayer, target, card):
    try:
      index = self.hands[target].index(card)
      self.hands[currentPlayer].append(self.hands[target].pop(index))
      return True
    except ValueError:
      return False

  def hasSuit(player, suit):
    for c in self.hands[player]:
      if c[SUIT] == suit:
        return True
    return False

  def hasCard(player, card):
    for c in self.hands[player]:
      if c == card:
        return True
    return False
  
  def getDeclarations(self, currentPlayer):
    lastDeclaration = 0
    # ends at two times around the circle without anyone declaring anything 
    while (lastDeclaration < self.numPlayers*2):
      # get the current player to declare a suit
      (suit, attrib) = self.players[currentPlayer].getDeclaration() # PLAYER CALL
      # determine whether the target has the card or not
      declarationSuccesful = self.resolveDeclaration(currentPlayer, suit, attrib)

      # tell everyone what happened
      for (p : self.players):
        p.tellDeclaration(currentPlayer, suit, attrib, declarationSuccessful) # PLAYER CALL

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

    trueAttrib = self.killSuit(suit)

    if len(attrib) != NUMVALUES:
      # invalid attributation
      score[opponents] += 1
      return False

    for (player in trueAttrib):
      if (currentPlayer - player) % 2 == 1:
        # card held by opposing team
        score[opponents] += 1
        return False

    if attrib == trueAttrib
      # correct declaration
      score[team] += 1
      return True

    # incorrect attributions
    score[opponents] += 1
    return False

  def killSuit(self, suit):
    trueAttrib = [-1] * NUMVALUES
    for i in range(NUMPLAYERS):
      hand = hands[i]
      for card in hand:
        if card[SUIT] == suit:
          trueAttrib[card[VALUE]] = i
          hand.pop(hand.index(card))
    return trueAtrib

  def gameOver(self):
    team0count = sum(map(len, hands[0::2]))
    team1count = sum(map(len, hands[1::2]))

    # game over when one team has no more cards
    return (team0count * team1count) == 0
