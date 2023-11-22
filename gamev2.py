import random
import pygame

pygame.init()

WIDTH = 1000
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)
bg_color = (128, 128, 128)
game_speed = 3
init_y = HEIGHT - 130
distance = 0
gravity = 0.4
distance = 0
high_score = 0
lifetime = 0

class GameScreen:
    def __init__(self, width, height, bg_color, game_speed, font):
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.game_speed = game_speed
        self.font = font
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.line_list = [0, width / 4, 2 * width / 4, 3 * width / 4]
        self.laser = []
        self.distance = 0
        self.new_bg = 0
        self.restart_cmd = False
        self.pause = False
        self.restart_btn = pygame.draw.rect(self.surface, 'white', [200, 220, 280, 50], 0, 10)
        self.quit_btn = pygame.draw.rect(self.surface, 'white', [520, 220, 280, 50], 0, 10)

    def update(self, distance, new_bg, high_score):
        self.surface.fill('black')
        pygame.draw.rect(self.surface, (self.bg_color[0], self.bg_color[1], self.bg_color[2], 50), [0, 0, self.width, self.height])
        screen.blit(self.surface, (0, 0))
        top = pygame.draw.rect(screen, 'gray', [0, 0, self.width, 50])
        bot = pygame.draw.rect(screen, 'gray', [0, self.height - 50, self.width, 50])

        # Verifique se a lista laser tem pelo menos dois elementos antes de acessá-los
        if len(self.laser) >= 2:
            for i in range(len(self.line_list)):
                pygame.draw.line(screen, 'black', (self.line_list[i], 0), (self.line_list[i], 50), 3)
                pygame.draw.line(screen, 'black', (self.line_list[i], self.height - 50), (self.line_list[i], self.height), 3)
                if not self.pause:
                    self.line_list[i] -= self.game_speed
                    self.laser[0][0] -= self.game_speed
                    self.laser[1][0] -= self.game_speed
                if self.line_list[i] < 0:
                    self.line_list[i] = self.width

            lase_line = pygame.draw.line(screen, 'yellow', (self.laser[0][0], self.laser[0][1]), (self.laser[1][0], self.laser[1][1]), 10)
            pygame.draw.circle(screen, 'yellow', (self.laser[0][0], self.laser[0][1]), 12)
            pygame.draw.circle(screen, 'yellow', (self.laser[1][0], self.laser[1][1]), 12)

        screen.blit(self.font.render(f'Distance: {int(distance)} m', True, 'white'), (10, 10))
        screen.blit(self.font.render(f'High Score: {int(high_score)} m', True, 'white'), (10, 70))

        return top, bot, lase_line

    def draw_menu(self):
        pygame.draw.rect(self.surface, (128, 128, 128, 150), [0, 0, self.width, self.height])
        pygame.draw.rect(self.surface, 'dark gray', [200, 150, 600, 50], 0, 10)
        self.surface.blit(self.font.render('Game Paused. Escape Btn Resumes', True, 'black'), (220, 160))
        self.surface.blit(self.font.render('Restart', True, 'black'), (220, 230))
        self.surface.blit(self.font.render('Quit', True, 'black'), (540, 230))
        pygame.draw.rect(self.surface, 'dark gray', [200, 300, 600, 50], 0, 10)
        self.surface.blit(self.font.render(f'Lifetime Distance Ran: {int(lifetime)}', True, 'black'), (220, 310))
        screen.blit(self.surface, (0, 0))

# Uso da classe
game_screen = GameScreen(WIDTH, HEIGHT, bg_color, game_speed, font)

