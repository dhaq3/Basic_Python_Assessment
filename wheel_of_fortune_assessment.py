import random
import string
import csv

round1word = 'abyss'
round2word = 'axiom'
round3word = 'xylophone'

global turn
global bank
global end_round
global wheel
global word1sofar
global endGuess
global playerList

word1sofar = []
word2sofar = []
word3sofar = []

endGuess = False
turn = 0
bank = [0,0,0]
end_round = False

wheel = [(50*i+100) for i in range(22)]

wheel.append('bankrupt')
wheel.append('lose a turn')
for i in range(17,22):
    wheel[i] -= 500

playerList = []

def GameStart():
    global playerList
    print("Welcome to Wheel of Fortune! Please begin by entering a name or alias.")
    print('-----------------------------------------------------------------------')
    player1 = str(input("Enter player ones name/alias (is given first turn): "))
    player2 = str(input("Enter player twos name/alias (is given second turn): "))
    player3 = str(input("Enter player threes name/alias (is given third turn): "))
    playerList.append(player1)
    playerList.append(player2)
    playerList.append(player3)
    print(playerList)
    print('---------------------------------------')
    print('We will now begin round 1.')
    print('-------------------------------------------------------------------------')

def round1():
    global turn
    global bank
    global end_round
    global word1sofar
    print('To begin round one player one must spin the wheel.')
    print('-----------------------------------------------------')
    for i in range(len(round1word)):
        word1sofar.append('_')
    while not end_round:
        print('current turn: %i' % turn)
        print("So far the word is: %s" % "".join(word1sofar))
        print('---------------------------------------------------')
        PlayerConfirmation = str(input("Are you ready to spin the wheel %s? [y/n]: " % playerList[turn % 3])).lower().strip()
        if PlayerConfirmation == 'y':
            print("Good luck %s!" % playerList[turn % 3])
            print('---------------------------')
            spin_wheel()
        elif PlayerConfirmation == 'n':
            print("Tough Luck you're spinning it anyways %s!" % playerList[turn % 3])
            print('---------------------------------------')
            spin_wheel()

def spin_wheel():
    global turn
    global bank
    global wheel
    global wheel_selection
    wheel_selection = random.choice(wheel)
    print('You landed on', ':', wheel_selection)
    print('-----------------------------------')
    if wheel_selection == 'bankrupt':
        print("That sucks! You lose your turn and money %s." % playerList[turn % 3])
        print('----------------------------')
        bank[turn % 3] = 0
        turn += 1
    elif wheel_selection == 'lose a turn':
        print("That sucks! You lose your turn %s." % playerList[turn % 3])
        print('----------------------------')
        turn += 1
    else:
        print("Good job %s! You may now guess the word or pick a consonant" % playerList[turn % 3])
        guess()

def consonantCounter(word):
    NumConsonants = 0
    for letter in word:
        if letter not in 'aeiou' and letter != '_':
            NumConsonants += 1
    return NumConsonants

