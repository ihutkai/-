import pygame

pygame.init()

screen_title = 'pygame window'
screen_width = 700
screen_height = 500
screen_color = (250, 200, 200)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(screen_title)

fps = 60
clock = pygame.time.Clock()

class Hitbox():
    
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw_hitbox(self):
        pygame.draw.rect(screen, self.color, self.rect, 2)

class Platform(Hitbox):
    def __init__(self, x, y, width, height, color, speed, player_id):
        Hitbox.__init__(self, x, y, width, height, color)
        self.speed = speed
        self.player_id = player_id
        self.dx = 0
        self.dy = 0

    def draw_platform(self):
        self.draw_hitbox()

    def move(self):
        self.rect.x += self.speed * self.dx
        self.rect.y += self.speed * self.dy 

    def controller(self):
        keys = pygame.key.get_pressed()

        if self.player_id == 1:

            if keys[pygame.K_LEFT] and not  keys[pygame.K_RIGHT]:
                self.dx = -1
            elif  keys[pygame.K_RIGHT] and not  keys[pygame.K_LEFT]:
                self.dx = 1
            else:
                self.dx = 0

        if self.player_id == 2:

            if keys[pygame.K_a] and not  keys[pygame.K_d]:
                self.dx = -1
            elif  keys[pygame.K_d] and not  keys[pygame.K_a]:
                self.dx = 1
            else:
                self.dx = 0

    def collide_screen(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_width:
            self.rect.right = screen_width

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

    def collide_ball(self, sprite):
        if self.rect.colliderect(sprite.rect):
            if self.player_id == 1 and sprite.dy < 0 and sprite.rect.top > self.rect.centery:
                sprite.rect.top = self.rect.bottom
                sprite.dy *= -1
            if self.player_id == 2 and sprite.dy > 0 and sprite.rect.bottom < self.rect.centery:
                sprite.rect.bottom = self.rect.top
                sprite.dy *= -1

class Ball(Hitbox):

    def __init__(self, x, y, width, height, color, speed):
        Hitbox.__init__(self, x, y, width, height, color)
        self.speed = speed
        self.dx = -1
        self.dy = 1

    def draw_ball(self):
        self.draw_hitbox()

    def move(self):
        self.rect.x += self.speed * self.dx
        self.rect.y += self.speed * self.dy

    def collide_screen(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.dx *= -1
        elif self.rect.right > screen_width:
            self.rect.right = screen_width
            self.dx *= -1
        #if self.rect.top < 0:
         #   self.rect.top = 0
          #  self.dy *= -1
        #elif self.rect.bottom > screen_height:
         #   self.rect.bottom = screen_height
          #  self.dy *= -1

platform1 = Platform(1, 0, 150, 50, (255, 255, 255), 10, 1)
platform2 = Platform(1, 448, 150, 50, (255, 255, 255), 10, 2)
ball = Ball(0, 0, 50, 50, (30, 30, 30), 5)

font_family = None
font_size = 32
main_font = pygame.font.SysFont(font_family, font_size)

font_size2 = 50
main_font2 = pygame.font.SysFont(font_family, font_size2)

win1 = False
lose1 = False

win2 = False
lose2 = False

points1 = 0
points2 = 0

is_on = True
while is_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_on = False

    if not win1 and not lose1 and not win2 and not lose2:

        screen.fill(screen_color)
        platform1.draw_platform()
        platform1.move()
        platform1.controller()
        platform1.collide_screen()
        platform1.collide_ball(ball)
        platform2.draw_platform()
        platform2.move()
        platform2.controller()
        platform2.collide_screen()
        platform2.collide_ball(ball)
        ball.draw_ball()
        ball.move()
        ball.collide_screen()

        if ball.rect.bottom < 0:
            points1 += 1
            ball.rect.center = (screen_width // 2, screen_height // 2)
            ball.dy *= -1
        elif ball.rect.top > screen_height:
            points2 += 1
            ball.rect.center = (screen_width // 2, screen_height // 2)
            ball.dy *= -1

        points_info1 = main_font.render('Счет 1: ' + str(points1), True, (255, 255, 255))
        screen.blit(points_info1, (20, 20))
        points_info2 = main_font.render('Счет 2: ' + str(points2), True, (255, 255, 255))
        screen.blit(points_info2, (20, 40))

        if points1 >= 3:
            win1 = True
            lose2 = True

        if points2 >= 3:
            win2 = True
            lose1 = True

    elif win1 == True:
        win_info = main_font2.render('ПОБЕДА ПЕРВОГО', True, (0, 255, 0))
        screen.blit(win_info, (200, 210))

    elif win2 == True:
        win_info = main_font2.render('ПОБЕДА ВТОРОГО', True, (0, 255, 0))
        screen.blit(win_info, (200, 210))

    pygame.display.update()
    clock.tick(fps)