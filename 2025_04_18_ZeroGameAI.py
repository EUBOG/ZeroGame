import pygame
import random
import math
import time

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 600, 800
WHITE = (255, 255, 255)
BLUE = (173, 216, 230)  # Голубой цвет для сугробов

# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Лыжный марафон")

# Класс лыжников
class Skier():
    def __init__(self, x, y, speed_x, speed_y, image):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.image = image

    def moveski(self, image):
        self.image = image
        self.y += self.speed_y
        if self.y > HEIGHT:  # Если лыжник вышел за экран, то его надо перезапустить
            self.y = -20

    def drawski(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Загружаем изображения
bolshunov_left = pygame.image.load("skier_left_100.png")
bolshunov_right = pygame.image.load("skier_right_100.png")
blue_skier_left = pygame.image.load("skier_left_100_2_blue.png")
blue_skier_right = pygame.image.load("skier_right_100_2_blue.png")
red_skier_left = pygame.image.load("skier_left_100_3_red.png")
red_skier_right = pygame.image.load("skier_right_100_3_red.png")
snowflake_cursor = pygame.image.load("snow-10.png")  # Загружаем изображение снежинки
image_rect1 = bolshunov_left.get_rect()
image_rect_blue = blue_skier_left.get_rect()
image_rect_red = red_skier_left.get_rect()
blue_skier_image = blue_skier_left
red_skier_image = red_skier_left
blueskier = Skier(200, -20, 0, 2, blue_skier_image)
redskier = Skier(300, -20, 0, 1, red_skier_image)
image_rect_blue.x = 200
image_rect_red.x = 300

speed = 3 # Определяем скорость

class Snowdrift: # Класс сугробов
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width # ширина сугроба
        self.height = 5  # Высота сугроба

    def move(self, speed):
        self.y += speed
        if self.y > HEIGHT:  # Если сугроб вышел за экран, то его надо перезапустить
            self.y = -20

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# --- Назначаем шрифт ---
font = pygame.font.Font(None, 20)

collision_status = "Гонка проходит нормально" # начальный статус
total_distance = 0  # Общее пройденное расстояние
distance_multiplier = 0.001  # Коэффициент пересчёта (можно настроить)
start_time = 0  # Время начала заезда
current_time = 0  # Текущее время

# Основной игровой цикл
def main():
    global start_time, current_time
    start_time = time.time()  # Фиксируем время старта
    clock = pygame.time.Clock()
    running = True
    global speed
    Leftdrifts = []
    Rightdrifts = []

    # Переменные для управления временем и состоянием изображений лыжников
    bolshunov_image = bolshunov_left
    blue_skier_image = blue_skier_left
    red_skier_image = red_skier_left
    last_switch_time_b = time.time()
    last_switch_time_blue = time.time()
    last_switch_time_red = time.time()
    switch_interval_b = 0.5  # 0.5 секунды
    switch_interval_blue = 0.4  # 0.4 секунды
    switch_interval_red = 0.3  # 0.3 секунды

    # Генерация левых сугробов
    for i in range(40):
        x = 0
        y = - 20 - i * 5
        width = 5 + (i + 0) * 5
        Leftdrifts.append(Snowdrift(x, y, width))
    for n in range(10):
        x = 0
        y = - 20 - (i + n) * 5
        width = 5 + (i + 0) * 5
        Leftdrifts.append(Snowdrift(x, y, width))

    # Генерация правых сугробов
    for i in range(40):
        width = 5 + (i + 0) * 5
        x = 600 - width
        y = -250 - i * 5
        Rightdrifts.append(Snowdrift(x, y, width))
    for n in range(10):
        x = 600 - (5 + (i + 0) * 5)
        y = - 250 - (i + n) * 5
        width = 5 + (i + 0) * 5
        Rightdrifts.append(Snowdrift(x, y, width))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:  # это настройка курсора мыши чуть выше центра фигуры Большунова
                mouseX, mouseY = pygame.mouse.get_pos()
                image_rect1.x = mouseX - 50
                image_rect1.y = mouseY - 35

        if time.time() - last_switch_time_b > switch_interval_b:
            if bolshunov_image == bolshunov_left: # Каждые 0,5 с меняем положение Большунова - имитируем отталкивания
                bolshunov_image = bolshunov_right
            else:
                bolshunov_image = bolshunov_left
            last_switch_time_b = time.time()  # Обновляем время последнего переключения большунова

        if time.time() - last_switch_time_blue > switch_interval_blue:
            if blue_skier_image == blue_skier_left: # каждые 0,4 с меняем положение синего лыжника - имитируем отталкивания
                blue_skier_image = blue_skier_right
            else:
                blue_skier_image = blue_skier_left
            last_switch_time_blue = time.time() # Обновляем время последнего переключения

        if time.time() - last_switch_time_red > switch_interval_red:
            if red_skier_image == red_skier_left: # каждые 0,3 с меняем положение красного лыжника - имитируем отталкивания
                red_skier_image = red_skier_right
            else:
                red_skier_image = red_skier_left
            last_switch_time_red = time.time() # Обновляем время последнего переключения

        # Перемещение лыжников
        blueskier.moveski(blue_skier_image)
        redskier.moveski(red_skier_image)

        # Отрисовка экрана
        screen.fill(WHITE)

        # Обновление состояния сугробов
        for snowdrift in Leftdrifts:
            snowdrift.move(speed)
        for snowdrift in Rightdrifts:
            snowdrift.move(speed)

        # Отрисовка сугробов
        for snowdrift in Leftdrifts:
            snowdrift.draw(screen)
        for snowdrift in Rightdrifts:
            snowdrift.draw(screen)
        # Отрисовка Большунова
        screen.blit(bolshunov_image, image_rect1)
        blueskier.drawski(screen)  # Отрисовка синего лыжника
        redskier.drawski(screen)   # Отрисовка красного лыжника

        image_rect_blue = blueskier.image.get_rect(topleft=(blueskier.x, blueskier.y))
        image_rect_red = redskier.image.get_rect(topleft=(redskier.x, redskier.y))

        if image_rect1.colliderect(image_rect_blue):
            speed = 1
            collision_status = "Столкнулся с синим!"
            # print(speed)
        elif image_rect1.colliderect(image_rect_red):
            speed = 2
            # print(speed)
            collision_status = "Столкнулся с красным!"
        else:
            speed = 3
            collision_status = "Гонка продолжается"

        # Проверяем столкновения синего лыжника
        for drift in Leftdrifts + Rightdrifts:
            if image_rect1.colliderect(drift.get_rect()):
                speed = 1
                collision_status = "Заехал в сугроб!"

        collision_text = font.render(collision_status, True, (0, 0, 0))
        screen.blit(collision_text, (10, 30))

        # Текущая скорость
        speed_text = font.render(f"Скорость: {speed}", True, (0, 0, 0))
        screen.blit(speed_text, (10, 10))

        # Увеличиваем расстояние на величину перемещения за кадр
        global total_distance
        total_distance += image_rect1.y * distance_multiplier

        # Отрисовываем расстояние
        distance_text = font.render(f"Дистанция: {int(total_distance)} м", True, (0, 0, 0))
        screen.blit(distance_text, (10, 50))

        current_time = time.time() - start_time  # Вычисляем время игры

        # Отрисовываем время в формате ММ:СС
        mins, secs = divmod(int(current_time), 60)
        time_text = font.render(f"Время: {mins:02d}:{secs:02d}", True, (0, 0, 0))
        screen.blit(time_text, (10, 70))

        average_speed = round(total_distance / current_time, 2)
        average_speed_text = font.render(f"Средняя корость: {average_speed}", True, (0, 0, 0))
        screen.blit(average_speed_text, (10, 90))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()