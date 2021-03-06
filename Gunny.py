import pygame
from pygame.locals import *
import pygbutton
from common.constant import Constant
from common.utils import Utils
from sprites.ground import Ground
from sprites.explosion import Explosion
from sprites.bullet import Bullet
from sprites.MonsterBullet import MonsterBullet
from sprites.energy_bar import Energy_bar
from sprites.power_bar import Power_bar
from sprites.live_bar import Live_bar
from sprites.player import Player
from common.e_bullet_type import EBulletType
from sprites.screeps.basic_creep import BasicCreep
from sprites.screeps.creep_a import CreepA
from sprites.screeps.creep_b import CreepB
from sprites.screeps.creep_c import CreepC
from sprites.screeps.creep_d import CreepD
from sprites.screeps.creep_e import CreepE
from sprites.screeps.creep_f import CreepF
from sprites.screeps.creep_a_special import CreepASpecial
from sprites.item.coreItem import coreItem


from sprites.item.money import money
from sprites.item.magic_box import magicbox
from sprites.item.bumerange import bumerange
from sprites.item.monster import monster
from sprites.item.berry import berry

from sprites.creep_manager import CreepManager

from sprites.tile import TileCache
from sprites.tile import Tile

from sprites.creep_manager import CreepManager
from sprites.tile import SpecialObject
from sprites.tile import SpecialObject


# See if we can load more than standard BMP

if not pygame.image.get_extended():
    raise SystemExit("Sorry, extended image module required")

def start(game_state):
    # Initialize pygame
    pygame.init()
    if pygame.mixer and not pygame.mixer.get_init():
        print ('Warning, no sound')
        pygame.mixer = None

    # Set the display mode
    win_style = 0  # FULL SCREEN
    best_depth = pygame.display.mode_ok(Constant.SCREENRECT.size, win_style, 32)
    screen = pygame.display.set_mode(Constant.SCREENRECT.size, win_style, best_depth)

    pygame.display.set_caption('Gunny')
    pygame.mouse.set_visible(1)
    home(screen, game_state)


def home(screen, game_state):
    background = pygame.image.load("resources\data\home_back.png")

    play_button_obj = pygbutton.PygButton((430, 200, 100, 40), 'Play')
    how_to_play_button_obj = pygbutton.PygButton((430, 300, 100, 40), 'How to play')
    about_us_button_obj = pygbutton.PygButton((430, 400, 100, 40), 'About us')
    exit_button_obj = pygbutton.PygButton((430, 500, 100, 40),'Exit')
    while game_state == Constant.HOME:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
            if 'click' in play_button_obj.handleEvent(event):
                game_state = Constant.GAME
                if game_state == Constant.GAME:
                    main(screen)
            elif 'click' in how_to_play_button_obj.handleEvent(event):
                game_state = Constant.HOWTOPLAY
                how_to_play(screen,game_state)
            elif 'click' in about_us_button_obj.handleEvent(event):
                game_state = Constant.ABOUTUS
                about_us(screen,game_state)
            elif 'click' in exit_button_obj.handleEvent(event):
                if pygame.mixer:
                    pygame.mixer.music.fadeout(1000)
                pygame.time.wait(1000)
                pygame.quit()
        if game_state == Constant.HOME:
            screen.blit(background, (0, 0))
            play_button_obj.draw(background)
            how_to_play_button_obj.draw(background)
            about_us_button_obj.draw(background)
            exit_button_obj.draw(background)
            pygame.display.flip()

def how_to_play(screen, game_state):
    background = pygame.image.load("resources\data\HowToPlay.png")

    back_button_obj = pygbutton.PygButton((0, 600, 100, 40),'Back')
    while game_state == Constant.HOWTOPLAY:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
            if 'click' in back_button_obj.handleEvent(event):
                game_state = Constant.HOME
                home(screen, game_state)
        if game_state == Constant.HOWTOPLAY:
            screen.blit(background, (0, 0))
            Font = pygame.font.Font("resources\Fonts\GoodDog.otf", 40)
            screen.blit(Font.render('Press "A, D" to ', True, (255, 0, 0)), (30, 100))
            screen.blit(Font.render('move left or right.  ', True, (255, 0, 0)), (30, 150))
            screen.blit(Font.render('Press "W, S" to ', True, (255, 0, 0)), (30, 250))
            screen.blit(Font.render('choose angle.  ', True, (255, 0, 0)), (30, 300))
            screen.blit(Font.render('Press "J" to jump . Press "Space" to choose power.', True, (255, 0, 0)), (30, 400))
            screen.blit(Font.render('Press "TAB" to change bullet.', True, (255, 0, 0)), (30, 500))
            back_button_obj.draw(background)
            pygame.display.flip()

