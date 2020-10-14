import pygame
import random
import copy
import sys


class Body:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction


def draw_rect_with_borders(screen, coord, border_color, color, thickness):
    x, y, dist1, dist2 = coord

    pygame.draw.rect(screen, border_color, (x, y, dist1, dist2))
    pygame.draw.rect(screen, color, (x + thickness, y + thickness, dist1 - 2 * thickness, dist2 - 2 * thickness))


def am_i_outside(snake, width, height, dist):
    return snake[0].x < 0 or snake[0].x + dist > width or snake[0].y < 0 or snake[0].y + dist > height


def hit_myself(snake, head, dist):
    for i in range(1, len(snake)):
        if snake[i].x == head.x and snake[i].y == head.y:
            return True
    return False


def main():
    pygame.init()

    white = (255, 255, 255)
    black = (0, 0, 0)
    green = (2, 250, 5)
    red = (255, 0, 0)

    width = 800
    height = 640
    dist = 30
    thickness = 4
    dim = (width, height)

    move_x = 0
    move_y = 0

    screen = pygame.display.set_mode(dim)

    pygame.display.set_caption('snake game')

    x, y = width // 2 - dist + 100, height // 2 - dist
    apple_x, apple_y = width // 2 - dist - 100, height // 2 - dist

    draw_rect_with_borders(screen, (x, y, dist, dist), white, green, thickness)

    snake = [Body(x, y, "left")]

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif keys[pygame.K_UP] and snake[0].direction != "down":
                snake[0].direction = "up"
                move_x = 0
                move_y = -dist
            elif keys[pygame.K_DOWN] and snake[0].direction != "up":
                snake[0].direction = "down"
                move_x = 0
                move_y = dist
            elif keys[pygame.K_LEFT] and snake[0].direction != "right":
                snake[0].direction = "left"
                move_x = -dist
                move_y = 0
            elif keys[pygame.K_RIGHT] and snake[0].direction != "left":
                snake[0].direction = "right"
                move_x = dist
                move_y = 0

        save = copy.deepcopy(snake)

        snake[0].x += move_x
        snake[0].y += move_y

        for i in range(1, len(snake)):
            snake[i] = save[i - 1]

        for i in range(len(snake)):
            draw_rect_with_borders(screen, (snake[i].x, snake[i].y, dist, dist), white, green, thickness)

        if (apple_x <= snake[0].x <= apple_x + dist and apple_y <= snake[0].y <= apple_y + dist) \
                or (apple_x <= snake[0].x + dist <= apple_x + dist and apple_y <= snake[0].y + dist <= apple_y + dist) \
                or (apple_x <= snake[0].x + dist <= apple_x + dist and apple_y <= snake[0].y + dist <= apple_y + dist) \
                or (apple_x <= snake[0].x + dist <= apple_x + dist and apple_y <= snake[0].y + dist <= apple_y + dist):

            apple_x = random.randint(30, width - 30)
            apple_y = random.randint(30, height - 30)

            if snake[-1].direction == "up":
                snake.append(Body(snake[-1].x, snake[-1].y + dist, snake[-1].direction))
            elif snake[-1].direction == "down":
                snake.append(Body(snake[-1].x, snake[-1].y - dist, snake[-1].direction))
            elif snake[-1].direction == "left":
                snake.append(Body(snake[-1].x + dist, snake[-1].y, snake[-1].direction))
            elif snake[-1].direction == "right":
                snake.append(Body(snake[-1].x - dist, snake[-1].y, snake[-1].direction))

        draw_rect_with_borders(screen, (apple_x, apple_y, dist, dist), white, red, thickness)

        pygame.display.update()

        if am_i_outside(snake, width, height, dist) or hit_myself(snake, snake[0], dist):
            pygame.quit()
            sys.exit()

        screen.fill(black)
        clock.tick(20)


if __name__ == '__main__':
    main()
