from UI_class import *

class Poker3:

    def __init__(self, lord_cards, farmerD_cards, farmerU_cards):
        lord_cards.sort(key=lambda x: CARDS2VALUES[x])
        farmerD_cards.sort(key=lambda x: CARDS2VALUES[x])
        farmerU_cards.sort(key=lambda x: CARDS2VALUES[x])
        self.deck = Deck()
        self.lord_hand = Hand(lord_cards, self.deck)
        self.farmerD_hand = Hand(farmerD_cards, self.deck)
        self.farmerU_hand = Hand(farmerU_cards, self.deck)
        self.lord_move = []
        self.farmerD_move = []
        self.farmerU_move = []

    def check_valid_move(self):
        lord_m = [card.rank for card in self.lord_move]
        lord_m_type = get_move_type(lord_m)

        if lord_m_type['type'] == TYPE_99_WRONG:
            return False

        farmD_m = [card.rank for card in self.farmerD_move]
        farmD_m_type = get_move_type(farmD_m)
        farmU_m = [card.rank for card in self.farmerU_move]
        farmU_m_type = get_move_type(farmU_m)

        last_move_type = farmU_m_type
        if farmU_m_type['type'] == TYPE_0_PASS:
            last_move_type = farmD_m_type

        if last_move_type['type'] == TYPE_0_PASS:
            if lord_m_type['type'] != TYPE_0_PASS:
                return True
            else:
                return False
        if lord_m_type['type'] == TYPE_0_PASS and last_move_type['type'] != TYPE_0_PASS:
            return True
        if lord_m_type['type'] == TYPE_5_KING_BOMB:
            return True
        if lord_m_type['type'] == TYPE_4_BOMB and last_move_type['type'] != TYPE_4_BOMB and last_move_type['type'] != TYPE_5_KING_BOMB:
            return True
        if lord_m_type['type'] == last_move_type['type'] and lord_m_type['rank'] > last_move_type['rank']:
            if 'serial_len' in lord_m_type:
                if lord_m_type['serial_len'] == last_move_type['serial_len']:
                    return True
                else:
                    return False
            else:
                return True
        return False

    def update_lord_hand(self):
        for c in self.lord_move:
            self.lord_hand.remove(c)

    def update_farmers_hand(self):
        for c in self.farmerD_move:
            self.farmerD_hand.remove(c)
        for c in self.farmerU_move:
            self.farmerU_hand.remove(c)

    def get_lord_move(self):
        self.lord_move.clear()
        for c in self.lord_hand:
            if c.selected:
                self.lord_move.append(c)

    def get_farmers_move(self):
        pass

    def reset_lord_move(self):
        self.lord_move.clear()

    def check_win(self):
        if len(self.lord_hand) == 0 or len(self.farmerD_hand) == 0 or len(self.farmerU_hand) == 0:
            return True
        return False
