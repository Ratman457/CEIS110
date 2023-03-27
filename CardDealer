# This program builds a deck of cards and then deals cards on the request of the user.

import random # So we can deal random cards.

deck = [] # These variables will be available everywhere in this file and will be lists of dictionaries representing cards.
hand = []

def main(): 
    input('Press ENTER to create a deck of cards\n')
    make_deck()
    card_num = input('Done!\nHow many cards do you want dealt to you?\n:    ')
    while int(card_num) > len(deck):
        card_num = input(f'There are not that many cards in the deck!\nPlease pick a hand size less than {len(deck)}.\n:    ')
    hand = deal_me_in(card_num)
    my_hand(hand)
    print('Press ENTER to deal another card, or enter HAND to see all cards dealt so far.')
    while len(deck) > 0: # We can keep getting cards until there are no more cards.
        if input() == 'HAND':
            print(f'You have {len(hand)} cards.')
            my_hand(hand)
        else:
            new_card = deal_me_in(1)
            hand.append(new_card[0])
            my_hand(new_card)
    print(f'Your hand was:')
    my_hand(hand)
    print('\n    All cards have been dealt. Please go outside.')

def make_deck(): # We could just write a list of all the cards but that would be boring and easier. If we run this twice the deck would have 2 of each card.
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    for suit in suits:
        for x in range(1, 14):
            deck.append({'value': x, 'suit': suit}) # Each 'card' is made up of two pairs of information. The 'keys' of the dictionary are 'suit' and 'value'.
    for card in deck: # We need to make sure that the card values are named correctly. We could do this another way but this way looks nicer, I think.
        if card['value'] == 1: card['value'] = 'Ace'
        if card['value'] == 11: card['value'] = 'Jack'
        if card['value'] == 12: card['value'] = 'Queen'
        if card['value'] == 13: card['value'] = 'King'

def deal_me_in(num_cards): # We can call this whenever we want cards. It returns a list with a number of cards in it so we need to add an index if we want to use them.
    hand = []
    print(f'Dealing {num_cards} cards...')
    for i in range(0, int(num_cards)):
        chosen_card = random.choice(deck)
        hand.append(chosen_card)
        deck.remove(chosen_card) # We do not want to get cards more than once so we remove the cards from the deck.
    return hand

def my_hand(hand): # When we print a card straight from the list of dictionaries it comes out looking dumb so we use a function to print cards in a nice-looking way.
    count = 1
    for card in hand:
        if count == len(hand): # The last card will have a period at the end.
            print(f'{card["value"]} of {card["suit"]}.')
        elif count % 6 == 0: # Every six cards we add in a newline.
            print(f'{card["value"]} of {card["suit"]}, ')
        else: # All other cards get a comma and a space.
            print(f'{card["value"]} of {card["suit"]}', end = ', ')
        count += 1
    print()

main()

