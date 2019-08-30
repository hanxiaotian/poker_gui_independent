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
            self.play3()
        elif self.state == 2:
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
        self.poker = threePlayerPoker.Poker3(['3','3','4','4','5','6','7','8','9','10','J','Q','K','A','2','SJ','BJ'],
                                ['3','4','5','5','6','6','7','7','8','8','9','10','J','Q','K','A','2'],
                                ['3','4','5','6','7','8','9','9','10','10','J','J','Q','Q','K','A','2'])

        # create the new variables
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

    def play3(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # when the user clicks on a card, change its color to signify a selection has occurred
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for index in range(len(self.player0cardRects)):
                    if self.player0cardRects[index].collidepoint(event.pos):
                        self.poker.lord_hand[index].upward = not self.poker.lord_hand[index].upward
                        break

                # check if clicked the playButton
                if self.playbuttonRect.collidepoint(event.pos):
                    self.poker.get_lord_move()
                    if self.poker.check_valid_move():
                        self.poker.get_farmers_move()
                        self.poker.update_farmers_hand()
                        self.poker.reset_lord_move()
                        break
                    else:
                        self.poker.reset_lord_move()

                # check if clicked the passButton
                if self.passbuttonRect.collidepoint(event.pos):
                    self.poker.reset_lord_move()
                    if self.poker.check_valid_move():
                        self.poker.get_farmers_move()
                        self.poker.update_farmers_hand()
                        break
                    else:
                        self.poker.reset_lord_move()

        if self.poker.check_win():
            self.state += 1
            self.results_init()
            return
        # display background
        SCREEN.blit(self.background, (-320, -100))

        # update game state
        self.update_3pgame_state()
        # display the Lord's hand
        self.display_cards(self.poker.lord_hand, self.player0cardLoc)
        # display the Farmer's hand
        self.display_cards(self.poker.farmerD_hand, self.player1cardLoc)
        self.display_cards(self.poker.farmerU_hand, self.player2cardLoc)
        # display the Lord's move
        self.display_cards(self.poker.lord_move, self.player0MoveLoc)
        # display the Farmer's move
        self.display_cards(self.poker.farmerD_move, self.player1MoveLoc)
        self.display_cards(self.poker.farmerU_move, self.player2MoveLoc)

        # display the text
        pygame.draw.rect(SCREEN, RED, self.playbuttonRect)
        pygame.draw.rect(SCREEN, BLACK, self.playbuttonRectOutline, 2)
        SCREEN.blit(self.playButton, self.playbuttonLoc)
        pygame.draw.rect(SCREEN, RED, self.passbuttonRect)
        pygame.draw.rect(SCREEN, BLACK, self.passbuttonRectOutline, 2)
        SCREEN.blit(self.passButton, self.passbuttonLoc)

        pygame.display.flip()

    def results_init(self):
        if len(self.poker.lord_hand) == 0:
            text = "NB"
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

    def display_cards(self, hand, locs, god_view=False):
        for index in range(len(hand)):
            if god_view:
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
        self.player0cardLoc.clear()
        self.player1cardLoc.clear()
        self.player2cardLoc.clear()
        self.player0MoveLoc.clear()
        self.player1MoveLoc.clear()
        self.player2MoveLoc.clear()
        self.player0cardRects.clear()
        # setup the locations for each card in each player's hand
        self._card_loc3_(self.player0cardLoc, len(self.poker.lord_hand), 2 * int(self.scale * self.cardSize[0]),
                         HEIGHT - int(self.scale * self.cardSize[1]))
        self._card_loc3_(self.player1cardLoc, len(self.poker.farmerD_hand), WIDTH / 2, self.edge_width, True)
        self._card_loc3_(self.player2cardLoc, len(self.poker.farmerU_hand), 0, HEIGHT / 5 * 2 - self.edge_width, True)
        # setup the locations for moves of each player
        self._card_loc3_(self.player0MoveLoc, len(self.poker.lord_move), 2 * int(self.scale * self.cardSize[0]),
                         self.player0cardLoc[0][1] - int(self.scale * self.cardSize[1]) - 10)
        self._card_loc3_(self.player1MoveLoc, len(self.poker.farmerD_move), self.player1cardLoc[0][0],
                         self.player1cardLoc[0][1] + int(self.scale * self.cardSize[1]) + 10)
        self._card_loc3_(self.player2MoveLoc, len(self.poker.farmerU_move), self.player2cardLoc[0][0],
                         self.player2cardLoc[0][1] + int(self.scale * self.cardSize[1]) + 10)
        # setup lord cards' rect to detect mouse click
        for index in range(len(self.poker.lord_hand)):
            self.player0cardRects.append(pygame.Rect(self.player0cardLoc[index], (int(self.scale * self.cardSize[0]*0.7),
                                                                                  int(self.scale * self.cardSize[1]))))

#############################################################
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
