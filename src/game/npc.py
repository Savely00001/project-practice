import pygame

class NPC:
    def __init__(self, x, y, name, sprite_path, is_enemy=False, scale=1.0):
        self.x = x
        self.y = y
        self.name = name
        self.is_enemy = is_enemy
        self.scale = scale

        # Загрузка и масштабирование спрайта
        try:
            original = pygame.image.load(sprite_path).convert_alpha()
        except FileNotFoundError:
            print(f"ОШИБКА: не найден спрайт {sprite_path}")
            original = pygame.Surface((32, 32))
            original.fill((128, 128, 128))
        # Масштабируем
        if scale != 1.0:
            w = int(original.get_width() * scale)
            h = int(original.get_height() * scale)
            self.sprite = pygame.transform.scale(original, (w, h))
        else:
            self.sprite = original

        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()
        self.rect = pygame.Rect(x, y, self.width, self.height)

        if is_enemy:
            self.hp = 50
            self.attack = 8
            self.defense = 3
            self.experience_reward = 20
            self.gold_reward = 10

        self.dialogues = []

    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))

    def add_dialogue(self, text):
        self.dialogues.append(text)

    def get_dialogue(self):
        if not self.dialogues:
            return "..."
        return self.dialogues[0]
