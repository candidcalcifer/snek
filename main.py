import random
import pygame
import tkinter as tk
from tkinter import messagebox


class point(object):
    rows = 20
    w = 500

    def __init__(self, start, x=1, y=0, color=(115, 215, 255)):
        self.pos = start
        self.x = 1
        self.y = 0
        self.color = color

    def move(self, x, y):
        self.x = x
        self.y = y
        self.pos = (self.pos[0] + self.x, self.pos[1] + self.y)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color,
                         (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            mid = (i * dis + centre - radius, j * dis + 8)
            mid2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), mid, radius)
            pygame.draw.circle(surface, (0, 0, 0), mid2, radius)


class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = point(pos)
        self.body.append(self.head)

        self.x = 0
        self.y = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()

            for key in keys:  # Loop through all the keys
                if keys[pygame.K_LEFT]:
                    self.x = -1
                    self.y = 0
                    self.turns[self.head.pos[:]] = [self.x, self.y]

                elif keys[pygame.K_RIGHT]:
                    self.x = 1
                    self.y = 0
                    self.turns[self.head.pos[:]] = [self.x, self.y]

                elif keys[pygame.K_UP]:
                    self.x = 0
                    self.y = -1
                    self.turns[self.head.pos[:]] = [self.x, self.y]

                elif keys[pygame.K_DOWN]:
                    self.x = 0
                    self.y = 1
                    self.turns[self.head.pos[:]] = [self.x, self.y]

        for i, c in enumerate(self.body):
            p = c.pos[:]

            if p in self.turns:
                turn = self.turns[p]  # Get the direction we should turn
                c.move(turn[0], turn[1])  # Move our cube in that direction
                if i == len(
                        self.body) - 1:  # If this is the last cube in our body remove the turn from the dict
                    self.turns.pop(p)

            else:
                if c.x == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.x == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.y == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.y == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.x, c.y)

    def reset(self, pos):
        self.head = point(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.x = 0
        self.y = 1

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.x, tail.y

        if dx == 1 and dy == 0:
            self.body.append(point((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(point((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(point((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(point((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].x = dx
        self.body[-1].y = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def draw_grid(w, r, surface):
    size = w // r

    x = 0
    y = 0
    for i in range(r):
        x = x + size
        y = y + size
        pygame.draw.line(surface, (123, 123, 123), (x, 0), (x, w))
        pygame.draw.line(surface, (123, 123, 123), (0, y), (w, y))


def redraw_window(surface):
    global rows, width, s, snack
    surface.fill((250, 250, 250))
    s.draw(surface)
    snack.draw(surface)
    draw_grid(width, rows, surface)
    pygame.display.update()


def random_snack(r, item):
    positions = item.body

    while True:
        x = random.randrange(r)
        y = random.randrange(r)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return x, y


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    root.destroy()


if __name__ == '__main__':
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((115, 215, 255), (10, 10))
    snack = point(random_snack(rows, s), color=(0, 0, 0))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            s.add_cube()
            snack = point(random_snack(rows, s), color=(0, 0, 0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                print('Score: ', len(s.body))
                message_box('You Lost!', 'Play again...')
                s.reset((10, 10))
                break

        redraw_window(win)