def about_us(screen, game_state):
    background = pygame.image.load("resources\data\AboutUs.png")

    back_button_obj = pygbutton.PygButton((0, 600, 100, 40),'Back')
    while game_state == Constant.ABOUTUS:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
            if 'click' in back_button_obj.handleEvent(event):
                game_state = Constant.HOME
                home(screen, game_state)
        if game_state == Constant.ABOUTUS:
            screen.blit(background, (0, 0))
            back_button_obj.draw(background)
            pygame.display.flip()

def game_over(screen,gamestate):
    pygame.mouse.set_visible(1)

    # #create the background, tile the bgd image
    bgdtile = Utils.load_image('gameover_back.jpg')
    background = pygame.Surface(Constant.SCREENRECT.size)
    for x in range(0, Constant.SCREENRECT.width, bgdtile.get_width()):
        background.blit(bgdtile, (x, 0))

    playagain = pygbutton.PygButton((380, 400, 100, 40), 'Play again')
    quit = pygbutton.PygButton((520, 400, 100, 40), 'Quit')

    while gamestate == Constant.GAMEOVER:
        for event in pygame.event.get():
            if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return
            if 'click' in playagain.handleEvent(event):
                gamestate = Constant.GAME
                if(gamestate == Constant.GAME):
                    CreepManager.init()
                    main(screen)
            if 'click' in quit.handleEvent(event):
                if pygame.mixer:
                    pygame.mixer.music.fadeout(1000)
                pygame.time.wait(1000)
                pygame.quit()
        screen.blit(background, (0,0))
        playagain.draw(background)
        quit.draw(background)
        pygame.display.flip()


