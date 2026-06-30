import random

def play_guessing_game():
    print("====================================")
    print("🎯 WELCOME TO THE NUMBER GUESSING GAME 🎯")
    print("====================================")
    
    # 1. Define bounds and parameters
    lower_bound = 1
    upper_bound = 100
    max_attempts = 7
    
    # 2. Generate the secret random number
    secret_number = random.randint(lower_bound, upper_bound)
    attempts = 0
    
    print(f"\nI'm thinking of a number between {lower_bound} and {upper_bound}.")
    print(f"You have exactly {max_attempts} attempts to crack it. Good luck!\n")
    
    # 3. Game loop
    while attempts < max_attempts:
        # Prompt user for input
        user_input = input(f"Attempt {attempts + 1}/{max_attempts} | Enter your guess: ").strip()
        
        # 4. Robust input validation
        try:
            guess = int(user_input)
        except ValueError:
            print("❌ Invalid input! Please type a whole number.\n")
            continue
            
        # Check if the guess is out of bounds
        if guess < lower_bound or guess > upper_bound:
            print(f"⚠ Out of bounds! Your guess must be between {lower_bound} and {upper_bound}.\n")
            continue
            
        # Increment the attempt counter only after a valid guess
        attempts += 1
        
        # 5. Core game logic checking
        if guess == secret_number:
            print(f"\n🎉 CONGRATULATIONS! You guessed it right!")
            print(f"🏆 The secret number was {secret_number}.")
            print(f"📊 It took you {attempts} attempt(s).\n")
            return  # End the function/game early on victory
        elif guess < secret_number:
            print("📉 Too low! Try a higher number.\n")
        else:
            print("📈 Too high! Try a lower number.\n")
            
    # 6. Out of attempts (Game Over condition)
    print("------------------------------------")
    print("💀 GAME OVER! You ran out of attempts.")
    print(f"The correct number was: {secret_number}")
    print("Better luck next time! 🕹")
    print("------------------------------------")

# Execute the game
if __name__ == "__main__":
    play_guessing_game()
