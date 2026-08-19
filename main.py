import json
import random
import time

# Open up the files for player and enemy stats, then load the flavor texts
with open("player_stats.json", "r", encoding="utf-8") as p_source:
    p_stats = json.load(p_source)
with open("enemy_stats.json", "r", encoding="utf-8") as e_source:
    e_stats = json.load(e_source)
with open("pistol_miss.txt", "r", encoding="utf-8") as f:
    pistol_miss_flavor = [
        line.strip().replace("\\n", "\n")
        for line in f
        if line.strip()
    ]
# Remember to use
# print(random.choice(pistol_miss_flavor))
# to choose a random quote

# Cybernetics for future use: player gets to choose one as part of "character creation". Will add this later
with open("cybernetics.json", "r", encoding="utf-8") as cybernetics_gear:
    cybernetics = json.load(cybernetics_gear)

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

    @staticmethod
    def instructions():
        """Used in the intro and to easily show the combat mechanics instructions"""
        print("Use the following options to fight:")
        print("1. Attack - Choose a weapon to attack with.")
        print("      Your melee weapon is accurate, but you also expose yourself to nastier hits in melee.")
        print("      Your pistol is weaker but more accurate than your rifle and deals meaner critical hits.")
        print("      Your rifle does more damage but crits less often than your pistol.")
        print("2. Dodge  - You make an evasive attack, but your accuracy will be slightly hindered.")
        print("3. Cover  - Seek cover to lessen the chance of being hit fir a few turns.")
        print("4. Reload - Reload a given gun. You can only reload one gun at a time.")
        print("5. Show these instructions.")
        print("6. Display current stats.")
        print("7. Exit game. Thanks for playing!")

    @staticmethod
    def short_instructions():
        """Shorter action menu"""
        print("1. Attack")
        print("2. Dodge")
        print("3. Cover")
        print("4. Reload")
        print("5. Detailed instructions")
        print("6. Stats")
        print("7. Quit")

    @staticmethod
    def game_status():
        print("Current situation:")
        print(f'You have {player1.current_hp} HP and the punk has {enemy1.current_hp} HP.')
        print(f'You have {player1.armor}-strength armor and the punk has {enemy1.armor} armor.')
        print(f'Your pistol has {player1.pistol_ammo}/{player1.pistol_max_ammo} and your rifle has {player1.rifle_ammo}/{player1.rifle_max_ammo} shots.')
        # Give some flavour text based o nthe enemy HP. This also has a hidden "run away" effect for really low-level enemies
        if enemy1.current_hp <= (enemy1.max_e_hp // 0.75):
            print('The punk looks like they are not backing down!')
        elif enemy1.current_hp <= (enemy1.max_e_hp // 0.5):
            print('The punk looks hurt, but still determined to rob you!')
        elif enemy1.current_hp <= enemy1.current_hp >= (enemy1.max_e_hp // 0.25):
            print('The punk looks hurt and regretting their choice to attack you.')
        elif enemy1.current_hp <= (enemy1.max_e_hp // 0.15):
            print('Bruised and bleeding, the punk looks just about ready to run! You can do this!')
        elif enemy1.current_hp < (enemy1.max_e_hp // 0.1):
            print('The punk is in such bad shape that they decide that this is not worth their life!')
            enemy1.current_hp = 0

    @staticmethod
    def which_attack():
        """Cycling through player actions"""
        print(f'You currently have {player1.current_hp} and your enemy has {enemy1.current_hp} HP.')
        print(f'Your pistol has {player1.pistol_ammo}/{player1.pistol_max_ammo} and your rifle has {player1.rifle_ammo}/{player1.rifle_max_ammo} shots.')
        Game.short_instructions()
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
        # stuck reloading a gun; I'd personally rather go back to the main options than have a forced choice
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
            game.game_status()
        elif _choice == "7":
            print("Thank you for your time and for playing my silly game!")
            print("You will disconnect and return to reality in a few seconds.")
            time.sleep(4)
            exit(0)
        else:
            pass

    @staticmethod
    def chose_attack():
        """Let's deal some damage by executing an attack. Pistol for testing purposes."""
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
    def win_loss():
        if player1.current_hp <= 0:
            print('You are too injured to keep fighting and the punk snags your wallet. You lost this time. Time for some new chrome?')
        elif enemy1.current_hp <= 0:
            print(f'{enemy1.punk_name} lies before you, injured and unconscious. You win!')
        elif player1.current_hp <= 0 and enemy1.current_hp <= 0:
            print(f"You and {enemy1.punk_name} both are sitting opposite to eachother, panting and leaning on something.\nYou both decide that this isn't worth it and limp away into the night to lick your wounds.")
        elif player1.current_hp > 0 and enemy1.current_hp > 0:
            print("This isn't over yet!")
        else:
            print('Something weird seems to have happened. Exiting to real life!')
            exit(0)

    @staticmethod
    def hit_location():
        """A simple location randomizer to add to hit rolls for flavour"""
        _hit_roll = random.randrange(1, 6)
        if _hit_roll == 1:
            return "chest"
        elif _hit_roll == 2:
            return "left arm"
        elif _hit_roll == 3:
            return "right arm"
        elif _hit_roll == 4:
            return "left leg"
        elif _hit_roll == 5:
            return "right leg"
        elif _hit_roll == 6:
            return "head"
        else:
            return None

class WeaponMode:
    """Attack modes for each weapon"""
    def __init__(self):
        pass

    @staticmethod
    def pistol_attack():
        """Run through the pistol attack code"""
        print('You chose to shoot with your pistol! Your pistol snaps a shot off and...')
        WeaponMode.hit_roll('pistol')
        player1.pistol_ammo -= 1
        if (random.randrange(1, 100) + player1.pistol_acc) < (enemy1.dodge + enemy1.dodge_bonus):
            print(f"You hit {enemy1.punk_name} with your pistol in the {game.hit_location}!")
        else:
            _hit_or_noeffect = random.randrange(1, 10)
            print(random.choice(pistol_miss_flavor))

    @staticmethod
    def rifle_attack():
        """Run through the rifle attack code"""
        print('You chose a rifle!')

    @staticmethod
    def melee_attack():
        """Run through the melee attack code. Need to include the dodge penalty for going into combat"""
        print('You chose a knife!')

    @staticmethod
    def hit_roll(attack_mode):
        """Making an attack roll: the simple initial idea is
            "accuracy + accuracy bonuses vs dodge + dodge bonuses" against a random 100 roll"""
        _accuracy_add = 0
        if attack_mode == 'melee':
            _accuracy_add = player1.melee_acc_bonus
        elif attack_mode == 'pistol':
            _accuracy_add = player1.pistol_acc
        elif attack_mode == 'rifle':
            _accuracy_add = player1.rifle_acc
        else:
            print('Need the proper attack mode.')
        hit_chance = (player1.accuracy + _accuracy_add) - (enemy1.dodge + enemy1.dodge_bonus)
        print(f"The chance to hit is {hit_chance}%!")

class Player:
    """Initialize each player with stats. In v0.1 there is only one player.
    p_stats holds the stats from the json file"""
    def __init__(self, pstats, name):
        self.max_p_hp = pstats["player"]["hp"]
        self.current_hp = self.max_p_hp
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
    def __init__(self, estats, punk_name='Street Larry'):
        self.max_e_hp = estats["enemy"]["hp"]
        self.current_hp = self.max_e_hp
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
        self.punk_name = punk_name

# Set the game up
game = Game()
game_running = True
player_input = 5 # Set the default choice to 5 to display detailed instructions for the game start

game.intro() # Run intro

player1 = Player(p_stats, game.p_name) # Give stats to players and enemies
enemy1 = Enemy(e_stats, "Robber Larry")

# The actual game loop: run while there is any HP left
print(f'You, {player1.runner_name}, were on your way home and are about to be mugged by {enemy1.punk_name}. Teach them a lesson!')
Game.instructions()

# Inside jokes about some of my friends characters
if player1.runner_name == "Hamfist": # My favourite Cyberpunk RED character I've made
    player1.melee_acc_bonus += 10
    print("Your hamfisted approach might work here...")
elif player1.runner_name == "Sticky":
    player1.dodge_bonus += 10
    print("Time to DEAL some damage.")
elif player1.runner_name == "Grim":
    player1.melee["min"] += 10
    player1.melee["max"] += 10
    print("That linear frame is doing it's work.")
elif player1.runner_name == "Trigger":
    player1.rifle_acc += 10
    print("Good thing you practiced using your sniper at closer ranges...")
elif player1.runner_name == "Viejo":
    player1.rifle["max"] += random.randrange(10, 25)
    print("Your experimental rifle makes a humming sound as it warms up...")
elif player1.runner_name == "Scribe":
    player1.pistol_acc += 10
    print("Your two pistols are sometimes your press pass.")
else:
    pass

while game_running:
    if player1.current_hp <= 0 or enemy1.current_hp <= 0:
        game_running = False
    Game.which_attack()

# Game ends. Print the winner and thank the player for playing! Show a fancy exit sequence, too!
game.win_loss()
print("Thank you for your time and for playing my silly game!")
print("You will disconnect and return to reality in a few seconds.")
time.sleep(4)
exit(0)