import math
import sys
import pygame


class Menu:
    def __init__(self, screen):
        self.screen = screen
        # Font Initialization
        self.pri_font = pygame.font.Font("fonts/Berry Rotunda.ttf", 16)
        self.sec_font = pygame.font.Font("fonts/Berry Rotunda.ttf", 14)
        self.thi_font = pygame.font.Font("fonts/Berry Rotunda.ttf", 18)
        self.fou_font = pygame.font.Font("fonts/Berry Rotunda.ttf", 12)
        # Image Initialization
        self.i_frame = pygame.image.load("images/Frame.png").convert_alpha()
        # Sprite Initialization
        self.states_babe = [pygame.image.load("images/babe_crouch.png").convert_alpha(),
                            pygame.image.load("images/babe_stand.png").convert_alpha()]
        self.states_knight = [pygame.image.load("images/walk_1.png").convert_alpha(),
                              pygame.image.load("images/walk_2.png").convert_alpha(),
                              pygame.image.load("images/walk_3.png").convert_alpha()]
        self.knight_charge = pygame.image.load("images/charging.png").convert_alpha()
        self.knight_idle = pygame.image.load("images/stand.png").convert_alpha()
        self.k_ind = 0

        # State Variables
        self.direct = False
        self.charging = False
        self.game_finished = False

        # Action Variables
        self.charge = 0
        self.switch = 0

        # Menu Bar Activation
        self.menubar_open = False

        # Audio Initialization
        self.menu_music = pygame.mixer.Sound("audios/openingProduction.mp3")
        self.victory_music = pygame.mixer.Sound("audios/Victory.mp3")
        self.menu_music.set_volume(0.5)    # Sets original audio volume to half
        self.victory_music.set_volume(0.5)

        self.menu_music.play(loops=-1)  # Begins to play menu music



    def HomeScreen(self, cont, play, instruc, quit_x, stats, host):
        self.screen.blit(pygame.image.load("images/JumpKingMenuScreen.jpg").convert_alpha(), (0, 0))  # Background

        boarder = pygame.Rect(5, 5, 690, 490)

        # Importing Images
        b_start = pygame.transform.scale(pygame.image.load("images/NewGameButton.jpg").convert_alpha(), (85, 20))
        b_continue = pygame.transform.scale(pygame.image.load("images/ButtonContinue.jpg").convert_alpha(), (80, 25))
        b_quit = pygame.transform.scale(pygame.image.load("images/QuitButton.jpg").convert_alpha(), (50, 20))
        option_frame = pygame.transform.scale(self.i_frame, (200, 155))
        data_frame = pygame.transform.scale(self.i_frame, (300, 145))
        cursor = pygame.transform.scale(pygame.image.load("images/ArrowDisplay.png").convert_alpha(), (25, 20))

        # Initializing Texts
        t_instruc = self.sec_font.render("Controls", False, "white")

        t_attempts = self.pri_font.render(f"Attempts: {stats[0]}", False, "white")
        t_jumps = self.pri_font.render(f"Jumps: {stats[1]}", False, "white")
        t_games = self.pri_font.render(f"Time: {self.timeConversion(stats[2])}", False, "white")

        # Creating Corresponding Rectangles
        b_start_rect = b_start.get_rect(topleft=(120, 300))
        b_continue_rect = b_continue.get_rect(topleft=(120, 260))
        b_quit_rect = b_quit.get_rect(topleft=(120, 370))
        b_controls_rect = t_instruc.get_rect(topleft=(125, 340))

        # Outputting
        pygame.draw.rect(self.screen, "white", boarder, width=5)  # Boarder

        # Option Panel
        self.screen.blit(option_frame, (75, 250))  # Frame
        if stats[2] > 0 and not cont:  self.screen.blit(b_continue, (120, 260))
        self.screen.blit(b_start, (120, 300))
        self.screen.blit(t_instruc, (125, 340))
        self.screen.blit(b_quit, (122, 370))

        # User's Stats
        self.screen.blit(data_frame, (325, 250))  # Frame
        self.screen.blit(t_attempts, (375, 275))
        self.screen.blit(t_jumps, (400, 310))
        self.screen.blit(t_games, (375, 345))
        # Only displays if the user finished the game
        if self.game_finished:
            # Image Import
            staple_completion = pygame.transform.rotate(pygame.image.load("images/finished.png").convert_alpha(), -30)
            self.screen.blit(staple_completion, (525, 265))

        # System Scanning (User Interaction)
        mx, my = pygame.mouse.get_pos()
        l_click, mid_click, r_click = pygame.mouse.get_pressed()
        if 75 < mx < 275 and 250 < my < 405:  # If the Cursor is in the Selection Box
            if my < 280 and stats[2] > 0 and not cont:  # Mouse Hovering over the continue button
                self.screen.blit(cursor, (95, 261))

            elif my < 320:  # Mouse hovering over the new game button
                self.screen.blit(cursor, (95, 301))

            elif my < 355:  # Mouse hovering over the controls button
                self.screen.blit(cursor, (95, 336))

            elif my < 400:  # Mouse hovering over the quit button
                self.screen.blit(cursor, (95, 370))

            # Button Interactions
            if b_continue_rect.collidepoint(mx, my) and l_click and not cont:  # Continue Button is pressed
                play = True
                cont = True
                stats[0] += 1
                self.menu_music.stop()   # Stops the Music

            elif b_start_rect.collidepoint(mx, my) and l_click:  # Start Game is pressed
                play = True
                cont = False
                self.game_finished = False
                stats[0] = 1
                # Setting to Said Level
                host.bg = pygame.image.load("images/background.png").convert_alpha()
                host.nxt_lvl = ["12", "11", "10", "9", "8", "7", "6", "5", "4", "3", "2", "1", "beg"]
                host.prev_lvl = []
                # Resetting Player's Sprite
                host.player.x = 50
                host.player.y = 500
                host.player.rect.bottom = 500
                host.player.rect.left = 50
                self.menu_music.stop()  # Stops the Music

            elif b_controls_rect.collidepoint(mx, my) and l_click:  # Controls button is pressed
                instruc = True

            elif b_quit_rect.collidepoint(mx, my) and l_click:  # Quit Button is pressed
                quit_x = True

        return cont, play, instruc, quit_x, stats

    def Controls(self, instruc, ind):
        # Boarder Rec Initialization
        boarder = pygame.Rect(5, 5, 690, 490)
        exit_boarder = pygame.Rect(645, 25, 30, 30)

        # Boarder Initialization
        title_frame = pygame.transform.scale(self.i_frame, (200, 50))
        babe_frame = pygame.transform.scale(self.i_frame, (60, 60))  # Frame to hold the babe sprite
        player_frame = pygame.transform.scale(self.i_frame, (75, 70))  # Frame to hold the knight sprite

        # Text Initialization
        exit_button = self.thi_font.render("X", True, "white")
        t_title = self.thi_font.render("How to Play", False, "white")  # Title
        # Instructions
        t_goal_1 = self.sec_font.render("Your goal is to reach the top of the castle", False, "white")
        t_goal_2 = self.sec_font.render("and save the babe.", False, "white")
        t_chargeJump_1 = self.sec_font.render("The longer you are holding the | SPACEBAR |", False, "white")
        t_chargeJump_2 = self.sec_font.render("the more power you will generate.", False, "white")
        t_bounce_walls = self.sec_font.render("Jumping towards the wall will make you bounce.", False, "white")
        t_movement_1 = self.sec_font.render("Holding | A | will move you towards the left", False, "white")
        t_movement_2 = self.sec_font.render("Holding | D | will move you towards the right", False, "white")
        # Headings
        t_babe = self.fou_font.render("Babe", False, "white")
        t_power = self.fou_font.render(f"Power: {self.charge}", False, "white")

        # Outputting
        self.screen.fill("black")  # Background
        pygame.draw.rect(self.screen, "white", boarder, width=5)  # Boarder
        pygame.draw.rect(self.screen, "white", exit_boarder, width=1)  # Button Rect
        self.screen.blit(exit_button, (650, 30))  # Button Text

        # Instructions
        self.screen.blit(title_frame, (240, 50))  # Frame
        self.screen.blit(t_title, (275, 65))  # Title
        self.screen.blit(t_goal_1, (75, 150))  # Objective
        self.screen.blit(t_goal_2, (75, 175))
        # Controls
        self.screen.blit(t_chargeJump_1, (75, 225))
        self.screen.blit(t_chargeJump_2, (75, 250))
        self.screen.blit(t_bounce_walls, (75, 300))
        self.screen.blit(t_movement_1, (75, 350))
        self.screen.blit(t_movement_2, (75, 375))
        # Sprites
        self.screen.blit(babe_frame, (555, 125))  # Babe Frame
        self.screen.blit(self.states_babe[ind], (560, 130))  # Babe Sprite
        self.screen.blit(t_babe, (565, 190))  # babe heading

        self.screen.blit(player_frame, (555, 300))  # Knight Frame
        self.screen.blit(t_power, (560, 280))  # Power heading

        keys = pygame.key.get_pressed()  # Gets Keyboard Input
        x, y = pygame.mouse.get_pos()  # Gets Cursor Location
        lclick, midclick, rclick = pygame.mouse.get_pressed()
        # System Interactions
        if exit_boarder.collidepoint(x, y) and lclick:  # If the X is clicked
            instruc = False

        # Knight Animations
        if keys[pygame.K_SPACE]:  # Charging
            self.screen.blit(self.knight_charge, (565, 330))
            if not self.charging:  # Getting Starting Time
                self.time = pygame.time.get_ticks()
            self.charging = True
            if int(pygame.time.get_ticks() - self.time) <= 400:  # Charging the power
                self.charge += 1

        elif keys[pygame.K_a]:  # Walking West
            self.switch += 1  # used for animating
            self.direct = True
            self.screen.blit(pygame.transform.flip(self.states_knight[self.k_ind], self.direct, False), (565, 310))

        elif keys[pygame.K_d]:  # Walking East
            self.switch += 1  # used for animating
            self.direct = False
            self.screen.blit(pygame.transform.flip(self.states_knight[self.k_ind], self.direct, False), (565, 310))

        else:  # Standing
            self.charge = 0
            self.charging = False
            self.screen.blit(pygame.transform.flip(self.knight_idle, self.direct, False), (565, 310))
        # Animating (Changing Index)
        if self.switch == 10:
            self.k_ind = self.k_ind + 1 if self.k_ind < 2 else 0
            self.switch = 0

        return instruc

    def MenuBar(self, host, play, cont):
        hex_colour = "#5A5A5A"
        # Importing Images
        b_menubar = pygame.transform.scale(pygame.image.load("images/menubar.png").convert_alpha(), (25, 15))
        c_selector = pygame.transform.scale(pygame.image.load("images/ArrowDisplay.png").convert_alpha(), (25, 20))

        # Init Text
        t_returnHome = self.fou_font.render("Home", False, "white")
        t_levels = self.pri_font.render("Stages", False, "white")
        t_levelOne = self.fou_font.render("Jungle", False, "white")
        t_levelTwo = self.fou_font.render("Clouds", False, "white")
        t_levelThree = self.fou_font.render("Space", False, "white")
        t_levelFour = self.fou_font.render("Castle", False, "white")

        # Init Rectangles
        b_menubarIcon_rect = pygame.Rect(660, 5, 35, 27)
        b_menubar_rect = pygame.Rect(600, 35, 95, 200)
        b_returnHome = t_returnHome.get_rect(topleft=(645, 50))
        b_levelOne_rect = t_levelOne.get_rect(topleft=(645, 115))
        b_levelTwo_rect = t_levelTwo.get_rect(topleft=(645, 145))
        b_levelThree_rect = t_levelThree.get_rect(topleft=(645, 175))
        b_levelFour_rect = t_levelFour.get_rect(topleft=(645, 205))

        # Outputting
        pygame.draw.rect(self.screen, hex_colour, b_menubarIcon_rect)
        self.screen.blit(b_menubar, (665, 10))

        x, y = pygame.mouse.get_pos()
        lclick, midclick, rclick = pygame.mouse.get_pressed()
        # System Interaction
        if b_menubarIcon_rect.collidepoint(x, y):  # Menubar activates when cursor hovers over icon
            self.menubar_open = True
        # Menu Bar activated
        if self.menubar_open and 600 < x < 700 and 5 < y < 230:
            pygame.draw.rect(self.screen, hex_colour, b_menubar_rect)  # Draws the background
            self.screen.blit(t_returnHome, (645, 50))  # Return Home Button
            self.screen.blit(t_levels, (625, 85))  # Stage Heading
            self.screen.blit(t_levelOne, (645, 115))    # Level One Button
            self.screen.blit(t_levelTwo, (645, 145))    # Level Two Button
            self.screen.blit(t_levelThree, (645, 175))  # Level Three Button
            self.screen.blit(t_levelFour, (645, 205))   # Level Four Button

            # Cursor Selector
            if 35 < y < 75:     # Hovering over Return Home Button
                self.screen.blit(c_selector, (605, 45))
            elif 110 < y < 130:  # Hovering over the Level One Button
                self.screen.blit(c_selector, (605, 110))
            elif 130 < y < 160:   # Hovering over the Level Two Button
                self.screen.blit(c_selector, (605, 140))
            elif 160 < y < 190:   # Hovering over the Level Three Button
                self.screen.blit(c_selector, (605, 170))
            elif 190 < y < 220: # Hovering Over the level Four Button
                self.screen.blit(c_selector, (605, 200))

            # Button Interactions
            if b_returnHome.collidepoint(x, y) and lclick:  # Return Home Button Clicked
                play = False
                cont = False
                self.menu_music.play(loops=-1)  # Plays music

            elif b_levelOne_rect.collidepoint(x, y) and lclick:   # Level One Button Clicked
                # Setting to Said Level
                host.bg = pygame.image.load("images/background.png").convert_alpha()
                host.nxt_lvl = ["12", "11", "10", "9", "8", "7", "6", "5", "4", "3", "2", "1", "beg"]
                host.prev_lvl = []
                # Resetting Player's Actions
                host.player.gravity = 0
                host.player.move_val = 0
                # Changing Player Position
                host.player.x = 50
                host.player.y = 500
                host.player.rect.bottom = 500
                host.player.rect.left = 50

            elif b_levelTwo_rect.collidepoint(x, y) and lclick: # Level Two Button Clicked
                # Setting to Said Level
                host.bg = pygame.image.load("images/nightSKy.jpg").convert_alpha()
                host.nxt_lvl = ["12", "11", "10", "9", "8", "7", "6", "5", "4", "3", "2", "1"]
                host.prev_lvl = ["beg"]
                # Resetting Player's Actions
                host.player.gravity = 0
                host.player.move_val = 0
                # Changing Player Position
                host.player.x = 450
                host.player.y = 500
                host.player.rect.bottom = 500
                host.player.rect.left = 450

            elif b_levelThree_rect.collidepoint(x, y) and lclick:   # Level Three Button Clicked
                # Setting to Said Level
                host.bg = pygame.image.load("images/Space.jpg").convert_alpha()
                host.nxt_lvl = ["12", "11", "10", "9", "8", "7"]
                host.prev_lvl = ["6", "5", "4", "3", "2", "1", "beg"]
                # Resetting Player's Actions
                host.player.gravity = 0
                host.player.move_val = 0
                # Changing Player Position
                host.player.x = 450
                host.player.y = 500
                host.player.rect.bottom = 500
                host.player.rect.left = 450

            elif b_levelFour_rect.collidepoint(x, y) and lclick:    # Level Four Button Clicked
                # Setting to Said Level
                host.bg = pygame.image.load("images/CastleWall.png").convert_alpha()
                host.nxt_lvl = ["12", "11", "10"]
                host.prev_lvl = ["9", "8", "7", "6", "5", "4", "3", "2", "1", "beg"]
                # Resetting Player's Actions
                host.player.gravity = 0
                host.player.move_val = 0
                # Changing Player Position
                host.player.x = 600
                host.player.y = 250
                host.player.rect.bottom = 250
                host.player.rect.left = 600

        else:  # Menu Bar deactivated
            self.menubar_open = False

        return play, cont

    def ClosingScreen(self, time, ceremony):
        self.screen.blit(pygame.image.load("images/EndingScreen.jpg").convert_alpha(), (0, 0))   # Background
        # Text Initial
        t_time = self.pri_font.render(f"Final Time: {self.timeConversion(time)}", True, "white")
        t_return = self.thi_font.render("X", False, "White")
        # Rect Initial
        b_return = pygame.Rect(10, 10, 30, 30)
        # Output
        self.screen.blit(t_time, (430, 30))     # Time
        pygame.draw.rect(self.screen, "white", b_return, width=2)
        self.screen.blit(t_return, (15, 15))
        # Mouse Interactions
        x, y = pygame.mouse.get_pos()
        lclick, midclick, rclick = pygame.mouse.get_pressed()
        if b_return.collidepoint(x, y) and lclick:
            ceremony = False
            self.victory_music.stop()   # Stops the victory music
            self.menu_music.play(loops=-1)  # Plays Menu Music

        return ceremony


    def timeConversion(self, time):     # Changes milliseconds into mins and seconds
        seconds = time/1000
        minutes = math.floor(seconds/60)
        seconds = math.floor(seconds - (60 * minutes))
        return f"  {minutes} m  {seconds} s"
