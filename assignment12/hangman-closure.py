# Task 4
def make_hangman(secret_word):
    """Creates a closure for the Hangman game."""
    guesses = []

    def hangman_closure(letter):
        """Handles each guess and updates the word display."""
        if letter in guesses:
            print(f"You already guessed '{letter}'. Try again.")
            return False

        guesses.append(letter)
        result = "".join([char if char in guesses else "_" for char in secret_word])
        print(result)

        not_guessed = [ch for ch in secret_word if ch not in guesses]
        print("Not guessed yet:", not_guessed)
        return not not_guessed

    return hangman_closure

def play_again():
    """This function returns True if the player wants to play again; otherwise, it returns False."""
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')

if __name__ == "__main__":
    secret_word = input("Enter the secret word: ").lower()
    hangman = make_hangman(secret_word)
    missed_guesses = 0
    max_misses = 10
    parts = ["Base", "Upright pole", "Top beam", "Rope", "Head", "Body", "Left arm", "Right arm", "Left leg", "Right leg"]

    while True:
        guess = input("Guess a letter: ").lower()
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter.")
            continue

        if guess not in secret_word:
            missed_guesses += 1
            print(f"Wrong guess! Missed guesses: {missed_guesses}/{max_misses} — {parts[missed_guesses - 1]} added.")

        if hangman(guess):
            print("Congratulations! You guessed the word.")
            break

        if missed_guesses >= max_misses:
            print(f"💀 Game Over! The word was '{secret_word}'. Better luck next time.")
            if not play_again():
                break
            else:
                # Reset the game
                secret_word = input("Enter the secret word: ").lower()
                hangman = make_hangman(secret_word)
                missed_guesses = 0
