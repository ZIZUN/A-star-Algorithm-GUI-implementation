import pygame
import time

BLACK = (0, 0, 0)
GREEN = (102, 255, 102)
LIGHTGREEN = (0, 51, 0)
RED = (255, 0, 0)
BLUE = (102, 102, 102)
YELLOW = (204, 0, 0)
REALYELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
WHITE = (255, 255, 255)


class Block():

    def __init__(self, screen, x, y, block):
        self.screen = screen
        self.x = x
        self.y = y
        self.block = block
        self.location_x = x * self.block
        self.location_y = y * self.block

        self.fill_color = WHITE
        self.border_color = BLACK

        # f = g + h
        self.f = 0
        self.g = 0
        self.h = 0

        self.text_size = self.block // 6
        self.type = 0
        self.father_direction = -1

    def draw_text(self, text, x, y):
        font = pygame.font.Font('freesansbold.ttf', self.text_size)
        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_direction(self):
        # down right

        if self.father_direction == 0:
            pygame.draw.line(self.screen, REALYELLOW,
                             (self.location_x + self.block // 4 - (14 / self.block/60) ,
                              self.location_y + self.block // 4 - (14 / self.block/60)),
                             (self.location_x + 3 * self.block // 4 + (14 / self.block/60),
                              self.location_y + 3 * self.block // 4 + (14 / self.block/60)), 5)
        # down
        elif self.father_direction == 1:
            pygame.draw.line(self.screen, REALYELLOW,
                             (self.location_x + self.block // 2,
                              self.location_y + self.block // 8 - (11 / self.block/60)),
                             (self.location_x + self.block // 2,
                              self.location_y + 3 * self.block // 4 + (11 / self.block/60)), 5)
        # down left
        elif self.father_direction == 2:
            pygame.draw.line(self.screen, REALYELLOW,
                             (self.location_x + 3 * self.block // 4 + (14 / self.block/60),
                              self.location_y + self.block // 4 - (14 / self.block/60)),
                             (self.location_x + self.block // 4 - (14 / self.block/60),
                              self.location_y + 3 * self.block // 4 + (14 / self.block/60)), 5)
        # right
        elif self.father_direction == 3:
            pygame.draw.line(self.screen, REALYELLOW,
                             (self.location_x + self.block // 8 - (11 / self.block/60),
                              self.location_y + self.block // 2),
                             (self.location_x + 3 * self.block // 4 + (11 / self.block/60),
                              self.location_y + self.block // 2), 5)

        # left
        elif self.father_direction == 4:
            pygame.draw.line(self.screen, REALYELLOW,
                             (self.location_x + self.block // 4 - (11 / self.block/60),
                              self.location_y + self.block // 2),
                             (self.location_x + 7 * self.block // 8 + (11 / self.block/60),
                              self.location_y + self.block // 2), 5)
        # up right
        elif self.father_direction == 5:
            pygame.draw.line(self.screen, REALYELLOW,
                             (self.location_x + self.block // 4 - (14 / self.block/60),
                              self.location_y + 3 * self.block // 4 + (14 / self.block/60)),
                             (self.location_x + 3 * self.block // 4 + (14 / self.block/60),
                              self.location_y + self.block // 4 - (14 / self.block/60)), 5)
        # up
        elif self.father_direction == 6:
            pygame.draw.line(self.screen, REALYELLOW,
                             (self.location_x + self.block // 2,
                              self.location_y + self.block // 4 - (11 / self.block/60)),
                             (self.location_x + self.block // 2,
                              self.location_y + 7 * self.block // 8 + (11 / self.block/60)), 5)
        # up left
        elif self.father_direction == 7:
            pygame.draw.line(self.screen, REALYELLOW,
                             (self.location_x + self.block // 4 - (14 / self.block/60),
                              self.location_y + self.block // 4 - (14 / self.block/60)),
                             (self.location_x + 3 * self.block // 4 + (14 / self.block/60),
                              self.location_y + 3 * self.block // 4 + (14 / self.block/60)), 5)

    def draw_rect(self):
        pygame.draw.rect(self.screen, self.fill_color, [
            self.location_x, self.location_y, self.block, self.block], 0)

        pygame.draw.rect(self.screen, self.border_color, [
            self.location_x, self.location_y, self.block, self.block], 3)

    def direc(self):
        return self.father_direction

    def draw(self):
        self.draw_rect()
        padding_x = 10
        padding_y = 10

    def draw_line(self):
        self.draw_direction()

    def set_start(self):
        self.fill_color = GREEN

    def set_obstacle(self):
        if self.fill_color == WHITE:
            self.fill_color = BLUE
            return True
        else:
            return False

    def set_end(self):
        if self.fill_color == WHITE:
            self.fill_color = RED
            return True
        else:
            return False
    def set_end2(self):
        self.fill_color = RED
        return True

    def set_empty_all(self):
        if self.fill_color == BLUE:
            self.fill_color = WHITE
            return True
        else:
            return False

    def set_empty_R(self):
        if self.fill_color == RED:
            self.fill_color = WHITE
            return True
        else:
            return False
    def set_empty_G(self):
        if self.fill_color == GREEN:
            self.fill_color = WHITE
            return True
        else:
            return False
    def set_empty_W(self):
        if self.fill_color == WHITE:
            self.fill_color = BLUE
            return True
        else:
            return False
    def set_open(self):
        self.type = 1
        self.border_color = GREEN
        self.fill_color = GREEN

    def set_close(self):
        self.border_color = LIGHTGREEN
        self.fill_color = LIGHTGREEN

    def set_g(self, g):
        self.g = g
        self.f = self.g + self.h

    def set_h(self, h):
        self.h = h
        self.f = self.g + self.h

    def set_father(self, father, direction):
        self.father = father
        if direction != -1:
            self.father_direction = direction
