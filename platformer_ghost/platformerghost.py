import pygame
import math
from abc import ABC, abstractmethod

pygame.init()
window = pygame.display.set_mode((928, 512))
pygame.display.set_caption("A PLATFORMER THING")
width, height = 928, 512
font = pygame.font.SysFont(None, 24)
world_map = []
map_file = open("levels.txt", "r")
void = open("nothing", "r")
voidw = open("nothing", "w")
tile_size = 32
# change deathy
death_y = 480
# add colors
RED = (255, 0, 0)
GREY = (128, 128, 128)
ORANGE = (255, 165, 0)
GREEN = (0, 128, 0)
player_speed = 0.3
vec = pygame.math.Vector2
px, py = 0, 0
block_group = pygame.sprite.Group()
damage_group = pygame.sprite.Group()
sike_group = pygame.sprite.Group()
zombie_group = pygame.sprite.Group()
killed = 0
def write(text, color, pos):
    img = font.render(text, True, color)
    window.blit(img, pos)
class Button:
    def __init__(self, show, function, x, y, w, h, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.show = show
        self.function = function
        self.color = color

    def usage(self):
        self.function()

    def draw(self):
        if self.show():
            pygame.draw.rect(window, self.color, self.rect)


class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, d,hp=50,speed=1,typeo=1):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, tile_size, tile_size * 2)
        self.distance = d * 32
        self.x = x
        self.y = y
        self.color = (255, 255, 200)
        self.mov = 0
        self.dir = -1
        self.hp = hp
        self.speed = speed
        self.type = typeo
    def move(self):
        if self.mov < self.distance:
            self.x += self.dir / 10
            self.mov += self.speed
        else:
            self.dir *= -1
            self.mov = 0
    def checkdeath(self):
        global killed
        if self.hp <= 0:
            self.kill()
            if self.type == 2:
                killed += 1
                if killed == 4:
                    while True:
                        write("VICTORY ROYALE NUMBER ONE VICTORY ROYALE NUMBER ONE VICTORY ROYALE NUMBER ONE VICTORY ROYALE NUMBER ONE VICTORY ROYALE NUMBER ONE VICTORY ROYALE NUMBER ONE VICTORY ROYALE NUMBER ONE VICTORY ROYALE NUMBER ONE VICTORY ROYALE NUMBER ONE VICTORY ROYALE NUMBER ONE VICTORY ROYALE NUMBER ONE VICTORY ROYALE NUMBER ONE VICTORY ROYALE NUMBER ONE VICTORY ROYALE NUMBER ONE VICTORY ROYALE NUMBER ONE ", (255,255,255),(256,256))
                        pygame.display.update()
        if self.y > death_y:
            self.kill()
    def collide(self, collider):
        player_rect = pygame.Rect(collider.rectx, collider.recty, tile_size, tile_size * 2)
        if self.rect.colliderect(player_rect):
            self.attack(collider)

    def attack(self, person):
        person.hp -= 0.1

    def draw(self, surface, offset):
        pygame.draw.rect(surface, self.color, (self.x - offset.x, self.y - offset.y, tile_size, tile_size * 2))

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, tile_size, tile_size * 2)
        self.move()


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y

    def draw(self, surface, offset):
        pygame.draw.rect(surface, GREY,
                         (self.x - offset.x, self.y - offset.y, tile_size, tile_size))

    def collide(self, collider):
        block_rect = pygame.Rect(self.x, self.y, tile_size, tile_size)
        player_rect = pygame.Rect(collider.rectx, collider.recty, tile_size, tile_size * 2)

        if block_rect.colliderect(player_rect):
            # Find overlap distances
            dx_left = player_rect.right - block_rect.left  # overlap if hitting from left
            dx_right = block_rect.right - player_rect.left  # overlap if hitting from right
            dy_top = player_rect.bottom - block_rect.top  # overlap if hitting from top
            dy_bottom = block_rect.bottom - player_rect.top  # overlap if hitting from bottom

            # Pick smallest overlap (closest side)
            min_overlap = min(dx_left, dx_right, dy_top, dy_bottom)

            if min_overlap == dx_left:
                return "left"  # player is hitting from left → push them back left
            elif min_overlap == dx_right:
                return "right"  # player is hitting from right → push them back right
            elif min_overlap == dy_top:
                return "top"  # player is hitting from top → push them up
            elif min_overlap == dy_bottom:
                return "bottom"  # player is hitting from bottom → push them down
        return None


class SikeBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.color = color

    def draw(self, surface, offset):
        pygame.draw.rect(surface, self.color,
                         (self.x - offset.x, self.y - offset.y, tile_size, tile_size))


class DamageSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, color, damage):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.color = color
        self.damage = damage

    def draw(self, surface, offset):
        pygame.draw.rect(surface, self.color,
                         (self.x - offset.x, self.y - offset.y, tile_size, tile_size))

    def collision(self, collider):
        damage_rect = pygame.Rect(self.x, self.y, tile_size, tile_size)
        player_rect = pygame.Rect(collider.rectx, collider.recty, tile_size, tile_size * 2)

        if damage_rect.colliderect(player_rect):
            player.hp -= self.damage


def make_map():
    global px, py
    block_group.empty()
    damage_group.empty()
    sike_group.empty()
    zombie_group.empty()

    with open("levels.txt", "r") as f:
        for i, line in enumerate(f.read().split("\n")):
            tiles = line.split(",")
            for j, tile in enumerate(tiles):
                if tile == "w":
                    block = Block(j * tile_size, i * tile_size)
                    block_group.add(block)
                if tile == "P":
                    px = j * tile_size
                    py = i * tile_size - tile_size
                if tile == "l":
                    damagesprite = DamageSprite(j * tile_size, i * tile_size, ORANGE, 100)
                    damage_group.add(damagesprite)
                if tile == "s":
                    sike = SikeBlock(j * tile_size, i * tile_size, (144, 238, 144))
                    sike_group.add(sike)
                if tile == "z":
                    zombie = Zombie(j * tile_size, i * tile_size, 50)
                    zombie_group.add(zombie)
                if tile == "Z":
                    zombie = Zombie(j * tile_size, i * tile_size, 150, 500,2, typeo=2)
                    zombie_group.add(zombie)
                if tile == "a":
                    acid = DamageSprite(j * tile_size, i * tile_size, GREEN, 2)
                    damage_group.add(acid)
                if tile == "p":
                    sike = SikeBlock(j * tile_size, i * tile_size, (255, 192, 203))
                    sike_group.add(sike)





make_map()


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sx = x
        self.sy = y
        self.rectx = self.x
        self.recty = self.y
        self.inair = False
        self.gravity = 0.1
        self.hp = 100

    def respawn(self):
        make_map()
        self.hp = 100
        self.x = self.sx
        self.y = self.sy
        self.vel_y = 0

    def check_death(self):
        if self.y >= death_y:
            self.respawn()
        for damage in damage_group:
            damage.collision(self)
        for zombie in zombie_group:
            zombie.collide(player)
        if self.hp <= 0:
            self.respawn()

    def draw_hpbar(self):
        pygame.draw.rect(window, RED, (70, 400, 140, 20))
        pygame.draw.rect(window, (144, 238, 144), (70, 400, 40 + player.hp, 20))
        write("HP", (0, 0, 0), (70, 402))

    def draw(self, surface, offset):
        pygame.draw.rect(surface, RED,
                         (self.x - offset.x, self.y - offset.y, tile_size, tile_size * 2))

    def update(self):
        self.check_death()
        # gravity
        if self.inair:
            self.y += self.gravity

        # update rect
        self.rectx = self.x
        self.recty = self.y
        # self.draw_hpbar()
        # assume in air until proven otherwise
        self.inair = True

        for block in [b for b in block_group if abs(b.x - self.x) < 64 and abs(b.y - self.y) < 64]:
            side = block.collide(self)
            if side == "left":
                self.x = block.x - tile_size
            if side == "right":
                self.x = block.x + tile_size
            if side == "top":  # landed on block
                self.y = block.y - tile_size * 2
                self.vel_y = 0
                self.inair = False
            if side == "bottom":  # hit head
                self.y = block.y + tile_size
                self.vel_y = 0
            if side == "bottom":  # hit head
                self.y = block.y + tile_size
                self.vel_y = 0


