import pygame
from block import Block
from block import WHITE
import random

class Screen():

    def __init__(self, width, block, inc_obstacle_ratio):
        self.screen = pygame.display.set_mode((600 + 200, 600 + 50))
        self.screen.fill(WHITE)
        self.blocks = []
        self.width = width
        self.block = block
        self.inc_obstacle_ratio = inc_obstacle_ratio
        for j in range(self.width):
            for i in range(self.width):
                self.blocks.append(Block(self.screen, i, j, self.block))
        self.start_block_index = None
        self.end_block_index = None
        self.obstacle_blocks_index = []

    def draw(self):
        for block in self.blocks:
            block.draw()

    def drawline(self):
        k = []
        list = []
        tem_ = 0
        for block in self.blocks:
            k.append(block.direc())
        list.append(self.end_block_index)

        if k[self.end_block_index] == 0:
            tem_ = self.end_block_index + self.width + 1
        elif k[self.end_block_index] == 1:
            tem_ = self.end_block_index + self.width
        elif k[self.end_block_index] == 2:
            tem_ = self.end_block_index + self.width - 1
        elif k[self.end_block_index] == 3:
            tem_ = self.end_block_index + 1
        elif k[self.end_block_index] == 4:
            tem_ = self.end_block_index - 1
        elif k[self.end_block_index] == 5:
            tem_ = self.end_block_index - self.width + 1
        elif k[self.end_block_index] == 6:
            tem_ = self.end_block_index - self.width
        elif k[self.end_block_index] == 7:
            tem_ = self.end_block_index - self.width - 1

        list.append(tem_)
        while True:
            if k[tem_] == 0:
                tem_ = tem_ + self.width + 1
            elif k[tem_] == 1:
                tem_ = tem_ + self.width
            elif k[tem_] == 2:
                tem_ = tem_ + self.width - 1
            elif k[tem_] == 3:
                tem_ = tem_ + 1
            elif k[tem_] == 4:
                tem_ = tem_ - 1
            elif k[tem_] == 5:
                tem_ = tem_ - self.width + 1
            elif k[tem_] == 6:
                tem_ = tem_ - self.width
            elif k[tem_] == 7:
                tem_ = tem_ - self.width - 1
            else:
                break
            list.append(tem_)

        i=0
        for block in self.blocks:
            if i in list:
                block.draw_line()
            i= i+1


    def get_click_block_index(self, click_x, click_y):
        x = click_x // self.block
        y = click_y // self.block

        select_block = y * self.width + x
        return select_block

    def set_start(self, click_x, click_y):
        if(click_x < 600 and click_y < 600):
            block_index = self.get_click_block_index(click_x, click_y)
            self.blocks[block_index].set_start()
            self.start_block_index = block_index
            return True
        else:
            return False

    def set_obstacle(self, click_x, click_y):
        if (click_x < 600 and click_y < 600):
            block_index = self.get_click_block_index(click_x, click_y)

            if self.blocks[block_index].set_obstacle():
                self.obstacle_blocks_index.append(block_index)

    def set_end(self, click_x, click_y):
        if (click_x < 600 and click_y < 600):
            block_index = self.get_click_block_index(click_x, click_y)
            if self.blocks[block_index].set_end():
                self.end_block_index = block_index
                return True
            else:
                return False
    def set_empty(self, click_x, click_y):
        if (click_x < 600 and click_y < 600):
            block_index = self.get_click_block_index(click_x, click_y)
            if self.blocks[block_index].set_empty_R():
                self.end_block_index = None
                return 11
            elif self.blocks[block_index].set_empty_G():
                self.start_block_index = None
                return 22
            elif self.blocks[block_index].set_empty_W():
                self.obstacle_blocks_index.append(block_index)
                return 33

    def set_randomblock(self):
        list = [i for i in range(self.width*self.width)]
        sampleList = random.sample(list, int(self.width*self.width*self.inc_obstacle_ratio))

        for block_index in sampleList:
            if self.blocks[block_index].set_obstacle():
                self.obstacle_blocks_index.append(block_index)

    def set_block_reset(self):
        list = [i for i in range(self.width*self.width)]
        for block_index in list:
            if self.blocks[block_index].set_empty_all():
                self.obstacle_blocks_index.remove(block_index)