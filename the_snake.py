"""Игра «Изгиб Питона» на Python и Pygame."""

from random import choice

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(
        self,
        position=CENTER_POSITION,
        body_color=None,
    ):
        """Инициализирует позицию и цвет объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод для отрисовки, переопределяется в дочерних классах."""
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко."""

    def __init__(self):
        """Инициализирует яблоко, задаёт цвет и случайную позицию."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self, occupied=()):
        """Размещает яблоко в случайной свободной клетке."""
        occupied = set(occupied)
        free_cells = [
            (x, y)
            for y in range(0, SCREEN_HEIGHT, GRID_SIZE)
            for x in range(0, SCREEN_WIDTH, GRID_SIZE)
            if (x, y) not in occupied
        ]
        self.position = choice(free_cells)

    def draw(self):
        """Отрисовывает яблоко на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку и её поведение."""

    def __init__(self):
        """Инициализирует начальное состояние змейки."""
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Обновляет направление движения после нажатия клавиши."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Затирает след и отрисовывает все сегменты змейки."""
        if self.last is not None:
            rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice((UP, DOWN, LEFT, RIGHT))
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP
                    and game_object.direction != DOWN):
                game_object.next_direction = UP
            elif (event.key == pygame.K_DOWN
                    and game_object.direction != UP):
                game_object.next_direction = DOWN
            elif (event.key == pygame.K_LEFT
                    and game_object.direction != RIGHT):
                game_object.next_direction = LEFT
            elif (event.key == pygame.K_RIGHT
                    and game_object.direction != LEFT):
                game_object.next_direction = RIGHT


def main():
    """Основной игровой цикл."""
    # Инициализация PyGame:
    pygame.init()
    # Создание экземпляров классов.
    snake = Snake()
    apple = Apple()
    apple.randomize_position(snake.positions)
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)
        elif snake.get_head_position() == apple.position:
            snake.length += 1
            if snake.last is not None:
                snake.positions.append(snake.last)
                snake.last = None
            if snake.length == GRID_WIDTH * GRID_HEIGHT:
                snake.reset()
                screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
