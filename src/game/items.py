class Item:
    def __init__(self, name, description, item_type, value, effect=None):
        self.name = name
        self.description = description
        self.item_type = item_type   # 'weapon', 'armor', 'potion'
        self.value = value           # цена в золоте
        self.effect = effect         # число (хилы, +атака и т.д.)

    def use(self, player):
        if self.item_type == 'potion':
            player.hp = min(player.hp + self.effect, player.max_hp)
            return True   # предмет расходуется
        elif self.item_type == 'weapon':
            player.attack += self.effect
            return False  # экипируется, не расходуется
        elif self.item_type == 'armor':
            player.defense += self.effect
            return False
        return False