def BuyVowel():
    global turn
    global bank
    global end_round
    while True:
        vowelChoice = str(input('Which vowel would you like to %s, alternatively you may enter "q" if you have changed '
                            'your mind? [a,e,i,o,u]: ' % playerList[turn % 3])).lower().strip()
        if len(vowelChoice) == 1 and vowelChoice in 'aeiou':
            break
        elif vowelChoice == 'q':
            break
        else:
            print("Please input a valid choice.")
    if vowelChoice == 'q':
        print('You have now ended your turn %s.' % playerList[turn % 3])
        print('--------------------------------------')
        turn += 1
    else:
        bank[turn % 3] -= 250
        if vowelChoice in round1word:
            for i in range(len(round1word)):
                if list(round1word)[i] == vowelChoice:
                    word1sofar[i] = vowelChoice
            if ''.join(word1sofar) == round1word:
                print("Good work you got it %s! The word was %s." % (playerList[turn % 3], round1word))
                end_round = True
                turn += 1
            else:
                print("Good work %s you got a vowel! You may continue buying vowels, guess the word, or end your turn." % playerList[turn % 3])
                print("--------------------------------------------")
                print("Please keep in mind that if you have less than 250 in the bank and you select 'buy' your turn "
                      "will also end automatically.")
                print('----------------------------------------------------------------------------------')
                print("%s, your current bank is: %i" % (playerList[turn % 3], bank[turn % 3]))
                print('-----------------------------------------------------------------------------------------')
                choice = str(input('Which would you like to do? [buy, guess, end]: ')).lower().strip()
                if choice == 'buy' and bank[turn % 3] > 250:
                    print('-----------------------------------')
                    BuyVowel()
                elif choice == 'guess':
                    print('----------------------------------')
                    wordGuess = str(input('Please enter your full guess here keeping in mind that the word so far is '
                                          '%s: ' % ''.join(word1sofar))).lower().strip()
                    if wordGuess == round1word:
                        print('-------------------------------------------------------------------------')
                        print("Good work you got it %s! The word was %s. The round is now over." % (playerList[turn % 3], round1word))
                        end_round = True
                        turn += 1
                    else:
                        print('Your guess was incorrect! Your turn is now over %s.' % playerList[turn % 3])
                        turn += 1
                else:
                    print('Your turn is now over %s.' % playerList[turn % 3])
                    turn += 1
        else:
            print("That's unfortunate %s but that vowel was not in the word, your turn is now over." % playerList[turn % 3])
            turn += 1
    print('----------------------------------------------------------------------------------')

def guess():
    global turn
    global bank
    global end_round
    global endGuess
    global word1sofar
    endGuess = False
    if consonantCounter(round1word) == consonantCounter("".join(word1sofar)):
        print('----------------------------------------------')
        print('Good work everyone there are no more consonants left! You may now only buy vowels.')
        print('If you do not have enough in the bank to buy a vowel your turn will be skipped. Alternatively you may '
              'also skip your turn.')
        print('------------------------------------------------------------------------------------------------')
        buyAvowel = str(input('Would you like to buy a vowel %s? [y/n]: ' % playerList[turn % 3])).lower().strip()
        if buyAvowel == 'y':
            if bank[turn % 3] < 250:
                print("Sorry you don't actually have enough to buy a vowel %s. Your turn is now over." % playerList[turn % 3])
                turn += 1
            else:
                BuyVowel()
        else:
            print('Your turn is now over %s.' % playerList[turn % 3])
            turn += 1
    else:
        while not endGuess:
            print('---------------------')
            print("So far the word is: %s" % "".join(word1sofar))
            print('---------------------------')
            UserGuess = str(input("Guess a consonant or word %s:" % playerList[turn % 3])).lower().replace(" ", "")
            if len(UserGuess) == 0:
                print("Please enter a word or letter $s." % playerList[turn % 3])
                continue
            elif len(list(UserGuess)) > len([i for i in UserGuess if i in string.ascii_lowercase]):
                print('Try again, but input a word or consonant this time %s.' % playerList[turn % 3])
                continue
            elif len(UserGuess) == 1 and UserGuess in 'aeiou':
                print("You may not guess a vowel yet! Try again.")
                continue
            elif len(UserGuess) > 1 and UserGuess == round1word:
                print("Good work you got it %s! The round is now over." % playerList[turn % 3])
                end_round = True
                bank[turn % 3] += wheel_selection
                turn += 1
                break
            elif len(UserGuess) == 1 and UserGuess not in round1word:
                print("Tough luck bud, that consonant was not in the word! You will not receive money for this spin :( ")
                turn += 1
                break
            elif len(UserGuess) == 1 and UserGuess in round1word:
                bank[turn % 3] += wheel_selection
                for i in range(len(list(round1word))):
                    if list(round1word)[i] == UserGuess:
                        word1sofar[i] = UserGuess
                if ''.join(word1sofar) == round1word:
                    print("Good work you got it! The word was %s." % round1word)
                    end_round = True
                    endGuess = True
                    turn += 1
                else:
                    print('Good work you got a consonant %s! you may now end your turn or buy a vowel.' % playerList[turn % 3])
                    print('------------------------------------------------------------------------------')
                    PlayerChoice = str(input('Would you like to buy a vowel %s (Choosing no results in ending your '
                                             'turn)? [y/n]: ' % playerList[turn % 3])).strip().lower()
                    if PlayerChoice == 'y':
                        if bank[turn % 3] < 250:
                            print("Sorry you don't actually have enough to buy a vowel %s. Your turn is now over." % playerList[turn % 3])
                            endGuess = True
                            turn += 1
                        else:
                            BuyVowel()
                            endGuess = True
                    else:
                        endGuess = True
                        turn += 1

