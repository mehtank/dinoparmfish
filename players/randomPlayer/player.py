import random
from ..engine import card

class player:
  def debug(self, s):
    print "Player " + repr(self.index) + ": ",
    print s

  def setup(self, index, numPlayers, hand):
    self.index = index
    self.numPlayers = numPlayers
    self.hand = hand

    s = "Initialized : "
    for c in hand:
      s += "\n  " + repr(c)

    self.debug(s)

  def passTo(self):
    return (index + 2) % numPlayers;

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
    self.debug("asking player " + repr(target) + " for " + repr(ask))
    return (target, ask)

  def tellAsk(self, currentPlayer, target, card, askSuccessful):
    if askSuccessful:
      if (target == self.index):
        self.hand.pop(self.hand.index(card))
      if (currentPlayer == self.index):
        self.debug("Got " + repr(card) + " from player " + repr(target))
        self.hand.append(card)

  def getDeclaration(self):
    for suit in range(card.NUMSUITS):
      count = 0
      for c in self.hand:
        if c.suit == suit:
          count += 1
      if count == card.NUMVALUES:
        self.debug("Declaring suit: " + repr(suit))
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

