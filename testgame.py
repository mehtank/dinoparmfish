from engine import game
from players.randomPlayer import player as rp

p1 = rp.Player(debug=True)
p2 = rp.Player()
p3 = rp.Player()
p4 = rp.Player()
p5 = rp.Player()
p6 = rp.Player()

team0 = [p1, p3, p5]
team1 = [p2, p4, p6]

g = game.Game(team0, team1, debug=True)

score = g.go()

print repr(score)