class Player:
    def __init__(self, x, init_y):
        self.x = x
        self.init_y = init_y
        self.player_y = init_y
        self.counter = 0
        self.booster = False
        self.colliding = False  # New attribute to track collisions

    def update(self):
        play = pygame.rect.Rect((120, self.player_y + 10), (25, 60))

        if self.player_y < self.init_y or game_screen.pause:
            self.draw_boosted_player()
        else:
            self.draw_normal_player()

        pygame.draw.rect(screen, 'white', [100, self.player_y + 20, 20, 30], 0, 5)
        pygame.draw.ellipse(screen, 'orange', [120, self.player_y + 20, 30, 50])
        pygame.draw.circle(screen, 'orange', (135, self.player_y + 15), 10)
        pygame.draw.circle(screen, 'black', (138, self.player_y + 12), 3)

        return play

    def draw_boosted_player(self):
        if self.booster:
            pygame.draw.ellipse(screen, 'red', [100, self.player_y + 50, 20, 30])
            pygame.draw.ellipse(screen, 'orange', [105, self.player_y + 50, 10, 30])
            pygame.draw.ellipse(screen, 'yellow', [110, self.player_y + 50, 5, 30])
        pygame.draw.rect(screen, 'yellow', [128, self.player_y + 60, 10, 20], 0, 3)
        pygame.draw.rect(screen, 'orange', [130, self.player_y + 60, 10, 20], 0, 3)

    def draw_normal_player(self):
        if self.counter < 10:
            pygame.draw.line(screen, 'yellow', (128, self.player_y + 60), (140, self.player_y + 80), 10)
            pygame.draw.line(screen, 'orange', (130, self.player_y + 60), (120, self.player_y + 80), 10)
        elif 10 <= self.counter < 20:
            pygame.draw.rect(screen, 'yellow', [128, self.player_y + 60, 10, 20], 0, 3)
            pygame.draw.rect(screen, 'orange', [130, self.player_y + 60, 10, 20], 0, 3)
        elif 20 <= self.counter < 30:
            pygame.draw.line(screen, 'yellow', (128, self.player_y + 60), (120, self.player_y + 80), 10)
            pygame.draw.line(screen, 'orange', (130, self.player_y + 60), (140, self.player_y + 80), 10)
        else:
            pygame.draw.rect(screen, 'yellow', [128, self.player_y + 60, 10, 20], 0, 3)
            pygame.draw.rect(screen, 'orange', [130, self.player_y + 60, 10, 20], 0, 3)


# Uso da classe
player = Player(120, init_y)
def modify_player_info():
    global high_score, lifetime
    if distance > high_score:
        high_score = distance
    lifetime += distance
    file = open('player_info.txt', 'w')
    file.write(str(int(high_score)) + '\n')
    file.write(str(int(lifetime)))
    file.close()
    


class LaserGenerator:
    def __init__(self):
        self.WIDTH = 1000
        self.HEIGHT = 600

    def generate_laser(self):
        laser_type = random.randint(0, 1)
        offset = random.randint(10, 300)

        if laser_type == 0:
            laser_width = random.randint(100, 300)
            laser_y = random.randint(100, self.HEIGHT - 100)
            new_lase = [[self.WIDTH + offset, laser_y], [self.WIDTH + offset + laser_width, laser_y]]
        else:
            laser_height = random.randint(100, 300)
            laser_y = random.randint(100, self.HEIGHT - 400)
            new_lase = [[self.WIDTH + offset, laser_y], [self.WIDTH + offset, laser_y + laser_height]]

        return new_lase

# Uso da classe
laser_generator = LaserGenerator()

class Rocket:
    def __init__(self, screen, font, game_speed, player_y):
        self.screen = screen
        self.font = font
        self.game_speed = game_speed
        self.player_y = player_y
        self.rocket_counter = 0
        self.rocket_active = False
        self.rocket_delay = 0
        self.rocket_coords = []

    def draw_rocket(self, coords, mode):
        if mode == 0:
            rock = pygame.draw.rect(self.screen, 'dark red', [coords[0] - 60, coords[1] - 25, 50, 50], 0, 5)
            self.screen.blit(self.font.render('!', True, 'black'), (coords[0] - 40, coords[1] - 20))
            if not self.pause:
                if coords[1] > self.player_y + 10:
                    coords[1] -= 3
                else:
                    coords[1] += 3
        else:
            rock = pygame.draw.rect(self.screen, 'red', [coords[0], coords[1] - 10, 50, 20], 0, 5)
            pygame.draw.ellipse(self.screen, 'orange', [coords[0] + 50, coords[1] - 10, 50, 20], 7)
            if not self.pause:
                coords[0] -= 10 + self.game_speed

        return coords, rock

    def update(self, pause):
        if not self.rocket_active and not pause:
            self.rocket_counter += 1
        if self.rocket_counter > 180:
            self.rocket_counter = 0
            self.rocket_active = True
            self.rocket_delay = 0
            self.rocket_coords = [WIDTH, HEIGHT / 2]
        if self.rocket_active:
            if self.rocket_delay < 90:
                if not pause:
                    self.rocket_delay += 1
                self.rocket_coords, _ = self.draw_rocket(self.rocket_coords, 0)
            else:
                self.rocket_coords, _ = self.draw_rocket(self.rocket_coords, 1)
            if self.rocket_coords[0] < -50:
                self.rocket_active = False

    def draw(self):
        _, rocket = self.draw_rocket(self.rocket_coords, 1)
        return rocket



