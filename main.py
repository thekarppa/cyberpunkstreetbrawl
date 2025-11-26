import json
import random

'''Open up the stat and flavor text files'''
with open("player_stats.json", "r", encoding="utf-8") as p_source:
    p_stats = json.load(p_source)
with open("enemy_stats.json", "r", encoding="utf-8") as e_source:
    e_stats = json.load(e_source)

'''Used for various easily accessible functions'''
class Game:
    def __init__(self):
        self.p_name = ""
        self.player_name = None

    def intro(self):
        print("You are an Edgerunner and you came across a street punk…")
        self.p_name = input("What is your street name? ") or "Street Bear"
        self.player_name = Player(p_stats, self.p_name)

    '''Used in the intro and to easily show the combat mechanics instructions'''
    @staticmethod
    def instructions():
        print("Use the following options to fight:")
        print("1. Attack - Choose a weapon to attack with:")
        print("Your pistol is weaker but more accurate than your rifle.")
        print("Your melee weapon is accurate, but you also expose yourself to nastier hits in melee.")
        print("2. Dodge  - You make an evasive attack, but your accuracy will be slightly hindered.")
        print("3. Cover  - Seek cover to lessen the chance of being hit fir a few turns.")
        print("4. Reload - Reload a given gun. You can only reload one gun at a time.")

    '''Shorter action menu'''
    @staticmethod
    def short_instructions():
        print("1. Attack")
        print("2. Dodge")
        print("3. Cover")
        print("4. Reload")
        print("5. Instructions")
        print("6. Quit")

    '''Asking for player actions'''
    @staticmethod
    def which_attack():
        _choice = input("What do you want to do? ")
        if _choice == "1":
            pass
        elif _choice == "2":
            pass
        elif _choice == "3":
            pass
        elif _choice == "4":
            pass
        elif _choice == "5":
            Game.instructions()
        elif _choice == "6":
            exit(0)
        else:
            Game.short_instructions()

    '''Function for each choice'''
    @staticmethod
    def chose_attack():
        pass
    @staticmethod
    def chose_dodge():
        pass
    @staticmethod
    def chose_cover():
        pass
    @staticmethod
    def chose_reload():
        pass

    '''Making an attack roll: the simple idea is
    "accuracy + accuracy bonuses vs dodge + dodge bonuses" against a random 100 roll'''
    @staticmethod
    def player_attack(self, enemy, accuracy_total=0, dodge_total=0):
        hit_chance = (player1.accuracy + accuracy_total) - (enemy.dodge + dodge_total)
        print(f"The chance to hit is {hit_chance}!")

'''Initialize each player with stats. In v0.1 there is only one player.
p_stats holds the stats from the json file'''
class Player:
    def __init__(self, pstats, name):
        self.max_p_hp = pstats["player"]["p_hp"]
        self.armor = pstats["player"]["p_armor"]
        self.accuracy = pstats["player"]["p_accuracy"]
        self.dodge = pstats["player"]["p_dodge"]
        self.m_damage = pstats["player"]["p_melee_damage"]
        self.m_acc_bonus = pstats["player"]["p_melee_accuracy_bonus"]
        self.m_acc_pen = pstats["player"]["p_melee_dodge_penalty"]
        self.pistol_dam = pstats["player"]["p_pistol_damage"]
        self.pistol_acc = pstats["player"]["p_pistol_accuracy_bonus"]
        self.pistol_max_ammo = pstats["player"]["p_pistol_ammo"]
        self.rifle_damage = pstats["player"]["p_rifle_damage"]
        self.rifle_acc = pstats["player"]["p_rifle_accuracy_bonus"]
        self.rifle_max_ammo = pstats["player"]["p_rifle_ammo"]
        self.pistol_ammo = self.pistol_max_ammo
        self.rifle_ammo = self.rifle_max_ammo
        self.dodge_bonus = 0
        self.runner_name = name

'''Initialize enemies with stats. In v.01 there is just one enemy'''
class Enemy:
    def __init__(self, estats):
        self.max_e_hp = estats["enemy"]["e_hp"]
        self.armor = estats["enemy"]["e_armor"]
        self.accuracy = estats["enemy"]["e_accuracy"]
        self.dodge = estats["enemy"]["e_dodge"]
        self.m_damage = estats["enemy"]["e_melee_damage"]
        self.m_acc_bonus = estats["enemy"]["e_melee_accuracy_bonus"]
        self.m_acc_pen = estats["enemy"]["e_melee_dodge_penalty"]
        self.pistol_dam = estats["enemy"]["e_pistol_damage"]
        self.pistol_acc = estats["enemy"]["e_pistol_accuracy_bonus"]
        self.pistol_max_ammo = estats["enemy"]["e_pistol_ammo"]
        self.rifle_damage = estats["enemy"]["e_rifle_damage"]
        self.rifle_acc = estats["enemy"]["e_rifle_accuracy_bonus"]
        self.rifle_max_ammo = estats["enemy"]["e_rifle_ammo"]
        self.pistol_ammo = self.pistol_max_ammo
        self.rifle_ammo = self.rifle_max_ammo
        self.dodge_bonus = 0
        self.punk_name = "Street Larry"

'''Set the game up'''
game = Game()
game_running = True
player_input = 5
'''Run intro'''
game.intro()
'''Give stats to players and enemies'''
player1 = game.player_name
enemy1 = Enemy(e_stats)

'''Start the actual game cycle'''
Game.instructions()
while game_running:
    Game.short_instructions()
    Game.which_attack()
