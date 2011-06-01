NUMVALUES = 6
NUMSUITS = 8

class card:
  suit = -1
  value = -1

  def __init__(self, suit, value):
    self.suit = suit
    self.value = value

  def __eq__(self, other):
    return (self.suit == other.suit) and (self.value == other.value)

  def __repr__(self):
    return "<" + repr(self.value) + " of " + repr(self.suit) + ">"
