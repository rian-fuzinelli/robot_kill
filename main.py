import pygame

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Jogo em Python")
icon = pygame.image.load('images/joystick.png').convert_alpha()
pygame.display.set_icon(icon)

# Player
background = pygame.image.load('images/bg.png').convert_alpha()
walk_left = [
    pygame.image.load('images/player-left/1.png').convert_alpha(),
    pygame.image.load('images/player-left/2.png').convert_alpha(),
    pygame.image.load('images/player-left/3.png').convert_alpha(),
    pygame.image.load('images/player-left/4.png').convert_alpha(),
    pygame.image.load('images/player-left/5.png').convert_alpha(),
]
walk_right = [
    pygame.image.load('images/player-right/1.png').convert_alpha(),
    pygame.image.load('images/player-right/2.png').convert_alpha(),
    pygame.image.load('images/player-right/3.png').convert_alpha(),
    pygame.image.load('images/player-right/4.png').convert_alpha(),
    pygame.image.load('images/player-right/5.png').convert_alpha(),
]

enemy = pygame.image.load('images/enemy.png').convert_alpha()
enemy = pygame.transform.scale(enemy, (80, 90))
enemy_list_in_game = []

player_anim_count = 0
bg_x = 0

player_speed = 10
player_x = 150
player_y = 500

is_jump = False
jump_count = 9

bg_audio = pygame.mixer.Sound('audio/music_game.mp3')
bg_audio.play()

enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 2500)

label = pygame.font.Font('fonts/Roboto-Black.ttf', 40)
lose_label = label.render('Você perdeu!', False, (193, 196, 199))
restart_label = label.render('Jogar de novo', False, (115, 132, 148))
restart_label_rect = restart_label.get_rect(topleft=(475, 425))

bullets_left = 50
bullet = pygame.image.load('images/bullet.png').convert_alpha()
bullet = pygame.transform.scale(bullet, (40, 40))
bullets = []

gameplay = True

running = True
while running:

    screen.blit(background, (bg_x, 0))
    screen.blit(background, (bg_x + 1280, 0))

    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if enemy_list_in_game:
            for (i, el) in enumerate(enemy_list_in_game):
                screen.blit(enemy, el)
                el.x -= 33

                if el.x < -10:
                    enemy_list_in_game.pop(i)

                reduced_enemy_rect = el.inflate(-30, -30)

                if player_rect.colliderect(reduced_enemy_rect):
                    gameplay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 200:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -9:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 9


        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 2
        if bg_x == -1280:
            bg_x = 0

        if bullets:
            for (i,el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 10

                if el.x > 1280:
                    bullets.pop(i)

                if enemy_list_in_game:
                    for (index, enemy_el) in enumerate(enemy_list_in_game):
                        if el.colliderect(enemy_el):
                            enemy_list_in_game.pop(index)
                            bullets.pop(i)
    else:
        screen.fill((25, 26, 27))
        screen.blit(lose_label, (475, 325))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            enemy_list_in_game.clear()
            bullets.clear()
            bullets_left = 50

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == enemy_timer:
            enemy_list_in_game.append(enemy.get_rect(topleft=(1282, 535)))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and bullets_left > 0:

            # Permite disparar até duas balas
            if len(bullets) < 2:  # Verifica se há menos de duas balas em jogo
                bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 50)))
                bullets_left -= 1

    clock.tick(18)