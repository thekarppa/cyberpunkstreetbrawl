import json
import random

# Open up the files for player and enemy stats, then load the flavor texts
with open("player_stats.json", "r", encoding="utf-8") as p_source:
    p_stats = json.load(p_source)
with open("enemy_stats.json", "r", encoding="utf-8") as e_source:
    e_stats = json.load(e_source)
with open("pistol_miss.txt", "r", encoding="utf-8") as pistol_misses:
    pistol_miss_flavor = pistol_misses.readlines()
    pistol_miss_amount = len(pistol_miss_flavor)


class Game:
    """Main game functions. Includes intro, attack commands and some other elements"""
    def __init__(self):
        self.choice = None
        self.p_name = ""
        self.player_name = None
        self.select_weapon= 0
        self.cover_duration = 0 # For now this is a three-turn buff. Need to set it to a game variables json later

    def intro(self):
        """Simple intro to show at the start of the game"""
        print("You are an Edgerunner and you came across a street punk…")
        self.p_name = input("What is your street name? ") or "Street Bear"
        self.player_name = Player(p_stats, self.p_name)


    @staticmethod
    def instructions():
        """Used in the intro and to easily show the combat mechanics instructions"""
        print("Use the following options to fight:")
        print("1. Attack - Choose a weapon to attack with:")
        print("Your pistol is weaker but more accurate than your rifle.")
        print("Your melee weapon is accurate, but you also expose yourself to nastier hits in melee.")
        print("2. Dodge  - You make an evasive attack, but your accuracy will be slightly hindered.")
        print("3. Cover  - Seek cover to lessen the chance of being hit fir a few turns.")
        print("4. Reload - Reload a given gun. You can only reload one gun at a time.")

    @staticmethod
    def short_instructions():
        """Shorter action menu"""
        print("1. Attack")
        print("2. Dodge")
        print("3. Cover")
        print("4. Reload")
        print("5. Instructions")
        print("6. Quit")

    @staticmethod
    def which_attack():
        """Cycling through player actions"""
        _choice = input("What do you want to do? ")
        if _choice == "1":
            print("Do you want to use your")
            print(f"1. Knife ({player1.melee["min"]} to {player1.melee["max"]} damage, often crits) for deadly close-quarters combat")
            print(f"2. Pistol ({player1.pistol["min"]} to {player1.pistol["max"]} damage, sometimes crits) for a weaker aimed shot")
            print(f"3. Rifle ({player1.rifle["min"]} to {player1.rifle["max"]} damage, rarely crits) for deadly burst fire")
            print(f"4. Back out and choose something else")
            _select_weapon = int(input("What do you want to do? ")) # Need to refactor this to accept all inputs, not just int's
            # Run through the selections and perform some actions.
            if _select_weapon == 1:
                WeaponMode.melee_attack()
            elif _select_weapon == 2:
                if player1.pistol_ammo > 0:
                    WeaponMode.pistol_attack()
                    player1.pistol_ammo -= 1
                    print(f"Your pistol has {player1.pistol_ammo}/{player1.pistol_max_ammo} shots left.")
                else:
                    _p_empty = int(input("No ammo left! Do you want to 1. Reload it or 2. do something else?"))
                    if _p_empty == 1:
                        game.chose_pistol_reload()
                    else:
                        pass
            elif _select_weapon == 3:
                WeaponMode.rifle_attack()
            elif _select_weapon == 4:
                pass
            else:
                print("No time to mess about! Make a selection!")
        elif _choice == "2":
            game.chose_dodge()
        elif _choice == "3":
            game.chose_cover()

        # Reload options: using break in the loops to go back to the main selections to not get the player
        # stuck reloading a gun; I'd rather go back to the main options, personally
        elif _choice == "4":
            print(f"Your pistol has {player1.pistol_ammo}/{player1.pistol_max_ammo} shots and\n"
            f"your rifle has {player1.rifle_ammo}/{player1.rifle_max_ammo} shots.")
            while True:
                reload_choice = input("1. Pistol 2. Rifle: ")
                try:
                    reload_choice = int(reload_choice)
                except ValueError:
                    print("Do something else?")
                    break
                if reload_choice in (1, 2):
                    game.choose_reload(reload_choice)
                    break
                else:
                    print("Do something else?")
        elif _choice == "5":
            game.instructions()
        elif _choice == "6":
            exit(0)
        else:
            Game.short_instructions()

    @staticmethod
    def chose_attack():
        """Let's deal some damage by executing an attack. Pistol-only for a placeholder"""
        WeaponMode.pistol_attack()
    @staticmethod
    def chose_dodge():
        """Dodge cycle"""
        print("Chose dodge!")
    @staticmethod
    def chose_cover():
        """Set a dodge bonus for a few turns. Need to set a "cover_duration -= 1" when
        the enemy attacks to reduce this correctly"""
        cover_duration = 3
        print("Ducking into cover!")
    def choose_reload(self, choice):
        print(f"Your pistol has {player1.pistol_ammo}/{player1.pistol_max_ammo} shots\n"
              f"and your rifle has {player1.rifle_ammo}/{player1.rifle_max_ammo} shots.")
        print("Which one do you want to reload: 1. Pistol 2. Rifle")
        if choice == 1:
            Game.chose_pistol_reload()
        elif choice == 2:
            Game.chose_rifle_reload()
        else:
            print("No time to mess about! Make a selection!")
    @staticmethod
    def chose_pistol_reload():
        print("You reload your pistol with one of the mags in your pockets.")
        player1.pistol_ammo = player1.pistol_max_ammo
        print(f"Your pistol now has {player1.pistol_ammo}/{player1.pistol_max_ammo} shots.")
    @staticmethod
    def chose_rifle_reload():
        print("You reload your rifle with one of the mags in your pockets.")
        player1.rifle_ammo = player1.rifle_max_ammo
        print(f"Your rifle now has {player1.rifle_ammo}/{player1.rifle_max_ammo} shots.")

    @staticmethod
    def player_attack(self, enemy, accuracy_total=0, dodge_total=0):
        """Making an attack roll: the simple initial idea is
            "accuracy + accuracy bonuses vs dodge + dodge bonuses" against a random 100 roll"""
        hit_chance = (player1.accuracy + accuracy_total) - (enemy.dodge + dodge_total)
        print(f"The chance to hit is {hit_chance}!")

