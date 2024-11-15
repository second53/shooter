
from pygame import *
from random import randint

win_x = 700
win_y = 500
windows = display.set_mode((win_x, win_y))

display.set_caption("Шутер")

bg = transform.scale(image.load("galaxy.jpg"), (win_x, win_y))

clock = time.Clock()
FPS = 60
game = True
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
mixer.music.set_volume(0.1)


fire = mixer.Sound("hook.ogg")
hit = mixer.Sound("hit.ogg")
fire.set_volume(0.1)
hit.set_volume(0.1)


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size):
        super().__init__()
        self.size = size
        self.image = transform.scale(image.load(player_image), size)
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        windows.blit(self.image, (self.rect.x, self.rect.y))

    
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_x - self.size[0]:
            self.rect.x  += self.speed

    def fire(self):
        bullet = Bullet("huck.png", self.rect.centerx, self.rect.top, 15, (125, 125))
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = randint(-200, -80)
            self.rect.x = randint(10, 590)
            self.speed = randint(1, 4)
            lost += 1
            
            
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


font.init()
font1 = font.SysFont("Arial", 36)
lost = 0
gold = 0
win = 0
text_lose = font1.render("Пропущено: " + str(lost), True, (255, 255, 255))
text_win = font1.render("Сбито: " + str(win), True, (255, 255, 255))

text_winner = font1.render("Вы выйграли! " + str(lost), True, (255, 255, 255))
text_restart = font1.render("Нажмите пробел для перезапуска ", True, (255, 255, 255))
text_gold = font1.render("Собрано монет: " + str(gold), True, (255, 255, 255))

asteroids = sprite.Group()
for i in range(3):
    ast = Enemy("asteroid.png", randint(10, 590), randint(-200, -80), 1, (100, 65))
    asteroids.add(ast)
bullets = sprite.Group()
monsters = sprite.Group()
standart = 'gg.png'
player = Player(standart, 320, 365, 10, (150, 150))
for i in range(5):
    enemy1 = Enemy("enemy.png", randint(10, 590), randint(-200, -80), randint(2, 3), (65, 100))
    monsters.add(enemy1)



finish = False
while game:
    windows.blit(bg, (0, 0))
    clock.tick(FPS)
    if finish == False:
        asteroids.update()
        asteroids.draw(windows)
        player.reset()
        player.update()
        monsters.draw(windows)
        monsters.update()
        bullets.draw(windows)
        bullets.update()

        windows.blit(text_lose, (7, 7))
        windows.blit(text_win, (7, 32))
        windows.blit(text_gold, (7, 57))
        text_gold = font1.render("Собрано монет: " + str(gold), True, (255, 255, 255))

        text_lose = font1.render("Пропущено: " + str(lost), True, (255, 255, 255))
        text_win = font1.render("Сбито: " + str(win), True, (255, 255, 255))

        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        
        if sprites_list:
            win += 1
            enemy1 = Enemy("enemy.png", randint(10, 590), randint(-200, -80), randint(2, 3), (65, 100))
            monsters.add(enemy1)
            hit.play()

        sprites_list2 = sprite.spritecollide(player, monsters, False)
        sprites_list3 = sprite.spritecollide(player, asteroids, True)

        if sprites_list2:
            finish = True
            text_winner = font1.render("Вы проиграли! ", True, (255, 255, 255))
            

        if sprites_list3:
            gold += 1
            
            ast = Enemy("asteroid.png", randint(10, 590), randint(-200, -80), 1, (100, 65))
            asteroids.add(ast)

        if win >= 100:
            finish = True
            text_winner = font1.render("Вы выйграли! ", True, (255, 255, 255))

        if lost >= 10:
            finish = True
            text_winner = font1.render("Вы проиграли! ", True, (255, 255, 255))

        if gold == 10:
            player.image = transform.scale(image.load("gg2.png"), player.size)

            
            
           
            
    
    if finish == True:
        windows.blit(text_winner, (250, 220))
        windows.blit(text_restart, (120, 280))







    for e in event.get():
        if e.type == QUIT:
            game = False
            
        if e.type == KEYDOWN:
            if e.key == K_SPACE and finish == False:
                player.fire()
                fire.play()
            if e.key == K_SPACE and finish == True:
                finish = False
                bullets = sprite.Group()
                monsters = sprite.Group()
                asteroids = sprite.Group()
                lost = 0
                gold = 0
                win = 0
                player = Player("gg.png", 320, 365, 10, (150, 150))
                player.rect.x = 320
                for i in range(5):
                    enemy1 = Enemy("enemy.png", randint(10, 590), randint(-200, -80), randint(2, 3), (65, 100))
                    monsters.add(enemy1)
                for i in range(3):
                    ast = Enemy("asteroid.png", randint(10, 590), randint(-200, -80), 1, (100, 65))
                    asteroids.add(ast)

    display.update()