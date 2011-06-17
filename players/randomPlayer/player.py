import random
from ..engine import card

class player:
  def output(self, s):
    if not self.debug:
      return
    print "Player " + repr(self.index) + ": ",
    print s

  def __init__(self, debug=False):
    self.debug = debug

  def setup(self, index, handSizes, hand):
    self.index = index
    self.numPlayers = len(handSizes)
    self.hand = hand

    s = "Initialized : "
    for c in hand:
      s += "\n  " + repr(c)

    self.output(s)

  def passTo(self):
    return (self.index + 2) % self.numPlayers;

  def getAsk(self):
    target = random.randint(0, (self.numPlayers / 2) - 1)
    target = target * 2 + 1
    target = (target + self.index) % self.numPlayers

    myCard = random.choice(self.hand)
    values = range(card.NUMVALUES)
    for c in self.hand:
      if c.suit == myCard.suit:
        values.pop(values.index(c.value))
    value = random.choice(values)

    ask = card.card(suit=myCard.suit, value=value)
    self.output("asking player " + repr(target) + " for " + repr(ask))
    return (target, ask)

  def tellAsk(self, currentPlayer, target, card, askSuccessful):
    if askSuccessful:
      if (target == self.index):
        self.output("Gave " + repr(card) + " to player " + repr(currentPlayer))
        self.hand.pop(self.hand.index(card))
      if (currentPlayer == self.index):
        self.output("Got " + repr(card) + " from player " + repr(target))
        self.hand.append(card)

  def getDeclaration(self):
    for suit in range(card.NUMSUITS):
      count = 0
      for c in self.hand:
        if c.suit == suit:
          count += 1
      if count == card.NUMVALUES:
        self.output("Declaring suit: " + repr(suit))
        return (suit, [self.index] * card.NUMVALUES)
    else:
      return (None, None)

  def tellDeclaration(self, currentPlayer, suit, attrib, declarationSuccessful):
    if declarationSuccessful is None:
      return
    topop = []
    for c in self.hand:
      if c.suit == suit:
        topop.append(c)
    for c in topop:
      self.hand.pop(self.hand.index(c))

