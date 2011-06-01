from engine import game
from players.randomPlayer import player as rp

p1 = rp.player()
p2 = rp.player()
p3 = rp.player()
p4 = rp.player()
p5 = rp.player()
p6 = rp.player()

team0 = [p1, p3, p5]
team1 = [p2, p4, p6]

g = game.game(team0, team1)

score = g.go()

print repr(score)
