#!/usr/bin/env python

from schafkopf.game import Game
from schafkopf.players import RandomPlayer

Alfons = RandomPlayer(name="Alfons")
Bertl = RandomPlayer(name="Bertha")
Chrissie = RandomPlayer(name="Chris")
Dora = RandomPlayer(name="Dora")

playerlist = [Alfons, Bertl, Chrissie, Dora]

testgame = Game(players=playerlist, leading_player=0)

testgame.decide_game_mode()
#testgame.define_trumpcards()
print("game mode :    ",testgame.get_game_mode())
print("trumpcards :  ",  testgame._trump_cards)

while not testgame.finished():
    testgame.play_next_card()
    print("current player :    ", testgame.get_current_playerindex())
    print("current trick  :    ", testgame.get_current_trick())
    print("Tricks :     " , testgame.get_tricks())
