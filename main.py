import pygame
import math
from sys import exit
import TitleScreens

pygame.init()  # Initializes Pygame
screen = pygame.display.set_mode((700, 500))
pygame.display.set_caption("Jump King")
clock = pygame.time.Clock()


# Class Initializations
class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()  # Initializes the inherited class
        # Sprite Image Import
        walk_1 = pygame.image.load("images/walk_1.png").convert_alpha()
        walk_idle = pygame.image.load("images/walk_2.png").convert_alpha()
        walk_3 = pygame.image.load("images/walk_3.png").convert_alpha()
        self.walk_frames = [walk_1, walk_idle, walk_3, walk_idle]
        self.index = 0  # 0-3

        self.number_of_jumps = 0

        # Animated States
        self.walking = False
        self.left_blocked, self.right_blocked = False, False
        self.charging = False
        self.collision_fall = False
        self.face = False  # Where is the sprite facing (True = Left, False = Right)
        self.bounce = None
        self.air = False    # Sprite is in mid-air

        # Positional Variables
        self.x = 50  #
        self.y = 500  # Default Starting Position
        self.jump_power = 0
        self.gravity = 0
        self.move_val = 3
        self.aerial = 0
        self.last_ground_pos = (self.x, self.y)

        # Importing Music
        self.collision_sfx = pygame.mixer.Sound("audios/Collision.mp3")
        self.land_sfx = pygame.mixer.Sound("audios/Landing.mp3")
        self.collision_sfx.set_volume(0.1)
        self.land_sfx.set_volume(0.1)

        self.image = pygame.image.load("images/stand.png").convert_alpha()  # Default State: Standing
        self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    def player_move(self):
        keys = pygame.key.get_pressed()  # List of Bools of keys pressed

        if keys[pygame.K_a] and not self.bounce:
            self.face = True  # Change facing direction (Left)
        elif keys[pygame.K_d] and not self.bounce:
            self.face = False  # Change facing direction (Right)

        # Sprite Movements
        if not self.charging:  # Prevents Player to move when charging its jump
            if keys[pygame.K_a] and not self.right_blocked:
                self.rect.x -= self.move_val
                self.x -= self.move_val  # Towards the Left
            elif keys[pygame.K_d] and not self.left_blocked:
                self.rect.x += self.move_val
                self.x += self.move_val  # Towards the Right

        if self.rect.bottom == self.y:  # If the Player is on the ground

            if keys[pygame.K_SPACE] and not self.walking:  # Holding Space will increase the power of the jump
                if not self.charging:
                    self.start_time = pygame.time.get_ticks()  # Starts the Timer (Max of 1/2 second of charging);
                    self.number_of_jumps += 1
                self.charging = True
                self.image = pygame.image.load("images/charging.png").convert_alpha()
                self.rect = self.image.get_rect(midbottom=(self.x, self.y))
                if int(pygame.time.get_ticks()) - int(self.start_time) < 400:
                    self.jump_power -= 1  # Increasing Jump Power

            elif self.rect.bottom + self.jump_power < self.y:  # The player is in the air
                # Updates new ground position
                self.last_ground_pos = self.rect.midbottom
                self.gravity = self.jump_power
                self.charging = False
                self.move_val = 6
                self.jump_power = 0  # Resets Jump Power
                self.image = pygame.transform.flip(pygame.image.load("images/jump.png").convert_alpha(), self.face,
                                                   False)
                self.rect = self.image.get_rect(midbottom=(self.x, self.y))

            elif (keys[pygame.K_a] or keys[pygame.K_d]) and not self.charging:  # Walking
                self.walking = True
                self.move_val = 2

            else:  # Idle (No Specific Key pressed)
                self.walking = False
                self.image = pygame.transform.flip(pygame.image.load("images/stand.png").convert_alpha(), self.face,
                                                   False)
                self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    def player_animation(self):
        if self.walking:
            self.index += 0.1
            if self.index > len(self.walk_frames): self.index = 0
            self.image = pygame.transform.flip(self.walk_frames[int(self.index)], self.face, False)
            self.rect = self.image.get_rect(midbottom=(self.x, self.y))

        elif self.collision_fall:  # Sprite Falling (With Collision)
            self.image = pygame.transform.flip(pygame.image.load("images/fall_collision.png").convert_alpha(),
                                               self.face, False)

        elif self.gravity > 0:  # Sprite Falling (No Collision)
            self.image = pygame.transform.flip(pygame.image.load("images/fall.png").convert_alpha(), self.face, False)

    def Bounce_off_wall(self):
        self.collision_fall = True
        # Bouncing off Right Wall
        if self.face:
            if self.last_ground_pos[0] + 45 > self.rect.midbottom[0] + 6:
                # Colliding with the opposite wall (left)
                if self.closest_leftRect.left < self.rect.right and self.closest_leftRect.top < self.rect.bottom and \
                        self.rect.midbottom[0] + 6 > self.last_ground_pos[0]:
                    self.bounce = False
                    self.y = 600  # Sets the user to fall
                # Colliding with a platform above
                elif self.rect.top - round(math.log(6, self.base_values[-1]),
                                           2) < self.closest_bottomRect.bottom and self.rect.clipline(
                    self.closest_bottomRect.left, self.closest_bottomRect.bottom, self.closest_bottomRect.right,
                    self.closest_bottomRect.bottom):
                    self.bounce = False
                    self.y = 600  # Set the user to fall
                    self.gravity = 5
                else:
                    self.x += 6
                    self.rect.x += 6
                    self.y -= round(math.log(6, self.base_values[-1]), 2)
                    self.rect.y -= round(math.log(6, self.base_values[-1]), 2)
                    self.base_values.pop()
            else:
                self.bounce = False
                self.y = 600  # Sets the user to fall

        # Bouncing off Left Wall
        elif not self.face:
            if self.last_ground_pos[0] - 45 < self.rect.midbottom[0] - 6:
                # Colliding with the opposite wall (right)
                if self.closest_rightRect.right > self.rect.left and self.closest_rightRect.top < self.rect.bottom and \
                        self.rect.midbottom[0] - 6 < self.last_ground_pos[0]:
                    self.bounce = False
                    self.y = 600  # Set the user to fall
                # Colliding with bottom of a platform above
                elif self.rect.top - round(math.log(6, self.base_values[-1]),
                                           2) < self.closest_bottomRect.bottom and self.rect.clipline(
                    self.closest_bottomRect.left, self.closest_bottomRect.bottom, self.closest_bottomRect.right,
                    self.closest_bottomRect.bottom):
                    self.bounce = False
                    self.y = 600  # Set the user to fall
                    self.gravity = 5
                else:
                    self.x -= 6
                    self.rect.x -= 6
                    self.y -= round(math.log(6, self.base_values[-1]), 2)
                    self.rect.y -= round(math.log(6, self.base_values[-1]), 2)
                    self.base_values.pop()
            else:
                self.bounce = False
                self.y = 600  # Set the user to fall

    def Find_Closest(self, rects, index):
        global pos_rects, ref_value
        if index == 0:  # Inspecting Top Side
            pos_rects = [x.top for x in rects]
            ref_value = self.rect.bottom

        elif index == 1:  # Inspecting Left Side
            pos_rects = [x.left for x in rects]
            ref_value = self.rect.right

        elif index == 2:  # Inspecting Right Side
            pos_rects = [x.right for x in rects]
            ref_value = self.rect.left

        elif index == 3:  # Inspecting Bottom Side
            pos_rects = [x.bottom for x in rects]
            ref_value = self.rect.top

        # Finding The Closest Floor through Height
        for i in range(1, len(rects)):
            j = i - 1
            key_pos = pos_rects[i]
            key_rect = rects[i]
            while j >= 0 and abs(ref_value - key_pos) < abs(ref_value - pos_rects[j]):
                pos_rects[j + 1] = pos_rects[j]
                rects[j + 1] = rects[j]
                j -= 1
            pos_rects[j + 1] = key_pos
            rects[j + 1] = key_rect
        return rects[0]

    def check_collision(self, rects):
        """
        Sorts the obstacle rectangles based off the current position of the player rectangle (sorted(...))
        """
        self.closest_topRect = self.Find_Closest(sorted(rects, key=lambda x: abs(self.rect.x - x.x)), 0)
        self.closest_bottomRect = self.Find_Closest(sorted(rects, key=lambda x: abs(self.rect.x - x.x)), 3)
        self.closest_leftRect = self.Find_Closest(sorted(rects, key=lambda x: abs(self.rect.y - x.y)), 1)
        self.closest_rightRect = self.Find_Closest(sorted(rects, key=lambda x: abs(self.rect.y - x.y)), 2)

        # Hitting Head Against the Top of the Floor
        if self.rect.clipline(self.closest_bottomRect.left, self.closest_bottomRect.bottom,
                              self.closest_bottomRect.right,
                              self.closest_bottomRect.bottom) and self.rect.top >= self.closest_bottomRect.bottom + self.gravity:
            self.gravity = 0
            self.collision_fall = True

        # Landing on an elevated Floor
        if self.rect.clipline(self.closest_topRect.left + 1, self.closest_topRect.top - self.gravity - 3,
                              self.closest_topRect.right - 1,
                              self.closest_topRect.top - self.gravity - 3) and self.rect.bottom <= self.closest_topRect.top:
            self.y = self.closest_topRect.top
            # Sprite landed
            if self.air:
                self.land_sfx.play()  # Plays land sfx
                self.air = False

                # Colliding with the Right side of a wall
        if self.rect.clipline(self.closest_rightRect.right, self.closest_rightRect.top, self.closest_rightRect.right,
                              self.closest_rightRect.bottom):
            if self.rect.bottom == self.y:  # Player on standing
                self.rect.left = self.closest_rightRect.right
                self.x += 2
                self.right_blocked = True
            elif self.gravity < 0:  # Bouncing
                self.collision_sfx.play()   # Plays collision sfx
                self.gravity = 0  # Resets the gravity value
                self.bounce = True  # Initiates the bouncing off the wall phase
                self.face = True  # Change facing direction to Left
                self.base_values = [1 + (x * 0.05) for x in
                                    range(int(abs(self.last_ground_pos[0] + 50 - self.closest_rightRect.right) / 6), 0,
                                          -1)]
            elif self.gravity > 0:  # User is falling
                self.move_val = 0  # Cannot Move in the air
                self.rect.x += 6  # Energy Released back (Prevents further bugs)
                self.collision_fall = True

        # Colliding with the Left side of a wall
        if self.rect.clipline(self.closest_leftRect.left, self.closest_leftRect.top, self.closest_leftRect.left,
                              self.closest_leftRect.bottom):
            if self.rect.bottom == self.y:  # Player Standing
                self.rect.right = self.closest_leftRect.left
                self.x -= 2
                self.left_blocked = True
            elif self.gravity < 0:  # Bouncing
                self.collision_sfx.play()  # Plays collision sfx
                self.gravity = 0  # Resets the gravity value
                self.bounce = True  # Initiates the bouncing off the wall Phase
                self.face = False  # Change facing direction to Right
                self.base_values = [1 + (x * 0.05) for x in
                                    range(int(abs(self.last_ground_pos[0] - 50 - self.closest_leftRect.left) / 6), 0,
                                          -1)]
            elif self.gravity > 0:  # User is falling
                self.move_val = 0  # Cannot Move in the air
                self.rect.x -= 6  # Energy Released back (Prevents further bugs)
                self.collision_fall = True

                # Falling off a platform
        elif self.rect.right < self.closest_topRect.left or self.rect.left > self.closest_topRect.right:
            self.y = 600

        # Allowing Movement when not near an opposing wall (Facing Left)
        if self.rect.right != self.closest_leftRect.left or self.rect.bottom < self.closest_leftRect.top:
            self.left_blocked = False

        # Allowing Movement when not near an opposing wall (Facing Right)
        if self.rect.left != self.closest_rightRect.right or self.rect.bottom < self.closest_rightRect.top:
            self.right_blocked = False

    def apply_gravity(self):
        self.rect.y += self.gravity + 3
        if self.rect.bottom < self.y:
            self.gravity += 1 if self.gravity < 26 else 0  # Terminal Velocity
            self.walking = False
        else:
            self.gravity = 0
            self.rect.bottom = self.y
            self.collision_fall = False

    def update(self, objs):
        self.player_move()  # Get Input
        self.player_animation()  # Display Animations
        # Checks if the sprite is in the air
        if self.gravity != 0:
            self.air = True
        self.check_collision(objs)
        if self.bounce:
            self.move_val = 0
            self.Bounce_off_wall()
        else:
            self.apply_gravity()  #


