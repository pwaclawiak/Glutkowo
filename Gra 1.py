import pygame
from copy import copy
import math

FPS=60
SZEROKOSC=1536
WYSOKOSC=1024
SZEROKOSC_GRACZA=90
WYSOKOSC_GRACZA=150

pygame.init()
screen=pygame.display.set_mode((SZEROKOSC,WYSOKOSC))

background=pygame.image.load("glutkowo_background.png")
ludek = pygame.image.load("gracz.png")
ludek.set_colorkey("#ffffff")

pilka = pygame.image.load("Piłka.png")
pilka.set_colorkey("#ffffff")
pilka = pygame.transform.scale(pilka, (SZEROKOSC_GRACZA/3, SZEROKOSC_GRACZA/3))

wyrzutnia = pygame.image.load("Wyrzurtnia.png")
wyrzutnia.set_colorkey("#ffffff")
wyrzutnia = pygame.transform.scale(wyrzutnia, (SZEROKOSC_GRACZA, SZEROKOSC_GRACZA))


class Gracz:
    sprite_left = pygame.transform.scale(ludek, (SZEROKOSC_GRACZA, WYSOKOSC_GRACZA))
    sprite_right = pygame.transform.flip(sprite_left, True, False)
    
    def __init__(self, hp):
        self.pos_x = SZEROKOSC/4
        self.pos_y = WYSOKOSC/10*7
        self.sprite = Gracz.sprite_right
        self.kierunek = "right"
        self.hp = hp
    
    def draw(self, screen:pygame.Surface):
        screen.blit(self.sprite, (self.pos_x, self.pos_y))
    
    def move_right(self):
        self.sprite = Gracz.sprite_right
        if self.pos_x > SZEROKOSC-SZEROKOSC_GRACZA:
            self.pos_x = SZEROKOSC-SZEROKOSC_GRACZA
        else:
            self.pos_x += 5
        self.kierunek = "right"
    def move_left(self):
        self.kierunek = "left"
        self.sprite = Gracz.sprite_left
        if self.pos_x < 0:
            self.pos_x = 0 
        else:
            self.pos_x -= 5
    
    def skakanie(self):
        if self.pos_y > 0:
            self.pos_y -= 10
        if self.pos_y < 0:
            self.pos_y = pos_ziemia
    
    def spadanie(self):
        if self.pos_y<pos_ziemia:
            self.pos_y+=7
        else: 
            self.pos_y=pos_ziemia

class Pocisk:
    sprite = pilka
    half_sprite_size = pygame.math.Vector2(sprite.get_width()//2, sprite.get_height()//2)
    
    def __init__(self, pos, zadawane_hp, pozycja_myszki):
        self.pos = pos - Pocisk.half_sprite_size
        pomocniczy_vektor = pygame.math.Vector2(pozycja_myszki) - self.half_sprite_size
        self.kierunek = pomocniczy_vektor - self.pos
        self.hp = zadawane_hp
        self.speed = 10

    def draw(self, screen:pygame.Surface):
        screen.blit(Pocisk.sprite, self.pos)
    def lot_pocisku(self):
        self.pos = self.pos + self.kierunek/30

class Bazooka:
    sprite_left = wyrzutnia
    sprite_right=pygame.transform.flip(sprite_left, True, False)
    rotation_point_offset = pygame.math.Vector2(0, sprite_left.get_height()//4)
    wektor_lufy = pygame.math.Vector2(-sprite_left.get_width()//2, -sprite_left.get_height()//4)
    
    def __init__(self, player_x, player_y):
        self.pos = pygame.math.Vector2(player_x + SZEROKOSC_GRACZA*2/6, player_y + WYSOKOSC_GRACZA*4/6)
        self.sprite = Bazooka.sprite_right
        self.rotation_offset = Bazooka.rotation_point_offset
        self.sprite_version = "right"
        self.current_angle = 0
        self.pozycja_lufy = pygame.math.Vector2(0, 0)
    
    def aktualizacja_współrzędnych(self, player_x, player_y, player_head_dir):
        if player_head_dir == "left":
            self.sprite_version = "left"
            self.sprite = Bazooka.sprite_left
            self.pos.x = player_x + SZEROKOSC_GRACZA*4/6
        else:
            self.sprite_version = "right"
            self.sprite = Bazooka.sprite_right
            self.pos.x = player_x + SZEROKOSC_GRACZA*2/6
        self.pos.y = player_y + WYSOKOSC_GRACZA*4/6
    
    def oś_obrotu(self, screen:pygame.Surface):
        center = self.pos
        pygame.draw.circle(screen, "red", center, 4)
        pygame.draw.circle(screen, "blue", self.pozycja_lufy, 5)
    
    def draw(self, screen:pygame.Surface):
        sprite_rect = self.sprite.get_rect(center=self.pos - self.rotation_offset)
        screen.blit(self.sprite, sprite_rect.topleft)
        self.oś_obrotu(screen)
    
    def rotate (self, pozycja_myszki):
        wektor_myszy = pygame.math.Vector2(pozycja_myszki)
        odleglosc = wektor_myszy - self.pos

        wektor_lufy = copy(Bazooka.wektor_lufy)
        if self.sprite_version == "left":
            wektor_lufy.y = -wektor_lufy.y
        
        kat_myszki = odleglosc.angle_to(-wektor_lufy) - 80

        self.pozycja_lufy = self.pos + wektor_lufy.rotate(-self.current_angle + 90)

        # kat_myszki = math.degrees(math.atan2(-odleglosc.y, odleglosc.x))
        if self.sprite_version == "left":
            self.current_angle = kat_myszki - 20
        else:
            self.current_angle = kat_myszki

        self.rotation_offset = Bazooka.rotation_point_offset.rotate(-self.current_angle)
        self.sprite = pygame.transform.rotate(self.sprite, self.current_angle)


pos_ziemia = WYSOKOSC/10*4

gracz = Gracz(100)
bazoka = Bazooka(gracz.pos_x, gracz.pos_y)
pocisk = None
burki = []


clock=pygame.time.Clock()
run_game = True
while run_game:
    screen.fill("black")
    screen.blit(background, (0, 0))  
    
    keyboard = pygame.key.get_pressed()
    if keyboard[pygame.K_RIGHT] or keyboard[pygame.K_d]:
        gracz.move_right()

    if keyboard[pygame.K_LEFT]or keyboard[pygame.K_a]:
        gracz.move_left()
            
    if keyboard[pygame.K_SPACE] or keyboard[pygame.K_w]:
        gracz.skakanie()
    else:
        gracz.spadanie()
    
    bazoka.aktualizacja_współrzędnych(gracz.pos_x, gracz.pos_y, gracz.kierunek)
    
    pozycja_myszki = pygame.mouse.get_pos()  
    bazoka.rotate(pozycja_myszki)
    
    event_list = pygame.event.get()
    for event in event_list:
        if event.type==pygame.QUIT:
            run_game=False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click_pos = pygame.mouse.get_pos()
                pocisk = Pocisk(bazoka.pozycja_lufy, 10, click_pos)
    
    
    gracz.draw(screen)
    bazoka.draw(screen)
    
    if isinstance(pocisk, Pocisk):
        pocisk.lot_pocisku()
        pocisk.draw(screen)
    
    pygame.display.update()
    clock.tick(FPS)





pygame.quit()
