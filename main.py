from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

#Implement level system and save file with JSON file, experience points


# Create black magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 14, 1400, "black")

#Create White Magic
cure = Spell("Cure", 32, 620, "white")
cura = Spell("Cura", 40, 1500, "white")

#Create some items
potion = Item("Potion", "potion", "Heals for 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals for 100 HP", 100)
superpotion= Item("Super-Potion", "potion", "Heals for 1000 HP", 1000)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP of party member", 9999)
hielixir = Item("MegaElixir", "elixir", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Hits for 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spells = [fire, meteor, cure]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                 {"item": superpotion, "quantity": 5}, {"item": elixir, "quantity": 5},
                 {"item": hielixir, "quantity": 2}]

#Instantiate People
player1 = Person( "MUNDA :" , 3260, 132, 300, 34, player_spells, player_items)
player2 = Person( "Gizz  :" , 4150, 188, 311, 34, player_spells, player_items)#calling on the Person Class
player3 = Person( "Ruben :" , 3089, 174, 288, 34, player_spells, player_items)#calling on the Person Class


enemy1 = Person("PENCE   " , 1250, 130, 560, 325, enemy_spells, [])#calling on the Person Class
enemy2 = Person("TRUMP   " , 18200, 701, 525, 25, enemy_spells, [])#calling on the Person Class
enemy3 = Person("SESSIONS" , 1250, 130, 560, 325, enemy_spells, [])#calling on the Person Class


players = [player1, player2, player3 ]
enemies = [enemy1, enemy2, enemy3]
#calling on the Person Class


running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

# Battle Sequence between Party and Enemy
while running:
    print("===========================")
    print("\n\n")
    print("NAME               HP                                    MP")
    for player in players:
        player.get_stats()

    print("\n")
    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:

        #Choose what player wants to do (Attack, Magic, Items)
        player.choose_action()
        choice = input("    Choose action: ")
        index = int(choice) - 1

        #If player attacks
        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print(player.name.replace(":", "") + "attacked " + enemies[enemy].name.replace(" ", "")  + "for", dmg, " points of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died")
                del enemies[enemy]


            #If Player chooses Magic
        elif index == 1:
            player.choose_magic()

            magic_choice =int(input("    Choose magic:")) - 1

            #Return to menu
            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            #Healing Spells
            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), " HP" +bcolors.ENDC)

            #Damage Spells
            elif spell.type == "black":#damage spells
                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(magic_dmg)

                print (bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died")
                    del enemies[enemy]

        elif index == 2:
            player.choose_items()
            item_choice = int(input("    Choose Item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue
            player.items[item_choice]["quantity"] -= 1

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for ", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixir":

                if item.name == "MegaElixir":
                    for member in players:
                        member.hp = member.maxhp
                        member.mp = member.maxmp
                else:
                    player.hp = playe
                    player.mp = player.maxmp

                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)

                print(bcolors.FAIL + " \n" + item.name + " deals", str(item.prop), " points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died")
                    del enemies[enemy]

    #Check if battle is over
    defeated_enemies = 0
    defeated_players = 0

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1
    #Check if Player Won
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You Win!" + bcolors.ENDC)
        running = False

    #Check if Enemy Won
    elif defeated_players == 2:
        print(bcolors.FAIL + "Your enemies have defeated you!" + bcolors.ENDC)
        running = False
    #Enemy Attack Phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 3)
        #Choose Attack
        if enemy_choice == 0:
            target = random.randrange(0, 3)
            enemy_dmg = enemy.generate_damage()

            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ", "") + " attacks " + players[target].name.replace(" ", "") + "for:", enemy_dmg)

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            # Healing Spells
            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals " + enemy.name + " for", str(magic_dmg), " HP" + bcolors.ENDC)

            # Damage Spells
            elif spell.type == "black":  # damage spells

                target = random.randrange(0, 3)

                players[target].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "") + "'s " + spell.name + " deals", str(magic_dmg),
                      "points of damage to " + player[target].name.replace(" ", "") + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(player[target].name.replace(" ", "") + " has died")
                    del player[target]