# Levels
class Levels:

    def __init__(self, player):
        self.dark_gray = "#18191A"
        self.player = player
        self.bg = pygame.image.load("images/background.png").convert_alpha()
        # Levels
        self.nxt_lvl = ["12", "11", "10", "9", "8", "7", "6", "5", "4", "3", "2", "1", "beg"]
        self.prev_lvl = []
        self.game_complete = False
        # Babe Sprite
        self.babe1 = pygame.image.load("images/babe_stand.png").convert_alpha()
        self.babe2 = pygame.image.load("images/babe_crouch.png").convert_alpha()
        self.babe3 = pygame.image.load("images/babe_idle.png").convert_alpha()
        self.babe4 = pygame.image.load("images/babe_charge.png").convert_alpha()
        self.babe5 = pygame.image.load("images/babe_air.png").convert_alpha()
        self.babe6 = pygame.image.load("images/babe_land.png").convert_alpha()
        self.babe7 = pygame.image.load("images/babe_kiss.png").convert_alpha()

        self.frames = [self.babe1, self.babe2, self.babe3, self.babe4, self.babe5, self.babe6, self.babe7]
        self.ind = 0
        self.timer = 0
        self.rect = self.frames[5].get_rect(topleft=(625, 98))

    def Beginner_Room(self):  # Level One
        screen.blit(self.bg, (0, 0))

        # Barriers
        wall_left = pygame.Rect(-10, 0, 10, 500)
        wall_right = pygame.Rect(700, 0, 710, 500)
        wall_bottom = pygame.Rect(0, 500, 700, 550)

        # Platforms
        block1 = pygame.Rect(0, 350, 100, 50)
        block2 = pygame.Rect(300, 350, 50, 50)
        block3 = pygame.Rect(175, 200, 50, 300)
        block4 = pygame.Rect(550, 200, 50, 200)
        block5 = pygame.Rect(450, 0, 50, 50)
        block6 = pygame.Rect(600, 350, 100, 50)

        pygame.draw.rect(screen, "orange", wall_left)
        pygame.draw.rect(screen, "orange", wall_right)
        pygame.draw.rect(screen, "orange", wall_bottom)

        pygame.draw.rect(screen, "black", block1)
        pygame.draw.rect(screen, "black", block2)
        pygame.draw.rect(screen, "black", block3)
        pygame.draw.rect(screen, "black", block4)
        pygame.draw.rect(screen, "black", block5)
        pygame.draw.rect(screen, "black", block6)

        return [wall_right, wall_left, block1, block2, block3, block4, block5, block6, wall_bottom]

    def StageOne(self):
        screen.blit(self.bg, (0, 0))
        # Refer to Blueprint for block assignment
        block1 = pygame.Rect(450, 500, 50, 50)
        block2 = pygame.Rect(300, 450, 50, 50)
        block3 = pygame.Rect(0, 350, 125, 50)
        block4 = pygame.Rect(0, 100, 100, 50)
        block5 = pygame.Rect(50, 150, 50, 50)
        block6 = pygame.Rect(200, 50, 100, 150)
        block7 = pygame.Rect(250, 200, 50, 50)

        pygame.draw.rect(screen, "black", block1)
        pygame.draw.rect(screen, "black", block2)
        pygame.draw.rect(screen, "black", block3)
        pygame.draw.rect(screen, "black", block4)
        pygame.draw.rect(screen, "black", block5)
        pygame.draw.rect(screen, "black", block6)
        pygame.draw.rect(screen, "black", block7)

        return [block1, block2, block3, block4, block5, block6, block7]

    def StageTwo(self):
        screen.blit(self.bg, (0, 0))
        # Refer to Blueprint for block assignment
        block1 = pygame.Rect(475, 450, 50, 50)
        block2 = pygame.Rect(600, 200, 50, 50)
        block3 = pygame.Rect(450, 150, 50, 100)
        block4 = pygame.Rect(300, 150, 50, 100)
        block5 = pygame.Rect(150, 150, 50, 100)
        block6 = pygame.Rect(0, 150, 50, 100)

        pygame.draw.rect(screen, "black", block1)
        pygame.draw.rect(screen, "black", block2)
        pygame.draw.rect(screen, "black", block3)
        pygame.draw.rect(screen, "black", block4)
        pygame.draw.rect(screen, "black", block5)
        pygame.draw.rect(screen, "black", block6)

        return [block1, block2, block3, block4, block5, block6]

    def StageThree(self):
        # Setting the Background
        screen.blit(self.bg, (0, 0))
        # Initializing Course
        block1 = pygame.Rect(350, 450, 100, 50)
        block4 = pygame.Rect(600, 350, 50, 50)
        block5 = pygame.Rect(450, 150, 50, 50)
        block6 = pygame.Rect(300, 150, 50, 50)
        block7 = pygame.Rect(150, 150, 50, 50)
        block8 = pygame.Rect(200, 0, 350, 50)
        # Drawing Course
        pygame.draw.rect(screen, "black", block1)
        pygame.draw.rect(screen, "black", block4)
        pygame.draw.rect(screen, "black", block5)
        pygame.draw.rect(screen, "black", block6)
        pygame.draw.rect(screen, "black", block7)
        pygame.draw.rect(screen, "black", block8)

        return [block1, block4, block5, block6, block7, block8]

    def StageFour(self):
        # Setting the Background
        screen.blit(self.bg, (0, 0))
        # Initializing Course
        block1 = pygame.Rect(200, 450, 350, 50)
        block4 = pygame.Rect(400, 100, 50, 150)
        block5 = pygame.Rect(150, 50, 50, 50)
        block6 = pygame.Rect(650, 250, 50, 50)
        # Drawing Course
        pygame.draw.rect(screen, "black", block1)
        pygame.draw.rect(screen, "black", block4)
        pygame.draw.rect(screen, "black", block5)
        pygame.draw.rect(screen, "black", block6)

        return [block1, block4, block5, block6]

    def StageFive(self):
        # Setting the Background
        screen.blit(self.bg, (0, 0))
        # Initializing Course
        block1 = pygame.Rect(0, 350, 50, 50)
        block2 = pygame.Rect(150, 150, 50, 50)
        # Drawing Course
        pygame.draw.rect(screen, "black", block1)
        pygame.draw.rect(screen, "black", block2)

        return [block1, block2]

    def StageSix(self):
        # Setting the Background
        screen.blit(self.bg, (0, 0))
        # Initializing Course
        block1 = pygame.Rect(0, 450, 50, 50)
        block2 = pygame.Rect(250, 350, 50, 50)
        block3 = pygame.Rect(550, 250, 50, 50)
        block4 = pygame.Rect(450, 0, 50, 50)
        # Drawing Course
        pygame.draw.rect(screen, "black", block1)
        pygame.draw.rect(screen, "black", block2)
        pygame.draw.rect(screen, "black", block3)
        pygame.draw.rect(screen, "black", block4)

        return [block1, block2, block3, block4]

    def StageSeven(self):
        # Setting the Background
        screen.blit(self.bg, (0, 0))
        # Initializing Course
        block1 = pygame.Rect(150, 350, 50, 50)
        block2 = pygame.Rect(0, 150, 50, 200)
        block3 = pygame.Rect(150, 200, 50, 50)
        block4 = pygame.Rect(300, 50, 50, 50)
        block5 = pygame.Rect(250, 450, 50, 50)
        block6 = pygame.Rect(450, 500, 50, 50)
        # Drawing Course
        pygame.draw.rect(screen, "black", block1)
        pygame.draw.rect(screen, "black", block2)
        pygame.draw.rect(screen, "black", block3)
        pygame.draw.rect(screen, "black", block4)
        pygame.draw.rect(screen, "black", block5)

        return [block1, block2, block3, block4, block5, block6]

    def StageEight(self):
        # Setting the Background
        screen.blit(self.bg, (0, 0))
        # Initializing Course
        block1 = pygame.Rect(500, 400, 50, 50)
        block2 = pygame.Rect(675, 200, 25, 200)
        block3 = pygame.Rect(500, 200, 50, 50)
        block4 = pygame.Rect(250, 350, 50, 50)
        block5 = pygame.Rect(250, 0, 100, 350)
        block6 = pygame.Rect(0, 0, 250, 400)
        block7 = pygame.Rect(350, 50, 50, 50)
        # Drawing Course
        pygame.draw.rect(screen, "black", block1)
        pygame.draw.rect(screen, "black", block2)
        pygame.draw.rect(screen, "black", block3)
        pygame.draw.rect(screen, self.dark_gray, block4)
        pygame.draw.rect(screen, self.dark_gray, block5)
        pygame.draw.rect(screen, self.dark_gray, block6)
        pygame.draw.rect(screen, self.dark_gray, block7)

        return [block1, block2, block3, block4, block5, block6, block7]

    def StageNine(self):
        # Setting the Background
        screen.blit(self.bg, (0, 0))
        # Initializing Course
        block1 = pygame.Rect(600, 450, 50, 50)
        block2 = pygame.Rect(350, 300, 50, 50)
        block3 = pygame.Rect(0, 250, 350, 250)
        block4 = pygame.Rect(0, 0, 700, 100)
        # Drawing Course
        pygame.draw.rect(screen, "black", block1)
        pygame.draw.rect(screen, self.dark_gray, block2)
        pygame.draw.rect(screen, self.dark_gray, block3)
        pygame.draw.rect(screen, self.dark_gray, block4)

        return [block1, block2, block3, block4]

    def StageTen(self):
        # Setting the Background
        screen.blit(self.bg, (0, 0))
        # Initializing Course
        block1 = pygame.Rect(450, 0, 250, 100)
        block2 = pygame.Rect(0, 250, 700, 200)
        block3 = pygame.Rect(0, 0, 100, 250)
        block4 = pygame.Rect(100, 50, 50, 50)
        # Drawing Course
        pygame.draw.rect(screen, self.dark_gray, block1)
        pygame.draw.rect(screen, self.dark_gray, block2)
        pygame.draw.rect(screen, self.dark_gray, block3)
        pygame.draw.rect(screen, self.dark_gray, block4)

        return [block1, block2, block3, block4]

    def StageEleven(self):
        # Setting the Background
        screen.blit(self.bg, (0, 0))
        # Initializing Course
        block1 = pygame.Rect(250, 400, 50, 50)
        block2 = pygame.Rect(400, 250, 50, 50)
        block3 = pygame.Rect(250, 100, 50, 50)
        block5 = pygame.Rect(0, 0, 100, 500)
        block6 = pygame.Rect(450, 0, 250, 500)
        # Drawing Course
        pygame.draw.rect(screen, self.dark_gray, block1)
        pygame.draw.rect(screen, self.dark_gray, block2)
        pygame.draw.rect(screen, self.dark_gray, block3)
        pygame.draw.rect(screen, self.dark_gray, block5)
        pygame.draw.rect(screen, self.dark_gray, block6)

        return [block1, block2, block3, block5, block6]

    def StageTwelve(self):
        # Setting the Background
        screen.blit(self.bg, (0, 0))
        # Initializing Course
        block3 = pygame.Rect(250, 200, 50, 50)
        block4 = pygame.Rect(0, 350, 100, 150)
        block5 = pygame.Rect(0, 250, 50, 500)
        block6 = pygame.Rect(0, 150, 100, 100)
        block7 = pygame.Rect(0, 15, 50, 100)
        block8 = pygame.Rect(0, 0, 700, 15)
        block9 = pygame.Rect(400, 150, 300, 350)
        # Drawing Course
        pygame.draw.rect(screen, self.dark_gray, block3)
        pygame.draw.rect(screen, self.dark_gray, block4)
        pygame.draw.rect(screen, self.dark_gray, block5)
        pygame.draw.rect(screen, self.dark_gray, block6)
        pygame.draw.rect(screen, self.dark_gray, block7)
        pygame.draw.rect(screen, self.dark_gray, block8)
        pygame.draw.rect(screen, self.dark_gray, block9)
        if not self.game_complete:   # Functions that only occur or get checked when not reached end
            # Displaying Babe Sprite
            screen.blit(self.frames[self.ind], (600, 98))
            # User Completes the Game
            if self.rect.colliderect(self.player.rect):
                self.game_complete = True
                self.ind = 0    # Resets animations
                self.timer = 0
            # Changing Index
            elif self.timer == 25:
                self.ind = self.ind + 1 if self.ind < 1 else 0
                self.timer = 0
        self.timer += 1

        return [block3, block4, block5, block6, block7, block8, block9]

    def playLevel(self):
        if self.nxt_lvl[-1] == "12":
            return self.StageTwelve()

        elif self.nxt_lvl[-1] == "11":
            return self.StageEleven()

        elif self.nxt_lvl[-1] == "10":
            return self.StageTen()

        elif self.nxt_lvl[-1] == "9":
            return self.StageNine()

        elif self.nxt_lvl[-1] == "8":
            return self.StageEight()

        elif self.nxt_lvl[-1] == "7":
            return self.StageSeven()

        elif self.nxt_lvl[-1] == "6":
            return self.StageSix()

        elif self.nxt_lvl[-1] == "5":
            return self.StageFive()

        elif self.nxt_lvl[-1] == "4":
            return self.StageFour()

        elif self.nxt_lvl[-1] == "3":
            return self.StageThree()

        elif self.nxt_lvl[-1] == "2":
            return self.StageTwo()

        elif self.nxt_lvl[-1] == "1":
            return self.StageOne()

        elif self.nxt_lvl[-1] == "beg":
            return self.Beginner_Room()

    def switchLevel(self):
        # Progression
        if self.nxt_lvl[-1] == 'beg' and self.player.rect.centery + 5 < 0:
            # Modifying
            self.player.rect.bottom = 500
            self.bg = pygame.image.load("images/nightSKy.jpg").convert_alpha()
            # Levels
            self.prev_lvl.append(self.nxt_lvl[-1])
            self.nxt_lvl.pop()

        elif self.nxt_lvl[-1] == '1' and self.player.rect.centery + 5 < 0:
            # Modifying
            self.player.rect.bottom = 500
            self.bg = pygame.image.load("images/nightSKy.jpg").convert_alpha()
            # Levels
            self.prev_lvl.append(self.nxt_lvl[-1])
            self.nxt_lvl.pop()

        elif self.nxt_lvl[-1] == '2' and self.player.rect.centery + 5 < 0:
            # Modifying
            self.player.rect.bottom = 500
            self.bg = pygame.image.load("images/nightSKy.jpg").convert_alpha()
            # Levels
            self.prev_lvl.append(self.nxt_lvl[-1])
            self.nxt_lvl.pop()

        elif self.nxt_lvl[-1] == '3' and self.player.rect.centery + 5 < 0:
            # Modifying
            self.player.rect.bottom = 500
            self.bg = pygame.image.load("images/nightSKy.jpg").convert_alpha()
            # Levels
            self.prev_lvl.append(self.nxt_lvl[-1])
            self.nxt_lvl.pop()

        elif self.nxt_lvl[-1] == '4' and self.player.rect.centery + 5 < 0:
            # Modifying
            self.player.rect.bottom = 500
            self.bg = pygame.image.load("images/nightSKy.jpg").convert_alpha()
            # Levels
            self.prev_lvl.append(self.nxt_lvl[-1])
            self.nxt_lvl.pop()

        elif self.nxt_lvl[-1] == '5' and self.player.rect.centery + 5 < 0:
            # Modifying
            self.player.rect.bottom = 500
            self.bg = pygame.image.load("images/nightSKy.jpg").convert_alpha()
            # Levels
            self.prev_lvl.append(self.nxt_lvl[-1])
            self.nxt_lvl.pop()

        elif self.nxt_lvl[-1] == '6' and self.player.rect.centery + 5 < 0:
            # Modifying
            self.player.rect.bottom = 500
            self.bg = pygame.image.load("images/Space.jpg").convert_alpha()
            # Levels
            self.prev_lvl.append(self.nxt_lvl[-1])
            self.nxt_lvl.pop()

        elif self.nxt_lvl[-1] == '7' and self.player.rect.centery + 5 < 0:
            # Modifying
            self.player.rect.bottom = 500
            self.bg = pygame.image.load("images/Space.jpg").convert_alpha()
            # Levels
            self.prev_lvl.append(self.nxt_lvl[-1])
            self.nxt_lvl.pop()

        elif self.nxt_lvl[-1] == '8' and self.player.rect.centery + 5 < 0:
            # Modifying
            self.player.rect.bottom = 500
            self.bg = pygame.image.load("images/Space.jpg").convert_alpha()
            # Levels
            self.prev_lvl.append(self.nxt_lvl[-1])
            self.nxt_lvl.pop()

        elif self.nxt_lvl[-1] == '9' and self.player.rect.centerx < 0:
            # Modifying
            self.player.rect.right = 700
            self.player.x = 670
            self.bg = pygame.image.load("images/CastleWall.png").convert_alpha()
            # Levels
            self.prev_lvl.append(self.nxt_lvl[-1])
            self.nxt_lvl.pop()

        elif self.nxt_lvl[-1] == '10' and self.player.rect.centery + 5 < 0:
            # Modifying
            self.player.rect.bottom = 500
            self.bg = pygame.image.load("images/CastleWall.png").convert_alpha()
            # Levels
            self.prev_lvl.append(self.nxt_lvl[-1])
            self.nxt_lvl.pop()

        elif self.nxt_lvl[-1] == '11' and self.player.rect.centery + 5 < 0:
            # Modifying
            self.player.rect.bottom = 500
            self.bg = pygame.image.load("images/CastleWall.png").convert_alpha()
            # Levels
            self.prev_lvl.append(self.nxt_lvl[-1])
            self.nxt_lvl.pop()

        elif self.nxt_lvl[-1] == '12' and self.player.rect.centery + 5 < 0:
            # Modifying
            self.player.rect.bottom = 500
            self.bg = pygame.image.load("images/CastleWall.png").convert_alpha()
            # Levels
            self.prev_lvl.append(self.nxt_lvl[-1])
            self.nxt_lvl.pop()

        # Regression
        elif self.nxt_lvl[-1] == '1' and self.player.rect.bottom > 500:
            # Modifying
            self.player.rect.centery = 0
            self.bg = pygame.image.load("images/background.png").convert_alpha()
            self.player.y = self.player.closest_topRect.top
            # Levels
            self.prev_lvl.pop()
            self.nxt_lvl.append("beg")

        elif self.nxt_lvl[-1] == '2' and self.player.rect.bottom > 500:
            # Modifying
            self.player.rect.centery = 0
            self.bg = pygame.image.load("images/nightSKy.jpg").convert_alpha()
            self.player.y = self.player.closest_topRect.top
            # Levels
            self.prev_lvl.pop()
            self.nxt_lvl.append("1")

        elif self.nxt_lvl[-1] == '3' and self.player.rect.bottom > 500:
            # Modifying
            self.player.rect.centery = 0
            self.bg = pygame.image.load("images/nightSKy.jpg").convert_alpha()
            self.player.y = self.player.closest_topRect.top
            # Levels
            self.prev_lvl.pop()
            self.nxt_lvl.append("2")

        elif self.nxt_lvl[-1] == '4' and self.player.rect.bottom > 500:
            # Modifying
            self.player.rect.centery = 0
            self.bg = pygame.image.load("images/nightSKy.jpg").convert_alpha()
            self.player.y = self.player.closest_topRect.top
            # Levels
            self.prev_lvl.pop()
            self.nxt_lvl.append("3")

        elif self.nxt_lvl[-1] == '5' and self.player.rect.bottom > 500:
            # Modifying
            self.player.rect.centery = 0
            self.bg = pygame.image.load("images/nightSKy.jpg").convert_alpha()
            self.player.y = self.player.closest_topRect.top
            # Levels
            self.prev_lvl.pop()
            self.nxt_lvl.append("4")

        elif self.nxt_lvl[-1] == '6' and self.player.rect.bottom > 500:
            # Modifying
            self.player.rect.centery = 0
            self.bg = pygame.image.load("images/nightSKy.jpg").convert_alpha()
            self.player.y = self.player.closest_topRect.top
            # Levels
            self.prev_lvl.pop()
            self.nxt_lvl.append("5")

        elif self.nxt_lvl[-1] == '7' and self.player.rect.bottom > 500:
            # Modifying
            self.player.rect.centery = 0
            self.bg = pygame.image.load("images/nightSKy.jpg").convert_alpha()
            self.player.y = self.player.closest_topRect.top
            # Levels
            self.prev_lvl.pop()
            self.nxt_lvl.append("6")

        elif self.nxt_lvl[-1] == '8' and self.player.rect.bottom > 500:
            # Modifying
            self.player.rect.centery = 0
            self.bg = pygame.image.load("images/Space.jpg").convert_alpha()
            self.player.y = self.player.closest_topRect.top
            # Levels
            self.prev_lvl.pop()
            self.nxt_lvl.append("7")

        elif self.nxt_lvl[-1] == '9' and self.player.rect.bottom > 500:
            # Modifying
            self.player.rect.centery = 0
            self.bg = pygame.image.load("images/Space.jpg").convert_alpha()
            self.player.y = self.player.closest_topRect.top
            # Levels
            self.prev_lvl.pop()
            self.nxt_lvl.append("8")

        elif self.nxt_lvl[-1] == '10' and self.player.rect.centerx > 700:
            # Modifying
            self.player.rect.left = 0
            self.player.x = 30
            self.bg = pygame.image.load("images/Space.jpg").convert_alpha()
            # Levels
            self.prev_lvl.pop()
            self.nxt_lvl.append("9")

        elif self.nxt_lvl[-1] == '11' and self.player.rect.bottom > 500:
            # Modifying
            self.player.rect.centery = 0
            self.bg = pygame.image.load("images/CastleWall.png").convert_alpha()
            self.player.y = self.player.closest_topRect.top
            # Levels
            self.prev_lvl.pop()
            self.nxt_lvl.append("10")

        elif self.nxt_lvl[-1] == '12' and self.player.rect.bottom > 500:
            # Modifying
            self.player.rect.centery = 0
            self.bg = pygame.image.load("images/CastleWall.png").convert_alpha()
            self.player.y = self.player.closest_topRect.top
            # Levels
            self.prev_lvl.pop()
            self.nxt_lvl.append("11")

    def Final_cutscene(self):
        # Placing Player In Position
        self.player.rect.right = 625
        self.player.image = pygame.image.load("images/stand.png").convert_alpha()
        # Displaying Babe Sprite
        screen.blit(self.frames[self.ind], (600, 98))
        if self.timer == 25:
            if self.ind == 6:
                self.game_complete = False
            else:
                self.ind += 1
                self.timer = 0