# Uso da classe
rocket = Rocket(screen, font, game_speed,player.player_y)

run = True
# ... Código anterior ...

# Lógica de atualização
while run:
    timer.tick(fps)

    # Lógica de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            modify_player_info()
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Toggle pause
                game_screen.pause = not game_screen.pause
            elif event.key == pygame.K_SPACE and not game_screen.pause:
                player.booster = True
        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            player.booster = False
        elif event.type == pygame.MOUSEBUTTONDOWN and game_screen.pause:
            if game_screen.restart_btn.collidepoint(event.pos):
                game_screen.restart_cmd = True
            elif game_screen.quit_btn.collidepoint(event.pos):
                modify_player_info()
                run = False

    # Lógica de atualização das classes
    player.update()
    rocket.update(game_screen.pause)
    rocket.draw()

    # Lógica de desenho das classes
    game_screen.update(distance, game_screen.new_bg, high_score)
    game_screen.draw()

    
    rocket.draw()

    # Lógica de atualização das classes
    player.update()
    rocket.update(pause=True)
    game_screen.update()

    # Lógica de desenho das classes
    screen.fill(bg_color)

    top, bot, lase_line = game_screen.update()
    player_rect = player.draw()

    if game_screen.rocket_active:
        rocket_rect = rocket.draw()

    pygame.draw.rect(screen, 'gray', [0, 0, WIDTH, 50])
    pygame.draw.rect(screen, 'gray', [0, HEIGHT - 50, WIDTH, 50])

    for i in range(len(game_screen.line_list)):
        pygame.draw.line(screen, 'black', (game_screen.line_list[i], 0), (game_screen.line_list[i], 50), 3)
        pygame.draw.line(screen, 'black', (game_screen.line_list[i], HEIGHT - 50), (game_screen.line_list[i], HEIGHT), 3)

    screen.blit(font.render(f'Distance: {int(game_screen.distance)} m', True, 'white'), (10, 10))
    screen.blit(font.render(f'High Score: {int(game_screen.high_score)} m', True, 'white'), (10, 70))

    # Verifica colisão entre o jogador e a linha superior e inferior
   # Verifica colisão entre o jogador e a linha superior e inferior
if player_rect.colliderect(top) or player_rect.colliderect(bot):
    player.player_y = player.init_y
    game_screen.distance = 0

# Verifica colisão entre o jogador e as linhas verticais
for i in range(len(game_screen.line_list)):
    if player_rect.colliderect(pygame.Rect(game_screen.line_list[i], 0, 3, 50)) or \
            player_rect.colliderect(pygame.Rect(game_screen.line_list[i], HEIGHT - 50, 3, 50)):
        player.player_y = player.init_y
        game_screen.distance = 0

# Verifica colisão entre o jogador e o laser
if lase_line.colliderect(player_rect):
    player.player_y = player.init_y
    game_screen.distance = 0

# Verifica colisão entre o jogador e o foguete
if game_screen.rocket_active and rocket_rect.colliderect(player_rect):
    player.player_y = player.init_y
    game_screen.distance = 0

    # Atualiza a distância total percorrida
    game_screen.distance += game_speed
    distance+=game_speed
    

    pygame.display.flip()

# ... Restante do código ...
pygame.quit()
