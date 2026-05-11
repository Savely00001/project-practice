import pygame

class Player:
    def __init__(self, x, y, scale=1.0):
        # Размер кадра из спрайт-листа (96x80, 8 кадров)
        self.frame_width = 96
        self.frame_height = 80

        # Отображаемый размер с учётом масштаба
        self.width = int(self.frame_width * scale)
        self.height = int(self.frame_height * scale)

        self.x = x
        self.y = y
        self.speed = 5
        self.direction = 'down'
        self.is_moving = False

        # Игровые характеристики
        self.name = "Герой"
        self.level = 1
        self.max_hp = 100
        self.hp = 100
        self.attack = 10
        self.defense = 5
        self.experience = 0
        self.inventory = []      # список объектов Item
        self.gold = 0
        self.active_quests = []  # список активных квестов

        # Количество кадров
        self.FRAMES = 8

        # Словари для хранения кадров
        self.run_anim = {}
        self.idle_anim = {}

        directions = ['down', 'up', 'left', 'right']

        # Загрузка анимации бега (player_*_sheet.png)
        for d in directions:
            path = f'assets/player_{d}_sheet.png'
            try:
                sheet = pygame.image.load(path).convert_alpha()
            except FileNotFoundError:
                print(f"ОШИБКА: не найден файл {path}")
                sheet = pygame.Surface((self.frame_width, self.frame_height))
                sheet.fill((255, 0, 255))
            frames = []
            for i in range(self.FRAMES):
                rect = pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)
                frame = sheet.subsurface(rect)
                if scale != 1.0:
                    frame = pygame.transform.scale(frame, (self.width, self.height))
                frames.append(frame)
            self.run_anim[d] = frames

        # Загрузка анимации бездействия (idle_*.png)
        for d in directions:
            path = f'assets/idle_{d}.png'
            try:
                sheet = pygame.image.load(path).convert_alpha()
            except FileNotFoundError:
                print(f"ОШИБКА: не найден файл {path}")
                sheet = pygame.Surface((self.frame_width, self.frame_height))
                sheet.fill((0, 255, 0))
            frames = []
            for i in range(self.FRAMES):
                rect = pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)
                frame = sheet.subsurface(rect)
                if scale != 1.0:
                    frame = pygame.transform.scale(frame, (self.width, self.height))
                frames.append(frame)
            self.idle_anim[d] = frames

        # Параметры анимации
        self.current_frame = 0
        self.anim_speed_run = 0.08
        self.anim_speed_idle = 0.15
        self.last_update = pygame.time.get_ticks()

        # Прямоугольник для коллизий
        self.rect = pygame.Rect(x, y, self.width, self.height)

        print("Player создан. Анимация бега и покоя загружена.")

    def update_animation(self):
        now = pygame.time.get_ticks()
        speed = self.anim_speed_run if self.is_moving else self.anim_speed_idle
        if now - self.last_update > speed * 1000:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % self.FRAMES

    def move(self, dx, dy):
        old_moving = self.is_moving
        old_dir = self.direction

        if dx > 0:
            self.direction = 'right'
        elif dx < 0:
            self.direction = 'left'
        elif dy > 0:
            self.direction = 'down'
        elif dy < 0:
            self.direction = 'up'

        self.is_moving = (dx != 0 or dy != 0)

        if self.direction != old_dir or self.is_moving != old_moving:
            self.current_frame = 0
            self.last_update = pygame.time.get_ticks()

        self.x += dx
        self.y += dy
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen):
        self.update_animation()
        current_set = self.run_anim if self.is_moving else self.idle_anim
        sprite = current_set[self.direction][self.current_frame]
        screen.blit(sprite, (self.x, self.y))

    def gain_experience(self, amount):
        self.experience += amount
        exp_needed = self.level * 100
        if self.experience >= exp_needed:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_hp += 20
        self.hp = self.max_hp
        self.attack += 2
        self.defense += 1
        self.experience = 0
        print(f"Level up! Now level {self.level}")
