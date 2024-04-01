# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 02:10:36 2024

@author: Fernando
"""

# Libraries
import random

# Score of wins
user_wins = 0
computer_wins = 0

# List of options
options = ["rock", "paper", "scissors"]

# We ask the user to choose Rock, Paper or Scissors
while True:
    x = input("Type Rock/Paper/Scissors or Q to quit: ").lower()
    if x == "q":
        break
    if x not in options:
        continue
    # This is the pick of the computer
    r = random.randint(0, 2)
    y = options[r]
    print("Computer picked",y+".")
    # We verify who won
    if x == "rock" and y == "scissors":
        print("You won!")
        user_wins += 1
    elif x == "paper" and y == "rock":
        print("You won!")
        user_wins += 1
    elif x == "scissors" and y == "paper":
        print("You won!")
        user_wins += 1
    else:
        print("You lost.")
        computer_wins += 1
    
print("You won", user_wins, "times.")
print("The computes won", computer_wins, "times.")
print("Goodbye!")
