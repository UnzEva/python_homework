def make_hangman(secret_word):
    guesses = []

    def hangman_closure(letter):
        guesses.append(letter)
        display = ''

        all_guessed = True
        for ch in secret_word:
            if ch in guesses:
                display += ch
            else:
                display += '_'
                all_guessed = False

        print(display)
        return all_guessed

    return hangman_closure


secret = input("Enter the secret word: ")

# print("\n" * 50)

# Game
play = make_hangman(secret)

print("Let's play Hangman!\n")
guessed = False

while not guessed:
    guess = input("Guess a letter: ")
    if len(guess) != 1:
        print("Please enter a single letter.")
        continue
    guessed = play(guess)

print("Congratulations! You guessed the word.")