# Creating Player Group
player = pygame.sprite.GroupSingle()  # Creates the sprite group
player.add(Player())  # Adds our class: player to sprite group

# Initialization of Levels
room = Levels(player.sprite)

# Initialization of Timer
animation_timer = pygame.USEREVENT + 1
start_timer = False

# Initialization of Menu
menu = TitleScreens.Menu(screen)
# Menu Variables
cont = False
play = False
instruc = False
quit_x = False

player_time = 0
babe_index = 0
player_stats = [0, 0, 0]
closing_ceremony = False

# Main Code
while True:
    # Sets the timer and then disables after setting
    if start_timer:
        pygame.time.set_timer(animation_timer, 250)
        start_timer = False

    for event in pygame.event.get():
        if event.type == animation_timer:
            babe_index = 1 if babe_index == 0 else 0

        if event.type == pygame.QUIT or quit_x:
            pygame.quit()
            exit()

    # Instruction Screen is opened
    if instruc:
        instruc = menu.Controls(instruc, babe_index)
        if not instruc:  # If instruc tab is closed
            pygame.time.set_timer(animation_timer, 0, loops=0)  # Stop animating
    # Play New Game is called
    elif play:
        # Main Game Code
        hazards = room.playLevel()
        player.draw(screen)
        # When the Player Completes the game
        if room.game_complete:
            room.Final_cutscene()
            # When the Cutscene if over
            if not room.game_complete:    # Closing Ceremony
                player_stats[1] = player.sprite.number_of_jumps  # Updates Jump counter
                player_stats[2] = pygame.time.get_ticks() - player_time  # Updates Clock Timer
                closing_ceremony = True     # Starts Closing Ceremony
                menu.game_finished = True   # Game is finished
                menu.victory_music.play(loops=-1)   # Plays the victory music
                play = False
                cont = True  # Disables Continue button
        else:   # normal gameplay occurs
            player.update(hazards)
            room.switchLevel()
            play, cont = menu.MenuBar(room, play, cont)
            # When the player Exits from the game (either through menu or completion)
            if not play:
                player_stats[1] = player.sprite.number_of_jumps  # Updates Jump counter
                player_stats[2] = pygame.time.get_ticks() - player_time  # Updates Clock Timer

    # Closing Ceremony
    elif closing_ceremony:
        closing_ceremony = menu.ClosingScreen(player_stats[2], closing_ceremony)

    # Default Home Screen
    elif not play and not instruc:
        cont, play, instruc, quit_x, player_stats = menu.HomeScreen(cont, play, instruc, quit_x, player_stats, room)
        # Sets up the animation for instruc tab if the instruc tab is called
        if instruc:
            start_timer = True
        # Starts the Clock Time
        elif play and not cont:
            player.sprite.number_of_jumps = 0  # Resets
            player_time = pygame.time.get_ticks()

    pygame.display.update()
    clock.tick(60)  # Runs at 60fps
