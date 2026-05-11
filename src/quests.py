class Quest:
    def __init__(self, name, description, reward_gold, reward_exp):
        self.name = name
        self.description = description
        self.completed = False
        self.reward_gold = reward_gold
        self.reward_exp = reward_exp
        self.objectives = []

    def add_objective(self, description, target_count, current_count=0):
        self.objectives.append({
            'description': description,
            'target': target_count,
            'current': current_count
        })

    def update_objective(self, index, amount=1):
        if index >= len(self.objectives):
            return False
        self.objectives[index]['current'] += amount

        all_completed = all(obj['current'] >= obj['target'] for obj in self.objectives)
        self.completed = all_completed
        return self.completed

    def claim_reward(self, player):
        if self.completed:
            player.gold += self.reward_gold
            player.gain_experience(self.reward_exp)
            return True
        return False
