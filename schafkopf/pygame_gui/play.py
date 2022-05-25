from typing import List

import pygame

from schafkopf.pygame_gui.Button import Button
from schafkopf.pygame_gui.NextGameButton import NextGameButton
from schafkopf.pygame_gui.OpponentCard import OpponentCard
from schafkopf.pygame_gui.PlayerCard import PlayerCard
from schafkopf.pygame_gui.SchafkopfGame import SchafkopfGame
from schafkopf.pygame_gui.Widget import Widget
from schafkopf.pygame_gui.colors import BLACK

pygame.init()
FONT = pygame.font.Font(None, 30)

clock = pygame.time.Clock()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_size = screen_width, screen_height = screen.get_size()
background = pygame.transform.scale(pygame.image.load("../images/wood.jpg").convert(), screen_size)

space_between = 15
card_size = card_width, card_height = OpponentCard().rect.size

player_hand_position_height = screen_height * 95 / 100 - card_height
opposing_hand_position_height = screen_height * 5 / 100
neighboring_hand_edge_distance = screen_width * 5 / 100


def space_for_player_hand(num_cards):
    return num_cards * card_width + (num_cards - 1) * space_between


def player_hand_position_left(num_cards):
    return (screen_width - space_for_player_hand(num_cards)) / 2


def calculate_ith_card_position_player(i, player_hand):
    return (player_hand_position_left(len(player_hand)) + i * (card_width + space_between),
            player_hand_position_height)


def neighboring_hand_position_top(num_cards):
    return (screen_height - space_for_player_hand(num_cards)) / 2


def calculate_ith_card_position_first_opponent(num_cards, i):
    return (
        neighboring_hand_edge_distance,
        neighboring_hand_position_top(num_cards) + i * (card_width + space_between)
    )


def calculate_ith_card_position_second_opponent(num_cards, i):
    return (
        player_hand_position_left(num_cards) + i * (card_width + space_between),
        opposing_hand_position_height
    )


def calculate_ith_card_position_third_opponent(num_cards, i):
    return (
        screen_width - neighboring_hand_edge_distance - card_height,
        neighboring_hand_position_top(num_cards) + i * (card_width + space_between)
    )



class GameRunner:
    def __init__(self):
        self.leading_player_index = 0
        self.schafkopf_game = SchafkopfGame(leading_player_index=self.leading_player_index)
        self.widgets = self.get_widgets()
        self.done = False

    def next_game(self):
        self.leading_player_index += 1
        self.schafkopf_game = SchafkopfGame(self.leading_player_index)
        self.widgets = self.get_widgets()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.done = True
            buttons = [w for w in self.widgets if isinstance(w, Button)]
            for button in buttons:
                button.handle_event(event)

    def draw(self):
        screen.blit(background, (0, 0))
        for b in self.widgets:
            b.draw(screen)

        pygame.display.flip()

    def get_widgets(self) -> List[Widget]:
        return self.get_other_widgets() + self.get_buttons()

    def get_buttons(self) -> List[Button]:
        buttons = self.get_player_cards()
        if not self.schafkopf_game.bidding_is_finished():
            buttons += self.get_mode_proposals()
        buttons.append(NextGameButton((0, 0), self.next_game))
        return buttons

    def get_other_widgets(self) -> List[Widget]:
        if not self.schafkopf_game.finished():
            return self.get_opponent_cards()
        else:
            return []

    def foo(self, b):
        return lambda: print(b)

    def run(self):
        while not self.done:
            self.handle_events()
            self.draw()
            clock.tick(30)

    def get_player_cards(self) -> List[Button]:
        player_hand = self.schafkopf_game.get_player_hand()
        return [
            PlayerCard(
                topleft=calculate_ith_card_position_player(i, player_hand),
                card_encoded=card_encoded,
                hover_effect=False,
                callback=self.foo(card_encoded)
            ) for i, card_encoded in enumerate(player_hand)
        ]

    def get_opponent_cards(self) -> List[Widget]:
        first_opponent_hand, second_opponent_hand, third_opponent_hand = self.schafkopf_game.get_opponent_hands()
        first_opponent_cards = [
            OpponentCard(
                rotate=True,
                topleft=calculate_ith_card_position_first_opponent(len(first_opponent_hand), i)
            ) for i, _ in enumerate(first_opponent_hand)
        ]
        second_opponent_cards = [
            OpponentCard(
                rotate=False,
                topleft=calculate_ith_card_position_second_opponent(len(second_opponent_hand), i)
            ) for i, _ in enumerate(second_opponent_hand)
        ]
        third_opponent_cards = [
            OpponentCard(
                rotate=True,
                topleft=calculate_ith_card_position_third_opponent(len(third_opponent_hand), i)
            ) for i, _ in enumerate(third_opponent_hand)
        ]
        return first_opponent_cards + second_opponent_cards + third_opponent_cards

    def get_mode_proposals(self) -> List[Button]:
        return []


if __name__ == "__main__":
    GameRunner().run()
    pygame.quit()