def round2():
    global turn
    global bank
    global end_round
    global word2sofar
    print('--------------------------------------------------------')
    print("It's time for round 2!")
    print('-----------------------------------------------------')
    for i in range(len(round2word)):
        word2sofar.append('_')
    while not end_round:
        print('current turn: %i' % turn)
        print("So far the word is: %s" % "".join(word2sofar))
        print('---------------------------------------------------')
        PlayerConfirmation = str(
            input("Are you ready to spin the wheel %s? [y/n]: " % playerList[turn % 3])).lower().strip()
        if PlayerConfirmation == 'y':
            print("Good luck %s!" % playerList[turn % 3])
            print('---------------------------')
            spin_wheel_2()
        elif PlayerConfirmation == 'n':
            print("Tough Luck you're spinning it anyways %s!" % playerList[turn % 3])
            print('---------------------------------------')
            spin_wheel_2()

def spin_wheel_2():
    global turn
    global bank
    global wheel
    global wheel_selection
    wheel_selection = random.choice(wheel)
    print('You landed on', ':', wheel_selection)
    print('-----------------------------------')
    if wheel_selection == 'bankrupt':
        print("That sucks! You lose your turn and money %s." % playerList[turn % 3])
        print('----------------------------')
        bank[turn % 3] = 0
        turn += 1
    elif wheel_selection == 'lose a turn':
        print("That sucks! You lose your turn %s." % playerList[turn % 3])
        print('----------------------------')
        turn += 1
    else:
        print("Good job %s! You may now guess the word or pick a consonant" % playerList[turn % 3])
        guess2()

def guess2():
    global turn
    global bank
    global end_round
    global endGuess
    global word2sofar
    endGuess = False
    if consonantCounter(round2word) == consonantCounter("".join(word2sofar)):
        print('----------------------------------------------')
        print('Good work everyone there are no more consonants left! You may now only buy vowels.')
        print('If you do not have enough in the bank to buy a vowel your turn will be skipped. Alternatively you may '
              'also skip your turn.')
        print('------------------------------------------------------------------------------------------------')
        buyAvowel = str(input('Would you like to buy a vowel %s? [y/n]: ' % playerList[turn % 3])).lower().strip()
        if buyAvowel == 'y':
            if bank[turn % 3] < 250:
                print("Sorry you don't actually have enough to buy a vowel %s. Your turn is now over." % playerList[
                    turn % 3])
                turn += 1
            else:
                BuyVowel2()
        else:
            print('Your turn is now over %s.' % playerList[turn % 3])
            turn += 1
    else:
        while not endGuess:
            print('---------------------')
            print("So far the word is: %s" % "".join(word2sofar))
            print('---------------------------')
            UserGuess = str(input("Guess a consonant or word %s:" % playerList[turn % 3])).lower().replace(" ", "")
            if len(UserGuess) == 0:
                print("Please enter a word or letter $s." % playerList[turn % 3])
                continue
            elif len(list(UserGuess)) > len([i for i in UserGuess if i in string.ascii_lowercase]):
                print('Try again, but input a word or consonant this time %s.' % playerList[turn % 3])
                continue
            elif len(UserGuess) == 1 and UserGuess in 'aeiou':
                print("You may not guess a vowel yet! Try again.")
                continue
            elif len(UserGuess) > 1 and UserGuess == round2word:
                print("Good work you got it %s! The round is now over." % playerList[turn % 3])
                end_round = True
                bank[turn % 3] += wheel_selection
                turn += 1
                break
            elif len(UserGuess) == 1 and UserGuess not in round2word:
                print(
                    "Tough luck bud, that consonant was not in the word! You will not receive money for this spin :( ")
                turn += 1
                break
            elif len(UserGuess) == 1 and UserGuess in round2word:
                bank[turn % 3] += wheel_selection
                for i in range(len(list(round2word))):
                    if list(round2word)[i] == UserGuess:
                        word2sofar[i] = UserGuess
                if ''.join(word2sofar) == round1word:
                    print("Good work you got it! The word was %s." % round2word)
                    end_round = True
                    endGuess = True
                    turn += 1
                else:
                    print('Good work you got a consonant %s! you may now end your turn or buy a vowel.' % playerList[
                        turn % 3])
                    print('------------------------------------------------------------------------------')
                    PlayerChoice = str(input('Would you like to buy a vowel %s (Choosing no results in ending your '
                                             'turn)? [y/n]: ' % playerList[turn % 3])).strip().lower()
                    if PlayerChoice == 'y':
                        if bank[turn % 3] < 250:
                            print("Sorry you don't actually have enough to buy a vowel %s. Your turn is now over." %
                                  playerList[turn % 3])
                            endGuess = True
                            turn += 1
                        else:
                            BuyVowel2()
                            endGuess = True
                    else:
                        endGuess = True
                        turn += 1

