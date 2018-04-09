import pygame
import random
import math

SCREEN_DIM = (800, 600)

class Vec2d:

    def __init__(self, x ,y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Vec2d: ({},{})".format(self.x,self.y)

    def int_pair(self):
        return (int(self.x), int(self.y))

    def float_pair(self):
        return (float(self.x), float(self.y))


    def __sub__(self, other):
        return Vec2d(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Vec2d(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return Vec2d(self.x * other, self.y * other)

    def __len__(self):
        return 2

    def length(x):
        return math.sqrt(x[0] * x[0] + x[1] * x[1])

    def vec(x, y):
        return Vec2d.sub(y, x)


def choose(list):
    for i in list:
        if i.val == 1:
            return i

def draw_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "Move more FAST"])
    data.append(["Num-", "Move more SLOW"])
    data.append(["A", "Create new curve"])
    data.append(["M", "Add point to all curves"])
    data.append(["F", "Delete one knot from all curves"])
    data.append(["D", "Delete one knot from current curve"])
    data.append(["H", "Choose active next curve"])
    data.append(["J", "Choose active previos curve"])
    data.append(["Num-", "Move more SLOW"])
    data.append(["", ""])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
                      (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

class Polilyne:

    def __init__(self, ):
        self.steps = 35
        self.working = True
        self.points = []
        self.speeds = []
        self.show_help = False
        self.pause = True
        self.val = 0


    def draw_points(self, points, style="points", width=3, color=(255, 255, 255)):
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(gameDisplay, color, (points[p_n].int_pair()[0], points[p_n].int_pair()[1]), (points[p_n+1].int_pair()[0], points[p_n+1].int_pair()[1]), width)

        elif style == "points":
            for p in points:
                if self.val == 1:
                    pygame.draw.circle(gameDisplay, (255,0,0), (p.int_pair()[0], p.int_pair()[1]), width)
                else:
                    pygame.draw.circle(gameDisplay, color, (p.int_pair()[0], p.int_pair()[1]), width)

    def set_points(self, points, speeds):
        for p in range(len(points)):
            points[p] = (points[p] + speeds[p])
            if points[p].int_pair()[0] > SCREEN_DIM[0] or points[p].int_pair()[0] < 0:
                speeds[p] = Vec2d( -speeds[p].float_pair()[0], speeds[p].float_pair()[1])
            if points[p].int_pair()[1] > SCREEN_DIM[1] or points[p].int_pair()[1] < 0:
                speeds[p] = Vec2d(speeds[p].float_pair()[0], -speeds[p].float_pair()[1])

class Knot(Polilyne):

    def get_knot(self, points, count):
        if len(points) < 3:
            return []
        res = []
        for i in range(-2, len(points) - 2):
            ptn = []
            ptn.append((points[i] + points[i + 1]) * 0.5)
            ptn.append(points[i + 1])
            ptn.append((points[i + 1] + points[i + 2]) * 0.5)
            res.extend(self.get_points(ptn, count))
        return res

    def restart(self):
        self.points = []
        self.speeds = []

    def work(self):
        for k in program_list:
            self.draw_points(self.points)
            self.draw_points(self.get_knot(self.points,self.steps), "line", 3, color )


    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]

        return ((points[deg] * alpha) + (self.get_point(points, alpha, deg - 1) * (1 - alpha)))

    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def knot_append(self, points):
        self.points.append(Vec2d(points[0],points[1]))

    def knot_remove(self):
        if len(self.points) > 1 and len(self.speeds) > 1:
            del self.points[-1]
            del self.speeds[-1]
        else:
            self.points = []
            self.speeds = []

    def speeds_append(self,points):
        self.speeds.append(Vec2d(points[0],points[1]))

    def speed_up_down(self, option):
        for i in range(len(self.speeds)):
            if option == "plus":
                self.speeds[i] = Vec2d(abs(self.speeds[i].float_pair()[0]) + 1, abs(self.speeds[i].float_pair()[1]) + 1)
            elif option == "minus":
                self.speeds[i] = Vec2d(abs(self.speeds[i].float_pair()[0]) - 1, abs(self.speeds[i].float_pair()[1]) - 1)
            else:
                raise TypeError

if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")
    program_list = []
    program = Knot()
    program_list.append(program)


    program_list[0].val = 1
    hue = 0
    color = pygame.Color(0)

    while program.working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                program.working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    program.working = False
                if event.key == pygame.K_r:
                    program.restart()
                if event.key == pygame.K_d:
                    choose(program_list).knot_remove()
                if event.key == pygame.K_f:
                    for i in program_list:
                        i.knot_remove()
                if event.key == pygame.K_m:
                    for i in program_list:
                        i.knot_append((random.randrange(50,700),random.randrange(50,500)))
                        i.speeds_append((random.random() * 2, random.random() * 2))
                if event.key == pygame.K_a:
                    program_list.append(Knot())
                    choose(program_list).val = 0
                    program_list[-1].val = 1
                    program_list[-1].pause = program_list[0].pause
                if event.key == pygame.K_h:
                    ind = program_list.index(choose(program_list))
                    choose(program_list).val = 0
                    program_list[ind - 1].val = 1
                if event.key == pygame.K_j:
                    ind = program_list.index(choose(program_list))
                    choose(program_list).val = 0
                    program_list[ind +1].val = 1
                if event.key == pygame.K_p:
                    for i in program_list:
                        i.pause = not i.pause
                if event.key == pygame.K_KP_PLUS:
                    for i in program_list:
                        i.speed_up_down("plus")
                if event.key == pygame.K_F1:
                    program.show_help = not program.show_help
                if event.key == pygame.K_KP_MINUS:
                    for i in program_list:
                        i.speed_up_down("minus")
            if event.type == pygame.MOUSEBUTTONDOWN:
                choose(program_list).knot_append(event.pos)
                choose(program_list).speeds_append((random.random() * 2, random.random() * 2))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)

        for i in program_list:
            i.work()

            if not i.pause:
                i.set_points(i.points,i.speeds)
            if program.show_help:
                draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)