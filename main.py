from layoutlib.window import Window
from GameRunner import Core
from database import get_top_scores, send_score_to_website
from player_data import save_player_name, load_player_name

def menu():
    print("""
    .______   .______       __    ______  __  ___                               
|   _  \  |   _  \     |  |  /      ||  |/  /                               
|  |_)  | |  |_)  |    |  | |  ,----'|  '  /                                
|   _  <  |      /     |  | |  |     |    <                                 
|  |_)  | |  |\  \----.|  | |  `----.|  .  \                                
|______/  | _| `._____||__|  \______||__|\__\                               
                                                                            
.______   .______       _______     ___       __  ___  _______ .______      
|   _  \  |   _  \     |   ____|   /   \     |  |/  / |   ____||   _  \     
|  |_)  | |  |_)  |    |  |__     /  ^  \    |  '  /  |  |__   |  |_)  |    
|   _  <  |      /     |   __|   /  /_\  \   |    <   |   __|  |      /     
|  |_)  | |  |\  \----.|  |____ /  _____  \  |  .  \  |  |____ |  |\  \----.
|______/  | _| `._____||_______/__/     \__\ |__|\__\ |_______|| _| `._____|

Welcome to the Brick Breaker Game !
1- Play
2- TOP 10
3- Exit 
    """)
    while True:
        try :
            answer = int(input("Type your choice: "))
            if answer < 1 and answer > 3 :
                print("[!] Choose an option between 1 and 3 !")
            else:
                return answer
        except Exception as e:
            print("[!] Choose an option between 1 and 3")

def top10():

    print("TOP 10 Players:")

    results = get_top_scores()
    for i in range(len(results)):
        print("{}:\t{}\t{}\t{}".format(i+1, results[i][0], results[i][1], results[i][2] ))

def play():
    # Create an instance of the game environment
    game = Window(1080, 720, True, 'Break_IT')

    # Load the game engine into the game environment
    engine = Core()
    game.load_complete(engine, 'data', 'resources.dat', 'levels.dat')

    # Start the main game loop
    score = game.gInstance.main_loop()

    # Destroy the game environment and clean up resources
    game.destroy()

    # save user data
    player_name = load_player_name()
    if not player_name:
        player_name = input("[!] Enter your player name: ")
        save_player_name(player_name)
    send_score_to_website(player_name, score)

if __name__ == "__main__":
    # Entry point of the program
    choice = menu()
    if choice == 1:
        play()
    elif choice == 2:
        top10()
    else:
        exit()
