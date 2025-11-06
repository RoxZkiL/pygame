import pygame
import random
import math
import os

def main():
    pygame.init()

    # Rutas
    base_path = os.path.join(os.path.dirname(__file__), "assets")
    screen = pygame.display.set_mode((800, 600))

    # Título e ícono
    pygame.display.set_caption("Invasión Espacial")
    icon = pygame.image.load(os.path.join(base_path, "player.png"))
    pygame.display.set_icon(icon)
    background = pygame.image.load(os.path.join(base_path, "background.jpg"))

    # Jugador
    player_image = pygame.image.load(os.path.join(base_path, "player.png"))
    player_x = 368
    player_y = 500
    player_x_change = 0

    # Clase enemigo
    class Enemy:
        def __init__(self):
            self.image = pygame.image.load(os.path.join(base_path, "enemy.png"))
            self.x = random.randint(0, 736)
            self.y = random.randint(50, 240)
            self.x_change = 3
            self.y_change = 50

        def move(self):
            self.x += self.x_change
            if self.x <= 0:
                self.x_change = abs(self.x_change)
                self.y += self.y_change
            elif self.x >= 736:
                self.x_change = -abs(self.x_change)
                self.y += self.y_change

        def reset_position(self):
            self.x = random.randint(0, 736)
            self.y = random.randint(50, 240)

        def draw(self):
            screen.blit(self.image, (self.x, self.y))

    # Enemigos
    enemies = [Enemy() for _ in range(7)]

    # Bala
    bullet_image = pygame.image.load(os.path.join(base_path, "bullet.png"))
    bullet_x = 0
    bullet_y = 500
    bullet_y_change = 5
    bullet_visible = False

    # Puntaje
    score = 0
    font = pygame.font.Font(None, 28)
    final_font = pygame.font.Font(None, 64)

    def draw_player(x, y):
        screen.blit(player_image, (x, y))

    def shoot_bullet(x, y):
        nonlocal bullet_visible
        bullet_visible = True
        screen.blit(bullet_image, (x + 16, y + 10))

    def is_collision(x1, y1, x2, y2):
        return math.dist((x1, y1), (x2, y2)) < 30

    def show_score():
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    def show_game_over():
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        final_text = final_font.render("GAME OVER", True, (255, 50, 50))
        text_rect = final_text.get_rect(center=(400, 250))
        screen.blit(final_text, text_rect)

    running = True
    while running:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_x_change = -1
                if event.key == pygame.K_RIGHT:
                    player_x_change = 1
                if event.key == pygame.K_SPACE and not bullet_visible:
                    bullet_x = player_x
                    bullet_y = player_y
                    shoot_bullet(bullet_x, bullet_y)

            if event.type == pygame.KEYUP and event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                player_x_change = 0

        player_x = max(0, min(player_x + player_x_change, 736))

        game_over = False
        for enemy in enemies:
            if enemy.y > 500:
                game_over = True
                break

            enemy.move()
            if bullet_visible and is_collision(enemy.x, enemy.y, bullet_x, bullet_y):
                bullet_y = 500
                bullet_visible = False
                score += 1
                enemy.reset_position()

            enemy.draw()

        if game_over:
            for e in enemies:
                e.y = 1000
            show_game_over()
        else:
            if bullet_visible:
                shoot_bullet(bullet_x, bullet_y)
                bullet_y -= bullet_y_change
                if bullet_y <= -64:
                    bullet_visible = False
                    bullet_y = player_y
            draw_player(player_x, player_y)
            show_score()

        pygame.display.update()

if __name__ == "__main__":
    main()