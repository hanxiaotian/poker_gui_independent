import pygame
import os
import sys
import UI_class
import threePlayerPoker

HEIGHT = 720
WIDTH = 1280

# Global constants here
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (50, 50, 50)
RED = (207, 0, 0)


class Control:
    def __init__(self):
        deck = UI_class.Deck()
        self.images = {}
        self.scale = 0.5
        self.cardSize = (WIDTH / 10, WIDTH / 7)
        self.edge_width = 50
        self.background = pygame.image.load('img/background.jpg').convert_alpha()
        self.cardBack = pygame.image.load('img/back.png').convert_alpha()
        self.cardBack.set_alpha(0)
        self.cardBack = pygame.transform.scale(self.cardBack,
                                               (int(self.scale * self.cardSize[0]), int(self.scale * self.cardSize[1])))

        font = pygame.font.Font('font/CoffeeTin.ttf', 50)
        loadText = font.render("Loading...", 1, BLACK)
        loadSize = font.size("Loading...")
        loadLoc = (WIDTH / 2 - loadSize[0] / 2, HEIGHT / 2 - loadSize[1] / 2)

        SCREEN.blit(self.background, (-320, -100))

        SCREEN.blit(loadText, loadLoc)

        pygame.display.flip()

        for card in deck:
            s = str(card)
            self.images[s] = pygame.image.load(card.image_path).convert_alpha()
            self.images[s] = pygame.transform.scale(self.images[s], (
                int(self.scale * self.cardSize[0]), int(self.scale * self.cardSize[1])))

        self.state = 0
        self.player_num = 0

        self.start_init()

    def main(self):
        if self.player_num == 0:
            self.start()
        elif self.player_num == 3 and self.state == 1:
            self.play_call()
        elif self.player_num == 3 and self.state == 2:
            self.play3()
        elif self.state == 3:
            self.results()

    def start_init(self):
        font = pygame.font.Font('font/CoffeeTin.ttf', 100)

        self.startButton = font.render("Start", 1, BLACK)
        self.startButtonSize = font.size("Start")
        self.startButtonLoc = (WIDTH / 2 - self.startButtonSize[0] / 2,
                               HEIGHT / 2 - self.startButtonSize[1] / 2)
        self.startButtonRect = pygame.Rect(self.startButtonLoc, self.startButtonSize)
        self.startButtonRectOutline = pygame.Rect(self.startButtonLoc, self.startButtonSize)

    def start(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.startButtonRect.collidepoint(event.pos):
                    self.state += 1
                    self.player_num = 3
                    self.play_init3()
                    return
        # draw background
        SCREEN.blit(self.background, (-320, -100))

        # draw three player button
        pygame.draw.rect(SCREEN, RED, self.startButtonRect)
        pygame.draw.rect(SCREEN, BLACK, self.startButtonRectOutline, 2)
        SCREEN.blit(self.startButton, self.startButtonLoc)

        pygame.display.flip()

    def play_init3(self):
        self.poker = threePlayerPoker.Poker3(gs)

        # create the new variables
        self.pubcardLoc = {}
        self.player0cardLoc = {}
        self.player1cardLoc = {}
        self.player2cardLoc = {}
        self.player0MoveLoc = {}
        self.player1MoveLoc = {}
        self.player2MoveLoc = {}
        self.player0cardRects = []

        # setup game states
        self.update_3pgame_state()

        # setup the text that will be printed to the screen
        self.font = pygame.font.Font('font/IndianPoker.ttf', 35)
        self.font.set_bold(True)
        self.font2 = pygame.font.Font('font/CoffeeTin.ttf', 45)

        x = 1000
        self.playButton = self.font2.render(" Play ", 1, BLACK)
        self.buttonSize = self.font2.size(" Play ")
        self.playbuttonLoc = (x + 30, self.player0cardLoc[0][1] - 50)

        self.passButton = self.font2.render(" Pass ", 1, BLACK)
        self.passbuttonLoc = (x - self.buttonSize[0], self.player0cardLoc[0][1] - 50)

        self.playbuttonRect = pygame.Rect(self.playbuttonLoc, self.buttonSize)
        self.playbuttonRectOutline = pygame.Rect(self.playbuttonLoc, self.buttonSize)

        self.passbuttonRect = pygame.Rect(self.passbuttonLoc, self.buttonSize)
        self.passbuttonRectOutline = pygame.Rect(self.passbuttonLoc, self.buttonSize)

        x = 10
        # setup the text button used for call lord
        self.giveupButton = self.font2.render(" GiveUp ", 1, BLACK)
        self.giveupbuttonSize = self.font2.size(" GiveUp ")
        self.giveupbuttonLoc = (x, self.player0cardLoc[0][1] - 50)
        self.giveupbuttonRect = pygame.Rect(self.giveupbuttonLoc, self.giveupbuttonSize)
        self.giveupbuttonRectOutline = pygame.Rect(self.giveupbuttonLoc, self.giveupbuttonSize)

        self.callButton = self.font2.render(" Call ", 1, BLACK)
        self.callbuttonSize = self.font2.size(" Call ")
        self.callbuttonLoc = (x + self.giveupbuttonSize[0] + 20, self.player0cardLoc[0][1] - 50)
        self.callbuttonRect = pygame.Rect(self.callbuttonLoc, self.callbuttonSize)
        self.callbuttonRectOutline = pygame.Rect(self.callbuttonLoc, self.callbuttonSize)

        self.fightButton = self.font2.render(" Fight ", 1, BLACK)
        self.fightbuttonSize = self.font2.size(" Fight ")
        self.fightbuttonLoc = (x + self.giveupbuttonSize[0] + 20 + self.callbuttonSize[0] + 20, self.player0cardLoc[0][1] - 50)
        self.fightbuttonRect = pygame.Rect(self.fightbuttonLoc, self.fightbuttonSize)
        self.fightbuttonRectOutline = pygame.Rect(self.fightbuttonLoc, self.fightbuttonSize)

    def play_call(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # when the user clicks on a card, change its color to signify a selection has occurred
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # check if clicked the giveupButton
                if self.giveupbuttonRect.collidepoint(event.pos):
                    if self.poker.act_call(0):
                        break

                # check if clicked the callButton
                if self.callbuttonRect.collidepoint(event.pos):
                    if self.poker.act_call(1):
                        break

                # check if clicked the fightButton
                if self.fightbuttonRect.collidepoint(event.pos):
                    if self.poker.act_call(2):
                        break

        # display background
        SCREEN.blit(self.background, (-320, -100))

        # update game state
        self.update_3pgame_state()
        # display the Lord's hand
        self.display_cards(self.poker.player0_hand, self.player0cardLoc)
        # display the Farmer's hand
        self.display_cards(self.poker.player1_hand, self.player1cardLoc)
        self.display_cards(self.poker.player2_hand, self.player2cardLoc)
        # display the other player's action
        self.display_call(self.poker.player1_move, (self.player1cardLoc[0][0],
                         self.player1cardLoc[0][1] + int(self.scale * self.cardSize[1]) + 10))
        self.display_call(self.poker.player2_move, (self.player2cardLoc[0][0],
                         self.player2cardLoc[0][1] + int(self.scale * self.cardSize[1]) + 10))

        # display the text
        pygame.draw.rect(SCREEN, RED, self.giveupbuttonRect)
        pygame.draw.rect(SCREEN, BLACK, self.giveupbuttonRectOutline, 2)
        SCREEN.blit(self.giveupButton, self.giveupbuttonLoc)

        pygame.draw.rect(SCREEN, RED, self.callbuttonRect)
        pygame.draw.rect(SCREEN, BLACK, self.callbuttonRectOutline, 2)
        SCREEN.blit(self.callButton, self.callbuttonLoc)

        pygame.draw.rect(SCREEN, RED, self.fightbuttonRect)
        pygame.draw.rect(SCREEN, BLACK, self.fightbuttonRectOutline, 2)
        SCREEN.blit(self.fightButton, self.fightbuttonLoc)

        if self.poker.lord_pos is not None:
            #display public cards
            self.display_cards(self.poker.pub_cards, self.pubcardLoc)
            self.state += 1
            self.poker.player0_move.clear()
            self.poker.player1_move.clear()
            self.poker.player2_move.clear()

        pygame.display.flip()

    def play3(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # when the user clicks on a card, change its color to signify a selection has occurred
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for index in range(len(self.player0cardRects)):
                    if self.player0cardRects[index].collidepoint(event.pos):
                        self.poker.player0_hand[index].upward = not self.poker.player0_hand[index].upward
                        break

                # check if clicked the playButton
                if self.playbuttonRect.collidepoint(event.pos):
                    if self.poker.act():
                        break

                # check if clicked the passButton
                if self.passbuttonRect.collidepoint(event.pos):
                    if self.poker.act([]):
                        break

        # display background
        SCREEN.blit(self.background, (-320, -100))

        # update game state
        self.update_3pgame_state()
        # display the Lord's hand
        self.display_cards(self.poker.player0_hand, self.player0cardLoc)
        # display the Farmer's hand
        self.display_cards(self.poker.player1_hand, self.player1cardLoc)
        self.display_cards(self.poker.player2_hand, self.player2cardLoc)
        # display the Lord's move
        self.display_cards(self.poker.player0_move, self.player0MoveLoc)
        # display the Farmer's move
        self.display_cards(self.poker.player1_move, self.player1MoveLoc)
        self.display_cards(self.poker.player2_move, self.player2MoveLoc)
        # display public cards
        self.display_cards(self.poker.pub_cards, self.pubcardLoc)

        # display the text
        pygame.draw.rect(SCREEN, RED, self.playbuttonRect)
        pygame.draw.rect(SCREEN, BLACK, self.playbuttonRectOutline, 2)
        SCREEN.blit(self.playButton, self.playbuttonLoc)
        pygame.draw.rect(SCREEN, RED, self.passbuttonRect)
        pygame.draw.rect(SCREEN, BLACK, self.passbuttonRectOutline, 2)
        SCREEN.blit(self.passButton, self.passbuttonLoc)

        pygame.display.flip()

        if self.poker.check_win():
            self.state += 1
            self.results_init()
            return

    def results_init(self):
        if len(self.poker.player0_hand) == 0:
            text = "You Win"
        else:
            text = "You Lose"
        font = pygame.font.Font('font/IndianPoker.ttf', 150)
        self.resultButton = font.render(text, 1, BLACK)
        self.resultSize = font.size(text)
        self.resultbuttonLoc = (WIDTH / 2 - self.resultSize[0] / 2, HEIGHT / 2 - self.resultSize[1] / 2)

        font2 = pygame.font.Font('font/CoffeeTin.ttf', 45)
        self.replayButton = font2.render('retry', 1, BLACK)
        self.replaySize = font2.size('retry')
        self.replaybuttonLoc = (WIDTH / 2 - self.replaySize[0] / 2, HEIGHT - self.edge_width - self.replaySize[1])
        self.replaybuttonRect = pygame.Rect(self.replaybuttonLoc, self.replaySize)
        self.replaybuttonRectOutline = pygame.Rect(self.replaybuttonLoc, self.replaySize)

    def results(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.replaybuttonRect.collidepoint(event.pos):
                        self.state = 0
                        self.player_num = 0
                        self.start_init()
                        return

        # display background
        SCREEN.blit(self.background, (-320, -100))

        # draw the replay button
        pygame.draw.rect(SCREEN, RED, self.replaybuttonRect)
        pygame.draw.rect(SCREEN, BLACK, self.replaybuttonRectOutline, 2)
        SCREEN.blit(self.replayButton, self.replaybuttonLoc)
        SCREEN.blit(self.resultButton, self.resultbuttonLoc)

        pygame.display.flip()

    def display_call(self, call_act, locs):
        if len(call_act) == 0:
            return
        if call_act[0] == 0:
            SCREEN.blit(self.giveupButton, locs)
        elif call_act[0] == 1:
            SCREEN.blit(self.callButton, locs)
        else:
            SCREEN.blit(self.fightButton, locs)

    def display_cards(self, hand, locs):
        for index in range(len(hand)):
            SCREEN.blit(self.images[str(hand[index])], locs[index])
            if not hand[index].upward:
                SCREEN.blit(self.cardBack, locs[index])

    def _card_loc3_(self, res, num, width, height, overlap=False):
        x = width
        for i in range(num):
            res[i] = (x, height)
            if overlap:
                x += int(self.scale * self.cardSize[0]*0.3)
            else:
                x += int(self.scale * self.cardSize[0]*0.7)

    def update_3pgame_state(self):
        self.pubcardLoc.clear()
        self.player0cardLoc.clear()
        self.player1cardLoc.clear()
        self.player2cardLoc.clear()
        self.player0MoveLoc.clear()
        self.player1MoveLoc.clear()
        self.player2MoveLoc.clear()
        self.player0cardRects.clear()

        # setup the locations for each card in each player's hand
        self._card_loc3_(self.player0cardLoc, len(self.poker.player0_hand), 2 * int(self.scale * self.cardSize[0]),
                         HEIGHT - int(self.scale * self.cardSize[1]))
        self._card_loc3_(self.player1cardLoc, len(self.poker.player1_hand), WIDTH / 2, self.edge_width, True)
        self._card_loc3_(self.player2cardLoc, len(self.poker.player2_hand), 0, HEIGHT / 5 * 2 - self.edge_width, True)
        # setup the locations for moves of each player
        self._card_loc3_(self.player0MoveLoc, len(self.poker.player0_move), 2 * int(self.scale * self.cardSize[0]),
                         self.player0cardLoc[0][1] - int(self.scale * self.cardSize[1]) - 10)
        self._card_loc3_(self.player1MoveLoc, len(self.poker.player1_move), self.player1cardLoc[0][0],
                         self.player1cardLoc[0][1] + int(self.scale * self.cardSize[1]) + 10)
        self._card_loc3_(self.player2MoveLoc, len(self.poker.player2_move), self.player2cardLoc[0][0],
                         self.player2cardLoc[0][1] + int(self.scale * self.cardSize[1]) + 10)
        # setup the locations for public cards
        self._card_loc3_(self.pubcardLoc, len(self.poker.pub_cards), 1100, 350)
        # setup lord cards' rect to detect mouse click
        for index in range(len(self.poker.player0_hand)):
            self.player0cardRects.append(pygame.Rect(self.player0cardLoc[index], (int(self.scale * self.cardSize[0]*0.7),
                                                                                  int(self.scale * self.cardSize[1]))))

#############################################################
gs = threePlayerPoker.GameState([3,3,4,4,5,6,7,8,9,10,11,12,13,14,17,20,30],
                                [3,4,5,5,6,6,7,7,8,8,9,10,11,12,13,14,17],
                                [3,4,5,6,7,8,9,9,10,10,11,11,12,12,13,14,17],
                                [13,14,17], [], [], [], 0)
if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # center screen
    pygame.init()
    pygame.display.set_caption("CCP EndGame")
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

    main_loop = Control()
    Myclock = pygame.time.Clock()
    while 1:
        main_loop.main()
        Myclock.tick(16)
