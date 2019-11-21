from GameFunctions import *
from GameClasses import *

# Game welcome and setup deck and player balance
print("Welcome to my text based Black Jack Game")
player_bal = PlayerBalance()

# Execute game round
round_cycle(player_bal)

# End game message
print("Thank you for playing my Black Jack game")
