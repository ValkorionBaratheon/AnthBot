# Player

class Player:
    def __init__(self, user):
        self.user = user
        self.turn_status = True
        self.health = 100
        self.dead = False

    def set_health(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.dead = True