class WeaponMode:
    """Attack modes for each weapon"""
    def __init__(self):
        pass

    @staticmethod
    def pistol_attack():
        """Run through the pistol attack code"""
        print('You chose a pistol!')

    @staticmethod
    def rifle_attack():
        """Run through the rifle attack code"""
        print('You chose a rifle!')

    @staticmethod
    def melee_attack():
        """Run through the melee attack code. Need to include the dodge penalty for going into combat"""
        print('You chose a knife!')

class Player:
    """Initialize each player with stats. In v0.1 there is only one player.
    p_stats holds the stats from the json file"""
    def __init__(self, pstats, name):
        self.max_p_hp = pstats["player"]["hp"]
        self.armor = pstats["player"]["armor"]
        self.accuracy = pstats["player"]["accuracy"]
        self.dodge = pstats["player"]["dodge"]
        melee = p_stats["player"]["melee_damage"]
        self.melee = {
            "min": melee["min"],
            "max": melee["max"],
            "crit_multiplier": melee["crit_multiplier"],
            "crit_chance": melee["crit_chance"]
        }
        self.melee_acc_bonus = pstats["player"]["melee_accuracy_bonus"]
        self.melee_acc_pen = pstats["player"]["melee_dodge_penalty"]
        pistol = p_stats["player"]["pistol_damage"]
        self.pistol = {
            "min": pistol["min"],
            "max": pistol["max"],
            "crit_multiplier": pistol["crit_multiplier"],
            "crit_chance": pistol["crit_chance"]
        }
        self.pistol_acc = pstats["player"]["pistol_accuracy_bonus"]
        self.pistol_max_ammo = pstats["player"]["pistol_ammo"]
        rifle = p_stats["player"]["rifle_damage"]
        self.rifle = {
            "min": rifle["min"],
            "max": rifle["max"],
            "crit_multiplier": rifle["crit_multiplier"],
            "crit_chance": rifle["crit_chance"]
        }
        self.rifle_acc = pstats["player"]["rifle_accuracy_bonus"]
        self.rifle_max_ammo = pstats["player"]["rifle_ammo"]
        self.pistol_ammo = self.pistol_max_ammo
        self.rifle_ammo = self.rifle_max_ammo
        self.dodge_bonus = 0
        self.runner_name = name

class Enemy:
    """Initialize enemies with stats. In v.01 there is just one enemy"""
    def __init__(self, estats):
        self.max_e_hp = estats["enemy"]["hp"]
        self.armor = estats["enemy"]["armor"]
        self.accuracy = estats["enemy"]["accuracy"]
        self.dodge = estats["enemy"]["dodge"]
        melee = e_stats["enemy"]["melee_damage"]
        self.melee = {
            "min": melee["min"],
            "max": melee["max"],
            "crit_multiplier": melee["crit_multiplier"],
            "crit_chance": melee["crit_chance"]
        }
        self.m_acc_bonus = estats["enemy"]["melee_accuracy_bonus"]
        self.m_acc_pen = estats["enemy"]["melee_dodge_penalty"]
        pistol = e_stats["enemy"]["pistol_damage"]
        self.pistol = {
            "min": pistol["min"],
            "max": pistol["max"],
            "crit_multiplier": pistol["crit_multiplier"],
            "crit_chance": pistol["crit_chance"]
        }
        self.pistol_acc = estats["enemy"]["pistol_accuracy_bonus"]
        self.pistol_max_ammo = estats["enemy"]["pistol_ammo"]
        rifle = e_stats["enemy"]["rifle_damage"]
        self.rifle = {
            "min": rifle["min"],
            "max": rifle["max"],
            "crit_multiplier": rifle["crit_multiplier"],
            "crit_chance": rifle["crit_chance"]
        }
        self.rifle_acc = estats["enemy"]["rifle_accuracy_bonus"]
        self.rifle_max_ammo = estats["enemy"]["rifle_ammo"]
        self.pistol_ammo = self.pistol_max_ammo
        self.rifle_ammo = self.rifle_max_ammo
        self.dodge_bonus = 0
        self.punk_name = "Street Larry"

# Set the game up
game = Game()
game_running = True
player_input = 5

game.intro() # Run intro

player1 = game.player_name # Give stats to players and enemies
enemy1 = Enemy(e_stats)

# Start the actual game cycle
Game.instructions()
while game_running:
    Game.short_instructions()
    Game.which_attack()