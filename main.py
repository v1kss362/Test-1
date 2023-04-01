from pygame import *
from random import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_size_x, player_size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_size_x,player_size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png",self.rect.centerx,self.rect.y, 5, 35, 35)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

#музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

tank = Player('rocket.png', 300, 400, 5, 75, 75)

win_width = 800
win_height = 500

lost = 0

font.init()
font2 = font.SysFont(None, 32)


window = display.set_mode((800, 500))
display.set_caption('Забив с забивным')
background = transform.scale(
    image.load('galaxy.jpg'),(800, 500)
)

clock = time.Clock()

monsters = sprite.Group()
bullets = sprite.Group()

for i in range(5):
    monster = Enemy('ufo.png', randint(80, win_width - 80), 0, randint(1, 4), 50, 50)
    monsters.add(monster)

game = True

finish = False

lost2 = 0

while game != False :
    if finish == False :
        window.blit(background, (0,0))
        clock.tick(45)
        tank.update()
        tank.reset()
        text_lose = font2.render('Пропущено:' +  str(lost), 1, (255,255,255))
        text_lose2 = font2.render('Убито:' + str(lost2), 1, (255, 255, 255))

        sprites_list = sprite.groupcollide(
            monsters, bullets, True, True
        )

        sprites_list2 = sprite.spritecollide(
            tank, monsters, True
        )

        for i in sprites_list:
            lost2 += 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), 0, randint(1, 4), 50, 50)
            monsters.add(monster)
        if  len(sprites_list2) != 0 or lost == 3:
            finish = True
            text_lose3 = font2.render('Вы проиграли',  1, (255, 255, 255))
            window.blit(text_lose3, (300, 200))
        if lost2 >= 10:
            text_lose3 = font2.render('Вы победили', 1, (255, 255, 255))
            window.blit(text_lose3, (300, 200))
            finish = True


        window.blit(text_lose, (30,30))
        window.blit(text_lose2, (30, 50))
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        display.update()
    for e in event.get():
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                tank.fire()

        if e.type == QUIT:
            game = False
