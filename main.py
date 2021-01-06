import pygame
import sys
from pygame import locals
from screen import Screen
from search import A_star
from block import GREEN, WHITE, BLACK
import time
import argparse

parser = argparse.ArgumentParser(description="인자 받기")

parser.add_argument('--rows', required=False, default=30, help='행,열 갯수')  # ex) python main.py --rows=60
parser.add_argument('--inc_obstacle_ratio', required=False, default=0.2, help='장애물 비율 설정')
args = parser.parse_args()

WIDTH_NUM = int(args.rows)
BLOCK_SIZE = int(600 // WIDTH_NUM)
inc_obstacle_ratio = args.inc_obstacle_ratio

class Checkbox:
    def __init__(self, surface, x, y, color=(230, 230, 230), caption="", outline_color=(0, 0, 0),
                 check_color=(0, 0, 0), font_size=22, font_color=(0, 0, 0), text_offset=(28, 1)):
        self.surface = surface
        self.x = x
        self.y = y
        self.color = color
        self.caption = caption
        self.oc = outline_color
        self.cc = check_color
        self.fs = font_size
        self.fc = font_color
        self.to = text_offset
        self.checkbox_obj = pygame.Rect(self.x, self.y, 12, 12)
        self.checkbox_outline = self.checkbox_obj.copy()
        self.checked = False
        self.active = False
        self.unchecked = True
        self.click = False

    def _draw_button_text(self):
        self.font = pygame.font.Font(None, self.fs)
        self.font_surf = self.font.render(self.caption, True, self.fc)
        w, h = self.font.size(self.caption)
        self.font_pos = (self.x + 12 / 2 - w / 2 + self.to[0], self.y + 12 / 2 - h / 2 + self.to[1])
        self.surface.blit(self.font_surf, self.font_pos)

    def render_checkbox(self):
        if self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
            pygame.draw.circle(self.surface, self.cc, (self.x + 6, self.y + 6), 4)

        elif self.unchecked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
        self._draw_button_text()

    def _update(self, event_object):
        x, y = event_object.pos
        # self.x, self.y, 12, 12
        px, py, w, h = self.checkbox_obj  # getting check box dimensions
        if px < x < px + w and px < x < px + w:
            self.active = True
        else:
            self.active = False

    def _mouse_up(self):
            if self.active and not self.checked and self.click:
                    self.checked = True
            elif self.checked:
                self.checked = False
                self.unchecked = True

            if self.click is True and self.active is False:
                if self.checked:
                    self.checked = True
                if self.unchecked:
                    self.unchecked = True
                self.active = False

    def update_checkbox(self, event_object):
        if event_object.type == pygame.MOUSEBUTTONDOWN:
            self.click = True
            # self._mouse_down()
        if event_object.type == pygame.MOUSEBUTTONUP:
            self._mouse_up()
        if event_object.type == pygame.MOUSEMOTION:
            self._update(event_object)

    def is_checked(self):
        if self.checked is True:
            return True
        else:
            return False

    def is_unchecked(self):
        if self.checked is False:
            return True
        else:
            return False


def main():
    pygame.init()
    screen = Screen(WIDTH_NUM, BLOCK_SIZE, inc_obstacle_ratio)

    step = 1
    exit = False
    tem1 = ""

    pygame.display.set_caption('A* Algorithm')
    cccccc = 0
    screen.set_start(BLOCK_SIZE * 2, BLOCK_SIZE * WIDTH_NUM - BLOCK_SIZE * 3)
    screen.set_end(BLOCK_SIZE * WIDTH_NUM - BLOCK_SIZE * 3, BLOCK_SIZE * 2)

    font = pygame.font.Font('freesansbold.ttf', 20)
    font2 = pygame.font.Font('freesansbold.ttf', 30)
    text = font.render('  Start A* Search  ', True, WHITE, BLACK)
    textRect = text.get_rect()
    textRect.center = (100, 620)
    text2 = font.render('  Random walls  ', True, WHITE, BLACK)
    textRect2 = text2.get_rect()
    textRect2.center = (300, 620)
    text3 = font.render('  Reset  ', True, WHITE, BLACK)
    textRect3 = text3.get_rect()
    textRect3.center = (500, 620)
    text4 = font2.render('Heuristic', True, BLACK, WHITE)
    textRect4 = text4.get_rect()
    textRect4.center = (690, 40)
    text5 = font.render('Manhattan', True, BLACK, WHITE)
    textRect5 = text5.get_rect()
    textRect5.center = (700, 75)
    text6 = font.render('Euclidean', True, BLACK, WHITE)
    textRect6 = text6.get_rect()
    textRect6.center = (700, 110)
    chkbox = Checkbox(screen.screen, 630, 70)
    chkbox2 = Checkbox(screen.screen, 630, 105)

    check = 0
    chkbox.checked = True
    cccccc=0
    while True:
        chkbox.render_checkbox()
        chkbox2.render_checkbox()
        screen.screen.blit(text, textRect)
        screen.screen.blit(text2, textRect2)
        screen.screen.blit(text3, textRect3)
        screen.screen.blit(text4, textRect4)
        screen.screen.blit(text5, textRect5)
        screen.screen.blit(text6, textRect6)

        for event in pygame.event.get():
            if cccccc == 15:
                exit = True
                break

            if event.type == pygame.MOUSEBUTTONUP and step == 5:  # 마우스가떼어질때
                click_x, click_y = pygame.mouse.get_pos()
                if tem1 == 11:
                    screen.set_end(click_x, click_y)
                elif tem1 == 22:
                    screen.set_start(click_x, click_y)
                tem1 = 0
                step = 1

            if event.type == pygame.MOUSEBUTTONDOWN and step == 1:  # start, end 버튼 누르고 옮길때
                click_x, click_y = pygame.mouse.get_pos()

                if click_x >= 627 and click_x <= 752:  # 휴리스틱 설정부분
                    if click_y >= 66 and click_y <= 81:
                        chkbox.checked = not chkbox.checked
                        if chkbox2.checked == chkbox.checked:
                            chkbox2.checked = not chkbox2.checked

                        if chkbox.checked:
                            check = 0
                        else:
                            check = 1

                    elif click_y >= 101 and click_y <= 118:
                        chkbox2.checked = not chkbox2.checked
                        if chkbox.checked == chkbox2.checked:
                            chkbox.checked = not chkbox.checked

                        if chkbox.checked:
                            check = 0
                        else:
                            check = 1
                if click_y >= 608 and click_y <= 630:  # 버튼들 설정부분
                    if click_x >= 14 and click_x <= 186:
                        cccccc = 15
                    elif click_x >= 218 and click_x <= 380:
                        screen.set_randomblock()
                    elif click_x >= 459 and click_x <= 538:
                        screen.screen.fill(WHITE)
                        screen.set_block_reset()

                step = 5
                tem1 = screen.set_empty(click_x, click_y)
                if tem1 == 11 or tem1 == 22 or tem1 == 33:
                    continue


            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_x, click_y = pygame.mouse.get_pos()
                screen.set_obstacle(click_x, click_y)

            elif event.type == pygame.MOUSEBUTTONDOWN and step == 3:
                click_x, click_y = pygame.mouse.get_pos()
                exit = screen.set_end(click_x, click_y)
                # exit = True
            elif event.type == locals.KEYUP and event.key == locals.K_SPACE and step == 2:
                step = 3
                pygame.display.set_caption(
                    'click block to set finishing block')
            elif event.type == locals.QUIT or (event.type == locals.KEYUP and event.key == locals.K_ESCAPE):
                pygame.quit()
                sys.exit()

        screen.draw()
        pygame.display.flip()
        if exit:
            break
    search = A_star(screen, WIDTH_NUM)
    search.set_distance(check)
    while True:
        if not search.over:
            if search.step():
                time.sleep(6)
                break
        else:
            time.sleep(6)
            break
            pygame.quit()

            sys.exit()
        screen.draw()
        screen.drawline()
        pygame.display.flip()


if __name__ == '__main__':
    main()
