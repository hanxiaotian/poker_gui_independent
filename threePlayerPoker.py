from copy import deepcopy
from UI_class import *

class Poker3:

    def __init__(self, game_state):
        game_state.player0_cards.sort()
        game_state.player1_cards.sort()
        game_state.player2_cards.sort()
        self.deck = Deck()
        self.player0_hand = Hand([VALUES2CARDS[c] for c in game_state.player0_cards], self.deck)
        self.player1_hand = Hand([VALUES2CARDS[c] for c in game_state.player1_cards], self.deck)
        for card in self.player1_hand:
            card.upward = False
        self.player2_hand = Hand([VALUES2CARDS[c] for c in game_state.player2_cards],  self.deck)
        for card in self.player2_hand:
            card.upward = False
        self.pub_cards = Hand([VALUES2CARDS[c] for c in game_state.pub_cards],  self.deck)

        self.player0_move = []
        self.player1_move = []
        self.player2_move = []
        self.lord_pos = game_state.lord_pos

    def val_action2card_action(self, val_act, hand):
        res = []
        j = 0
        for i in range(len(hand)):
            if j >= len(val_act):
                break
            if hand[i].rank == val_act[j]:
                res.append(hand[i])
                j += 1
                continue
        return res

    def update_player_hand(self, move, hand):
        for c in move:
            hand.remove(c)

    def get_player0_move(self):
        temp_move = []
        for c in self.player0_hand:
            if not c.upward:
                temp_move.append(c)
        return temp_move

    def check_win(self):
        if len(self.player0_hand) == 0 or len(self.player1_hand) == 0 or len(self.player2_hand) == 0:
            return True
        return False

    def dealpub(self):
        if self.lord_pos == 0:
            self.player0_hand += deepcopy(self.pub_cards)
            self.player0_hand.sort()
        elif self.lord_pos == 1:
            self.player1_hand += deepcopy(self.pub_cards)
            self.player1_hand.sort()
            for card in self.player1_hand:
                card.upward = False
        elif self.lord_pos == 2:
            self.player2_hand += deepcopy(self.pub_cards)
            self.player2_hand.sort()
            for card in self.player2_hand:
                card.upward = False


    def act_call(self, act):
        if not send_action2env([act]):
            return False
        self.player0_move = [act]
        cur_game_state = get_game_state()
        self.lord_pos = cur_game_state.lord_pos
        if self.lord_pos is not None:
            self.dealpub()
            return True

        nxt_game_state = get_game_state(True)
        player1_action = nxt_game_state.player1_actions[-1]
        self.player1_move = player1_action
        self.lord_pos = nxt_game_state.lord_pos
        if self.lord_pos is not None:
            self.dealpub()
            return True

        nxt_game_state = get_game_state()
        player2_action = nxt_game_state.player2_actions[-1]
        self.player2_move = player2_action
        self.lord_pos = nxt_game_state.lord_pos
        if self.lord_pos is not None:
            self.dealpub()
            return True

        return True

    def act(self, s=None):
        player0_action = self.get_player0_move()
        if s is not None:
            player0_action = s
        if not send_action2env([c.rank for c in player0_action]):
            return False
        self.player0_move = player0_action
        for c in self.player0_move:
            c.upward = True
        self.update_player_hand(self.player0_move, self.player0_hand)

        nxt_game_state = get_game_state(True)
        player1_action = nxt_game_state.player1_actions[-1]
        self.player1_move = self.val_action2card_action(player1_action, self.player1_hand)
        for c in self.player1_move:
            c.upward = True
        self.update_player_hand(self.player1_move, self.player1_hand)

        nxt_game_state = get_game_state()
        player2_action = nxt_game_state.player2_actions[-1]
        self.player2_move = self.val_action2card_action(player2_action, self.player2_hand)
        for c in self.player2_move:
            c.upward = True
        self.update_player_hand(self.player2_move, self.player2_hand)

        return True


class GameState(object):
    def __init__(self, player0_cards, player1_cards, player2_cards, pub_cards, player0_actions, player1_actions,
                 player2_actions, cur_player, lord_pos=None, is_finished=False, winner=None):
        self.player0_cards = player0_cards
        self.player1_cards = player1_cards
        self.player2_cards = player2_cards
        self.pub_cards = pub_cards
        self.player0_actions = player0_actions
        self.player1_actions = player1_actions
        self.player2_actions = player2_actions
        self.cur_player = cur_player
        self.lord_pos = lord_pos
        self.is_finished = is_finished
        self.winner = winner


def get_game_state(game_proceed=False):
    # TODO get game state from env
    #  if game_proceed is true, after get game state, env proceed one step further

    gs = GameState([3, 3, 4, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 20, 30],
                    [3, 4, 5, 6, 6, 7, 7, 8, 8, 9, 10, 11, 12, 13, 14, 17],
                    [3, 4, 5, 6, 7, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 14, 17],
                    [13, 14, 17], [[0]], [[0]], [[1]], 0, 1)
    return gs
    pass

def send_action2env(action):
    # TODO send human player(player 0) action to env
    #  if valid, return true and env proceed to next step
    #  else return false and env remain the same
    return True
    pass