def BuyVowel2():
    global turn
    global bank
    global end_round
    while True:
        vowelChoice = str(input('Which vowel would you like to %s, alternatively you may enter "q" if you have changed '
                                'your mind? [a,e,i,o,u]: ' % playerList[turn % 3])).lower().strip()
        if len(vowelChoice) == 1 and vowelChoice in 'aeiou':
            break
        elif vowelChoice == 'q':
            break
        else:
            print("Please input a valid choice.")
    if vowelChoice == 'q':
        print('You have now ended your turn %s.' % playerList[turn % 3])
        print('--------------------------------------')
        turn += 1
    else:
        bank[turn % 3] -= 250
        if vowelChoice in round2word:
            for i in range(len(round2word)):
                if list(round2word)[i] == vowelChoice:
                    word2sofar[i] = vowelChoice
            if ''.join(word2sofar) == round2word:
                print("Good work you got it %s! The word was %s." % (playerList[turn % 3], round1word))
                end_round = True
                turn += 1
            else:
                print(
                    "Good work %s you got a vowel! You may continue buying vowels, guess the word, or end your turn." %
                    playerList[turn % 3])
                print("--------------------------------------------")
                print("Please keep in mind that if you have less than 250 in the bank and you select 'buy' your turn "
                      "will also end automatically.")
                print('----------------------------------------------------------------------------------')
                print("%s, your current bank is: %i" % (playerList[turn % 3], bank[turn % 3]))
                print('-----------------------------------------------------------------------------------------')
                choice = str(input('Which would you like to do? [buy, guess, end]: ')).lower().strip()
                if choice == 'buy' and bank[turn % 3] > 250:
                    print('-----------------------------------')
                    BuyVowel()
                elif choice == 'guess':
                    print('----------------------------------')
                    wordGuess = str(input('Please enter your full guess here keeping in mind that the word so far is '
                                          '%s: ' % ''.join(word2sofar))).lower().strip()
                    if wordGuess == round2word:
                        print('-------------------------------------------------------------------------')
                        print("Good work you got it %s! The word was %s. The round is now over." % (
                        playerList[turn % 3], round2word))
                        end_round = True
                        turn += 1
                    else:
                        print('Your guess was incorrect! Your turn is now over %s.' % playerList[turn % 3])
                        turn += 1
                else:
                    print('Your turn is now over %s.' % playerList[turn % 3])
                    turn += 1
        else:
            print("That's unfortunate %s but that vowel was not in the word, your turn is now over." % playerList[
                turn % 3])
            turn += 1
    print('----------------------------------------------------------------------------------')