class Fist:
    def __init__(self, player):
        self.player = player
        self.dir = 1
        self.width = tile_size
        self.height = tile_size // 2
        self.attacking = False
        self.attack_timer = 0
        self.attack_duration = 15  # frames fist stays extended
        self.update_position()

    def update_position(self):
        # only snap to player if not currently attacking
        if not self.attacking:
            if self.dir == 1:  # facing right
                self.x = self.player.x + 2 * tile_size
            else:  # facing left
                self.x = self.player.x - self.width - tile_size
            self.y = self.player.y + tile_size // 2
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def attack(self):
        if not self.attacking:  # only start a new punch if not already punching
            self.attacking = True
            self.attack_timer = self.attack_duration
            # extend fist forward
            if self.dir == 1:
                self.x = self.player.x + 4 * tile_size
            else:
                self.x = self.player.x - self.width - 3 * tile_size
            self.y = self.player.y + tile_size // 2
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

            # check for hits
            for zombie in zombie_group:
                if self.rect.colliderect(zombie.rect):
                    zombie.hp -= 10
                    if self.dir == 1:
                        zombie.x += 50
                    else:
                        zombie.x -= 50

    def update(self):
        if self.attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.attacking = False  # snap back to following player
        self.update_position()

    def draw(self, surface, offset):
        pygame.draw.rect(surface, RED,
            (self.x - offset.x, self.y - offset.y, self.width, self.height))

    def flip(self, direction):
        self.dir = direction


class Camera:
    def __init__(self, player):
        self.player = player
        self.offset = vec(0, 0)
        self.offset_float = vec(0, 0)
        self.DISPLAY_W, self.DISPLAY_H = width, height
        self.CONST = vec(-self.DISPLAY_W // 2, -self.DISPLAY_H // 2)

    def setmethod(self, method):
        self.method = method

    def scroll(self):
        self.method.scroll()


class CamScroll(ABC):
    def __init__(self, camera, player):
        self.camera = camera
        self.player = player

    @abstractmethod
    def scroll(self):
        pass


class Follow(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

    def scroll(self):
        player_rect = pygame.Rect(self.player.x, self.player.y, tile_size, tile_size * 2)
        self.camera.offset_float.x = player_rect.centerx + self.camera.CONST.x
        self.camera.offset_float.y = player_rect.centery + self.camera.CONST.y
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)


player = Player(px, py)
fist = Fist(player)
camera = Camera(player)
follow = Follow(camera, player)
camera.setmethod(follow)
running = True
coins = 0
clock = pygame.time.Clock()
while running:
    keys = pygame.key.get_pressed()
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:
        fist.attack()
    if keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]:
        if not player.inair:
            player.y -= tile_size * 2

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player.x -= player_speed
        fist.flip(-1)
    if keys[pygame.K_y]:
        for zombie in zombie_group:
            zombie.hp = 0
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player.x += player_speed
        fist.flip(1)

    if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
        if not player.inair:
            player.y -= player_speed * 2
            player.inair = True

    # update camera
    camera.scroll()
    # clock.tick(60)
    window.fill((173, 216, 230))
    player.update()
    # draw world with camera offset
    player.draw(window, camera.offset)
    for block in block_group:
        block.draw(window, camera.offset)
    for damage_thing in damage_group:
        damage_thing.draw(window, camera.offset)
    for sike in sike_group:
        sike.draw(window, camera.offset)
    for zombie in zombie_group:
        zombie.update()
        zombie.checkdeath()
        zombie.draw(window, camera.offset)
    fist.update()
    fist.draw(window, camera.offset)

    player.draw_hpbar()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
    pygame.display.update()
voidw.close()
void.close()
map_file.close()