def main(screen):
    pygame.mouse.set_visible(0)
    # Load image
    background = pygame.image.load("resources\image\TileSet\\background.png").convert()
    img = Utils.load_image('explosion1.gif')
    coins_image = pygame.image.load('resources\image\TileSet\Coins.png')
    Explosion.images = [img, pygame.transform.flip(img, 1, 1)]

    # Load font
    coin_font = pygame.font.Font("resources\Fonts\Number.ttf", 32)

    # Load the sound effects
    boom_sound = Utils.load_sound('boom.wav')
    shoot_sound = Utils.load_sound('1.wav')

    if pygame.mixer:
        music = 'resources/data/1037.wav'
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)

    # Initialize Game Groups
    aliens = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    monsterbombs = pygame.sprite.Group()
    render_group = pygame.sprite.OrderedUpdates()
    creeps = pygame.sprite.Group()
    items = pygame.sprite.Group()

    # Assign default groups to each sprite class

    # Ground.containers = all_group
    # Player.containers = all_group
    # BasicCreep.containers = all_group, creeps
    coreItem.containers = render_group

    Player.containers = render_group
    Player.screen = screen

    BasicCreep.containers = creeps, render_group
    Bullet.containers = bombs, render_group
    MonsterBullet.containers = monsterbombs,render_group
    Explosion.containers = render_group

    Live_bar.containers = render_group
    Energy_bar.containers = render_group
    Power_bar.containers = render_group

    # Create Some Starting Values
    # Global score

    clock = pygame.time.Clock()


    #ground = Ground()
    player = Player('nhan vat 1', 'character1', 1, 1, 350, screen)

    #*************************************
    # Init creeps
    #*************************************
    BasicCreep.screen = screen
    Player.screen = screen
    #*************************************
    # Init item
    #*************************************

    money_item = money(360, 200, "money")
    items.add(money_item)
    money_item = money(400, 200, "money")
    items.add(money_item)
    money_item = money(440, 200, "money")
    items.add(money_item)
    money_item = money(480, 200, "money")
    items.add(money_item)
    money_item = money(520, 200, "money")
    items.add(money_item)

    money_item = money(360, 80, "money")
    items.add(money_item)
    money_item = money(400, 80, "money")
    items.add(money_item)
    money_item = money(440, 80, "money")
    items.add(money_item)
    money_item = money(480, 80, "money")
    items.add(money_item)
    money_item = money(520, 80, "money")
    items.add(money_item)

    money_item = money(680, 40, "money")
    items.add(money_item)
    money_item = money(720, 40, "money")
    items.add(money_item)
    money_item = money(760, 40, "money")
    items.add(money_item)
    money_item = money(800, 40, "money")
    items.add(money_item)
    money_item = money(840, 40, "money")
    items.add(money_item)

    money_item = money(1600, 180, "money")
    items.add(money_item)
    money_item = money(1640, 180, "money")
    items.add(money_item)
    money_item = money(1680, 180, "money")
    items.add(money_item)
    money_item = money(1720, 180, "money")
    items.add(money_item)
    money_item = money(2592, 128, "money")
    items.add(money_item)
    money_item = money(2624, 128, "money")
    items.add(money_item)
    money_item = money(2656, 128, "money")
    items.add(money_item)
    money_item = money(2688, 128, "money")
    items.add(money_item)
    money_item = money(3744, 384, "money")
    items.add(money_item)
    money_item = money(3776, 384, "money")
    items.add(money_item)
    money_item = money(3808, 384, "money")
    items.add(money_item)
    money_item = money(3840, 384, "money")
    items.add(money_item)
    money_item = money(4736, 64, "money")
    items.add(money_item)
    money_item = money(4736, 32, "money")
    items.add(money_item)
    money_item = money(4768, 64, "money")
    items.add(money_item)
    money_item = money(4768, 32, "money")
    items.add(money_item)
    money_item = money(4800, 64, "money")
    items.add(money_item)
    money_item = money(4800, 32, "money")
    items.add(money_item)
    money_item = money(4832, 64, "money")
    items.add(money_item)
    money_item = money(4832, 32, "money")
    items.add(money_item)
    money_item = money(4864, 64, "money")
    items.add(money_item)
    money_item = money(4896, 32, "money")
    items.add(money_item)
    money_item = money(4928, 64, "money")
    items.add(money_item)
    money_item = money(4928, 32, "money")
    items.add(money_item)
    money_item = money(4960, 64, "money")
    items.add(money_item)
    money_item = money(4992, 32, "money")
    items.add(money_item)
    money_item = money(5024, 64, "money")
    items.add(money_item)
    money_item = money(5024, 32, "money")
    items.add(money_item)
    money_item = money(5056, 64, "money")
    items.add(money_item)
    money_item = money(5056, 32, "money")
    items.add(money_item)
    money_item = money(5088, 64, "money")
    items.add(money_item)
    money_item = money(5088, 32, "money")
    items.add(money_item)
    money_item = money(5120, 64, "money")
    items.add(money_item)
    money_item = money(5120, 32, "money")
    items.add(money_item)
    money_item = money(5152, 64, "money")
    items.add(money_item)
    money_item = money(5152, 32, "money")
    items.add(money_item)
    money_item = money(5184, 64, "money")
    items.add(money_item)
    money_item = money(5184, 32, "money")
    items.add(money_item)
    money_item = money(5216, 64, "money")
    items.add(money_item)
    money_item = money(5216, 32, "money")
    items.add(money_item)
    money_item = money(5248, 64, "money")
    items.add(money_item)
    money_item = money(5248, 32, "money")
    items.add(money_item)

    money_item = berry(2890, 100, "berry")
    items.add(money_item)


    money_item = money(5440, 192, "money")
    items.add(money_item)
    money_item = money(5472, 192, "money")
    items.add(money_item)
    money_item = money(5504, 192, "money")
    items.add(money_item)
    money_item = money(5472, 192, "money")
    items.add(money_item)

    money_item = money(5792, 160, "money")
    items.add(money_item)
    money_item = money(5824, 160, "money")
    items.add(money_item)
    money_item = money(5856, 160, "money")
    items.add(money_item)
    money_item = money(5888, 160, "money")
    items.add(money_item)

    money_item = money(6080, 160, "money")
    items.add(money_item)
    money_item = money(6112, 160, "money")
    items.add(money_item)
    money_item = money(6144, 160, "money")
    items.add(money_item)

    CreepManager.create_creep(creeps, 'A', 365, 332, 365, 480, 0, 1)
    CreepManager.create_creep(creeps, 'A', 611, 332, 576, 989, 0, 1)
    CreepManager.create_creep(creeps, 'A', 874, 332, 576, 989, 1, 1)
    CreepManager.create_creep(creeps, 'D', 1472+10, 316-50, 1472+10, 1588, 1, 1)
    CreepManager.create_creep(creeps, 'D', 1218+10, 380-50, 1218+10, 1374, 1, 1)

    CreepManager.create_creep(creeps, 'B', 1280+20, 508-30, 1280+20, 1374-20, 1, 1)
    CreepManager.create_creep(creeps, 'B', 1474+20, 508-30, 1474+20, 1628-50, 1, 1)
    CreepManager.create_creep(creeps, 'B', 1664+45, 508-30, 1664+45, 1782-20, 1, 1)

    CreepManager.create_creep(creeps, 'A', 2592+45, 442-48, 2592+45, 2876-20, 1, 1)
    CreepManager.create_creep(creeps, 'F', 2592+45, 100, 2592+45, 2876-20, 1, 4)

    CreepManager.create_creep(creeps, 'B', 3302+45, 442 - 30, 3302+45-20, 3548-20, 1, 2)
    CreepManager.create_creep(creeps, 'F', 3312+45, 300, 3302+45-20, 3548-20, 1, 4)
    CreepManager.create_creep(creeps, 'F', 3400, 200, 3302+45-20, 3548-20, 0, 3)
    CreepManager.create_creep(creeps, 'F', 3390, 70, 3302+45-20, 3548-20, 0, 3)

    CreepManager.create_creep(creeps, 'A', 3840+55, 442 - 15, 3840+50, 4000-20-20, 0, 1)

    CreepManager.create_creep(creeps, 'A', 4706+55, 362, 4706, 4862-20, 0, 1)

    CreepManager.create_creep(creeps, 'C', 5365, 162, 5365, 6000, 0, 4)
    CreepManager.create_creep(creeps, 'C', 5365, 62, 5365, 6000, 0, 4)

    CreepManager.create_creep(creeps, 'B', 6505, 316, 6505, 6645, 0, 4)

    CreepManager.create_creep(creeps, 'A_SPECIAL', 4917, 381, 4907, 5033, 0, 1)

    tileset = TileCache("resources/image/TileSet/ImageSheet.png", Constant.TILE_WIDTH, Constant.TILE_HEIGHT).load_tile_table()
    invisible_tiles = (((9,14), (9,15), (9, 16),(9, 17)),
                        ((6, 19), (6, 20), (6, 21), (6,22)),
                       ((12, 68), (12, 69), (12, 70), (13, 70), (14, 70)),
                       ((5, 81), (5, 82), (5, 83), (5, 84)),
                       ((7,144), (7, 145), (6, 146), (6, 147)))

    """ CREATE LIST OF SPECIAL OBJECTS """
    special_tiles = []
    for line in invisible_tiles:
        for element in line:
            special_tile = SpecialObject(tileset, element, (Constant.TILE_WIDTH * element[1], Constant.TILE_HEIGHT * element[0]))
            special_tiles.append(special_tile)

    camera_left = 0
    camera_right = Constant.SCREENRECT.width
    hCount = 1

    player.typeOfBullet = EBulletType.BASIC
    mymonster = monster(7400, 270, "monster")
    items.add(mymonster)
    player.sound_money = pygame.mixer.Sound('resources/data/yahoo.ogg')
    # Main loop
    while player.health > -10:

        # CREEP MANAGER
        CreepManager.update(creeps, player.pos[0], player.pos[1], player.rect.left)
        CreepManager.create_creep_dynamic(player.pos[0], creeps)
        if player.state == Constant.DIE_STATE:
            player.health -= 0.1

        # Get input
        player1_down_to_up = player.fire_down

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
            elif event.type == KEYDOWN:
                if event.key == Constant.PLAYER1FIREKEY:
                    player.fire_down = True
                elif event.key == Constant.PLAYER1CHANGEBULLET:
                    player.typeOfBullet += 1
                    if player.typeOfBullet >= Constant.NUM_BULLET_TYPE:
                        player.typeOfBullet = EBulletType.BASIC
                elif event.key == Constant.PLAYER1JUMPKEY:
                    if not player.downable:
                        player.jump = 20
            elif event.type == KEYUP:
                if event.key == Constant.PLAYER1FIREKEY:
                    player.fire_down = False
                    if player.enegery >= 20:
                        player.state = Constant.THROW_STATE

        # Clear/erase the last drawn sprites
        render_group.clear(screen, background)
        screen.fill((0, 0, 0))
        if (camera_right < Constant.SCREENRECT.width * 8):
            if camera_left < (hCount - 1) * background.get_width():
                hCount -= 1
            elif (camera_left < hCount * background.get_width()):
                if (camera_right > hCount * background.get_width()):
                        screen.blit(background, (0  - camera_left + (hCount - 1) * background.get_width(), 0))
                        screen.blit(background, (hCount * background.get_width() - camera_left, 0))
                else:
                        screen.blit(background, (0  - camera_left + (hCount -1) * background.get_width(), 0))
            else:
                hCount += 1

        tiles = []
        for y in range(int(camera_left) / Constant.TILE_WIDTH, (int(camera_right) / Constant.TILE_WIDTH) + 1):
            if y > 239:
                y = 239
            for x in range(0, 20):
                if Constant.MAP[x][y] is not 0:
                    tile = Tile(tileset, (x, y), (32 * y, 32 * x))
                    for line in invisible_tiles:
                        if tile.id in line:
                            tile.visible = False
                            break
                    if tile.visible:
                        screen.blit(tile.image, (Constant.TILE_WIDTH * y - camera_left, Constant.TILE_HEIGHT * x))
                    tiles.append(tile)

        # Update all the sprites
        render_group.update()
        monsterbombs.update()
        
        for item in items.sprites():
            item.update_pos(player.pos[0], player.rect.left)

        screen.blit(coins_image, (440, 0))
        screen.blit(coin_font.render(' X  ' + str(player.money), True, (0, 0, 0)), (480, 0))
        items.update()

        # Handle player input
        key_state = pygame.key.get_pressed()

        player.check(key_state)

        if player1_down_to_up and not player.fire_down and player.enegery >= 25:
            if player.typeOfBullet == EBulletType.BASIC:
                butllet = Bullet(player.angle, player.power, player, "fireball.png")
                shoot_sound.play()
                player.enegery -= butllet.energy_cost
            else:
                butllet = Bullet(player.angle, player.power, player, "simple.png")
                butllet = Bullet(player.angle+10, player.power, player, "simple.png")
                butllet = Bullet(player.angle-10, player.power, player, "simple.png")
                shoot_sound.play()
                player.enegery -= butllet.energy_cost

        # *************************************************************
        # CHECK COLLISION HERE!
        # *************************************************************
        for b in bombs.sprites():
            b.update_pos(player.pos[0], player.rect.x)



        """ COLLIDE WITH SPECIAL OBJECT"""
        for tile in tiles:
            if tile.id ==  (11, 21) and Utils.check_collision(player, tile):
                for special_tile in special_tiles:
                    if special_tile.id in invisible_tiles[0]:
                        special_tile.visible = True
            if tile.id == (11, 27) and Utils.check_collision(player, tile):
                for special_tile in special_tiles:
                    if special_tile.id in invisible_tiles[1]:
                        special_tile.visible = True
            if tile.id == (14, 58) and Utils.check_collision(player, tile):
                for special_tile in special_tiles:
                    if special_tile.id in invisible_tiles[2]:
                        special_tile.visible = True
            if tile.id == (6, 77) and Utils.check_collision(player, tile):
                for special_tile in special_tiles:
                    if special_tile.id in invisible_tiles[3]:
                        special_tile.visible = True
            if tile.id == (9, 143) and Utils.check_collision(player, tile):
                for special_tile in special_tiles:
                    if special_tile.id in invisible_tiles[4]:
                        special_tile.visible = True
        for special_tile in special_tiles:
            if special_tile.visible:
                screen.blit(special_tile.image, (Constant.TILE_WIDTH * special_tile.id[1] - camera_left, Constant.TILE_HEIGHT * special_tile.id[0]))
        """ OUT OF MAP"""
        if (player.pos[1] + Constant.PLAYERHEIGHT >= Constant.SCREENRECT.height):
            game_state = Constant.GAMEOVER
            break

        """PLAYER GOES DOWN"""
        player.downable = True
        for tile in tiles:
            is_Visible = True
            for special_tile in special_tiles:
                if special_tile.id == tile.id and special_tile.visible == False:
                    is_Visible = False
                    break
            if not is_Visible :
                continue
            if tile.downable == True:
                continue;
            if (player.pos[0]  >= tile.pos[0] and player.pos[0]  <= tile.pos[0] + Constant.TILE_WIDTH) \
                    or ( player.pos[0] + Constant.PLAYERWIDTH  >= tile.pos [0] and player.pos[0] + Constant.PLAYERWIDTH  <= tile.pos[0] + Constant.TILE_WIDTH):
                if (player.pos[1] + Constant.PLAYERHEIGHT  >= tile.pos[1] and player.pos[1] + Constant.PLAYERHEIGHT <= tile.pos[1] + Constant.TILE_HEIGHT):
                    player.downable = False
                    break;
        """ WALL BLOCK """
        player.isBlockByWall = False
        for tile in tiles:
            is_Visible = True
            for special_tile in special_tiles:
                if special_tile.id == tile.id and special_tile.visible == False:
                    is_Visible = False
                    break
            if is_Visible and tile.isBlockByWall == True and player.pos[1] <= tile.pos[1] and player.pos[1] + Constant.PLAYERHEIGHT >= tile.pos[1] \
                and player.pos[1] > tile.pos[1] - Constant.TILE_HEIGHT:
                """ Player goes to the right """

                if player.direction == 1:
                    if player.pos[0] + Constant.PLAYERWIDTH + player.speed>= tile.pos[0] \
                            and player.pos[0] + Constant.PLAYERWIDTH  + player.speed <= tile.pos[0] + Constant.TILE_WIDTH:

                        player.isBlockByWall = True
                else:
                    if player.pos[0] - player.speed  >= tile.pos[0] \
                            and player.pos[0] - player.speed <= tile.pos[0] + Constant.TILE_WIDTH:
                        player.isBlockByWall = True
        """ GROUND BLOCK """
        player.is_block_by_ground = False
        for tile in tiles:
            is_Visible = True
            for special_tile in special_tiles:
                if special_tile.id == tile.id and special_tile.visible == False:
                    is_Visible = False
                    break
            if is_Visible and tile.isBlockByGround and player.jump > 0 and player.pos[1] >= tile.pos[1] and player.pos[1] <= tile.pos[1] + Constant.TILE_HEIGHT:
                if(player.pos[0]  >= tile.pos[0] and player.pos[0]  <= tile.pos[0] + Constant.TILE_WIDTH) \
                or ( player.pos[0] + Constant.PLAYERWIDTH  >= tile.pos [0] and player.pos[0] + Constant.PLAYERWIDTH  <= tile.pos[0] + Constant.TILE_WIDTH):
                    player.jump = 0

        """ Move with world """
        if not player.isBlockByWall and player.state == Constant.MOVE_STATE:
            if (((player.pos[0] + player.direction * player.speed) >= 0 ) and (player.pos[0] + player.direction * player.speed <= Constant.SCREENRECT.width * 8)):
                player.pos[0] += player.direction * player.speed
            if (camera_left + player.direction * player.speed >= 0) and (camera_right + player.direction * player.speed < Constant.SCREENRECT.width * 8):
                camera_left += player.direction * player.speed
                camera_right += player.direction * player.speed
                player.moveWithScreen = False
            else:
                player.moveWithScreen = True



        dict_collide = pygame.sprite.groupcollide(bombs, creeps, True, False)
        for key in dict_collide.keys():
            boom_sound.play()
            Explosion(key)
            for creep in dict_collide[key]:
                if not isinstance(creep, CreepASpecial):
                    creep.kill()
                else:
                    creep.check_die()
        #check va cham cua player voi dan cua monster
        dict_collide1 = pygame.sprite.spritecollide(player,monsterbombs, True)
        for key in dict_collide1:
            boom_sound.play()
            Explosion(key)
            player.lost_blood(70)
        #check va cham cua monster voi dan cua player
        if mymonster:
            dict_collide2 = pygame.sprite.spritecollide(mymonster,bombs, True)
            for key in dict_collide2:
                boom_sound.play()
                Explosion(key)
                mymonster.lost_blood(5)

        if pygame.sprite.spritecollide(player, creeps, True):
            player.lost_blood(40)

        item_collides = pygame.sprite.spritecollide(player, items, True)
        for item in item_collides:
            if isinstance(item, berry):
                player.typeOfBullet = EBulletType.THREE
                continue
            #item.playEffect()
            player.sound_money.play()
            player.money += 1
            player.enegery += 5

        for b in monsterbombs.sprites():
           b.update_pos(player.pos[0], player.rect.x)

        dirty = render_group.draw(screen)  # Draw all sprite, return list of rect
        pygame.display.update(dirty)    # Draw only changed rect
        pygame.display.flip()
        # Cap the frame rate
        clock.tick(Constant.FPS)
        #Clear tile list
        tiles[:] = []


    game_state = Constant.GAMEOVER

    game_over(screen, game_state)

# Call the "main" function if running this script
if __name__ == '__main__':
    start(Constant.HOME)