def round3():
    global word3sofar
    global max_value_index
    print("It's time for round 3!")
    print('------------------------------------')
    print('Round three can only be played by the winner of the first two rounds.')
    print('----------------------------------------------------------------------')
    print('The winner is the person with the most amount of money earned in the previous two rounds.')
    print('-----------------------------------------------------------------------------------------')
    max_value = max(bank)
    max_value_index = bank.index(max_value)
    print('In this case that would happen to be %s.' % playerList[max_value_index])
    print('-----------------------------------------------------------------------')
    print("Congratulations %s! I hope you're ready." % playerList[max_value_index])
    print("-----------------------------------------------------------------------")
    print("For this last round you will not be spinning the wheel as we do not want you going bankrupt or losing your "
          "only turn for this round.")
    print('---------------------------------------------------------------------------------------------------------')
    print("For this final round the letters R-S-T-L-N and E will be revealed immediately and you will have the "
          "opportunity to guess three more consonants and a vowel for free!")
    print('---------------------------------------------------------------------------------------------------------')
    for i in range(len(round3word)):
        word3sofar.append('_')
    for letter in 'rstlne':
        for i in range(len(word3sofar)):
            if letter == round3word[i]:
                word3sofar[i] = letter
    print("With R-S-T-L-N-E, revealed the word you must guess correctly is: %s" % ''.join(word3sofar))
    guess3()

def guess3():
    print('----------------------------------------------')
    print('To begin please enter your three consonant and vowel guesses below:')
    while True:
        FirstConsonant = str(input("Choose a consonant: ")).lower().strip()
        SecondConsonant = str(input("Choose another consonant: ")).lower().strip()
        ThirdConsonant = str(input("Choose your final consonant: ")).lower().strip()
        vowelguess = str(input("choose a vowel: ")).lower().strip()
        print('--------------------------------------------------------------------------------------------')
        if len(FirstConsonant) + len(SecondConsonant) + len(ThirdConsonant) + len(vowelguess) != 4:
            print('Enter in single letters for your guesses and try again!')
            continue
        elif (FirstConsonant in 'aeiou') or (SecondConsonant in 'aeiou') or (ThirdConsonant in 'aeiou'):
            print('You must enter a consonant when prompted for a consonant! Try again.')
            continue
        elif vowelguess not in 'aeiou':
            print('You must guess a vowel when prompted for one! Try again.')
            continue
        elif (FirstConsonant not in string.ascii_lowercase) or (SecondConsonant not in string.ascii_lowercase) or (ThirdConsonant not in string.ascii_lowercase) or (vowelguess not in string.ascii_lowercase):
            print('You must enter a letter when prompted for your guesses! Try again.')
            continue
        else:
            break
    guessesL = [FirstConsonant, SecondConsonant, ThirdConsonant, vowelguess]
    for letter in guessesL:
        for i in range(len(word3sofar)):
            if letter == round3word[i]:
                word3sofar[i] = letter
    print("Using your consonants and vowel, %s, the word is now %s" % (playerList[max_value_index], ''.join(word3sofar)))
    print('------------------------------------------------------------------------------------------------------------')
    print("You must now guess your final answer for the word")
    print('------------------------------------------------------------')
    valid = False
    while not valid:
        FinalGuess = str(input("Enter in the word you think it is %s: " % playerList[max_value_index])).lower().strip()
        invalidity_counter = 0
        for i in FinalGuess:
            if i not in string.ascii_lowercase:
                invalidity_counter += 1
        if invalidity_counter != 0:
            print('You must enter a word without any special charecters!')
        else:
            valid = True
    if FinalGuess == round3word:
        print("Congratulations %s! You've won the final round and will walk away with %i dollars." % (playerList[max_value_index], bank[max_value_index]))
    else:
        print("Sorry %s, you guessed the word wrong you've lost %i in winnings" % (playerList[max_value_index], bank[max_value_index]))

def game_summary():

    column_name = ['player name', 'Amount earned by end of game']
    rows = [[playerList[0], bank[0]], [playerList[1], bank[1]], [playerList[2], bank[2]]]
    with open('game_summary.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(column_name)
        w.writerows(rows)

def main():
    global end_round
    GameStart()
    round1()
    end_round = False
    round2()
    round3()
    print('----------------------------')
    print('With round three over the game is concluded. Goodbye!')
    game_summary()



main()

