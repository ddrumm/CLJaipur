# Don Drummond
# Create a Command Line version of the
# the popular 2-player game Jaipur

# DOCUMENT project with a write-up
# Start on Blog -- Board Game Evaluation
# get into AI/Analysis on if the game is balanced

import random
import os

# Once 3 goods become sold out the game is over
SOLD_OUT_GOODS = 0

# Create Deck
def make_deck():
	"""
	A deck in Jaipur has:
	6: Diamond, Gold, Silver Cards
	8: Cloth, Spice Cards
	10: Leather Cards
	11: Camels
	Note, a game starts with three up face camel cards
	in the market, thus our make_deck will online
	populate the deck with 8 camels
	:return: An Array with the correct Jaipur Deck
	"""
	deck = []
	for i in range(6):
		deck.append("Diamond")
		deck.append("Gold")
		deck.append("Silver")

	for i in range(8):
		deck.append("Cloth")
		deck.append("Spice")
		deck.append("Camel")

	for i in range(10):
		deck.append("Leather")

	random.shuffle(deck)

	return deck


# Create Tokens
def create_tokens():
	"""
	The Jaipur game has 38 tokens with the following values:
	7x 3 card bonus tokens valued: 3, 3, 2, 2, 2, 1, 1
	6x 4 card bonus tokens valued: 6, 6, 5, 5, 4, 4
	5x 5 card bonus tokens valued: 10, 10, 9, 8, 8
	5x diamond goods tokens valued: 7, 7, 5, 5, 5
	5x gold goods tokens valued: 6, 6, 5, 5, 5
	5x silver goods tokens valued: 5, 5, 5, 5, 5
	7x spice goods tokens valued: 5, 3, 3, 2, 2, 1, 1
	7x cloth goods tokens valued: 5, 3, 3, 2, 2, 1, 1
	9x leather goods tokens valued: 4, 3, 2, 1, 1, 1, 1, 1, 1

	:return: a dictionary with all available goods and bonus tokens
	"""
	tokens = {
		"card_three": [3, 3, 2, 2, 1, 1],
		"card_four": [6, 6, 5, 5, 4, 4],
		"card_five": [10, 10, 9, 8, 8],

		"Diamond": [7, 7, 5, 5, 5],
		"Gold": [6, 6, 5, 5, 5],
		"Silver": [5, 5, 5, 5, 5],
		"Spice": [5, 3, 3, 2, 2, 1, 1],
		"Cloth": [5, 3, 3, 2, 2, 1, 1],
		"Leather": [4, 3, 2, 1, 1, 1, 1, 1, 1]
	}

	random.shuffle(tokens["card_three"])
	random.shuffle(tokens["card_four"])
	random.shuffle(tokens["card_five"])

	return tokens


"""
def seal_excellence():
HANDLE 3x seals of excellence - awarded at round end

"""

"""
TODO handle most camel points.
def issue_camel_token(hand1, hand2):
	if hand1.camels() > hand2.camels():
		player1.points += 5
	else:
		player2.points += 5
"""


# create a player class
# intentionally leaving out herd and including in hand
class Player:
	def __init__(self, name, hand, tokens, points):
		self.name = name
		self.hand = hand
		self.tokens = tokens
		self.points = points
		self.seal_excellence = 0
		self.num_non_camel_cards = 0


# Deal Initial Hand
# increment player's num_non_camel_cards to track how many goods cards they have
def deal_hand(deck, p1, p2):
	for i in range(5):
		if deck[0] == "Camel":
			p1.hand.append(deck.pop(0))
			p2.hand.append(deck.pop(0))
		else:
			p1.hand.append(deck.pop(0))
			p1.num_non_camel_cards += 1
			p2.hand.append(deck.pop(0))
			p2.num_non_camel_cards += 1


# Create Market
def create_market(deck):
	market = ["Camel", "Camel", "Camel", deck.pop(0), deck.pop(0)]
	random.shuffle(market)
	return market


# Display Market or Hand
def display_cards(cards):
	for count, card in enumerate(cards):
		print(str(count + 1) + ". " + card)


# Display Tokens
def display_tokens(tokens):
	print("There are " + str(len(tokens["card_three"])) + " three card bonus tokens left.")
	print("There are " + str(len(tokens["card_four"])) + " four card bonus tokens left.")
	print("There are " + str(len(tokens["card_five"])) + " five card bonus tokens left.")
	diamond = ', '.join(map(str, tokens["Diamond"]))
	gold = ', '.join(map(str, tokens["Gold"]))
	silver = ', '.join(map(str, tokens["Silver"]))
	spice = ', '.join(map(str, tokens["Spice"]))
	cloth = ', '.join(map(str, tokens["Cloth"]))
	leather = ', '.join(map(str, tokens["Leather"]))
	print(" There are " + diamond + " diamond goods tokens left")
	print(" There are " + gold + " gold goods tokens left")
	print(" There are " + silver + " silver goods tokens left")
	print(" There are " + spice + " spice goods tokens left")
	print(" There are " + cloth + " cloth goods tokens left")
	print(" There are " + leather + " leather goods tokens left")


# Turn Mechanism
def display_options(player, market, deck, tokens):
	print("Enter:")
	print("1 to take goods")
	print("2 to sell goods")
	print("3 to see available tokens")
	print("4 to view your hand")
	print("5 to view the market")
	print("6 for help")
	print()
	print("The market is " + ', '.join(map(str, market)))
	print()
	print("Your hand is " + ', '.join(map(str, player.hand)))
	print()
	answer = input()
	if answer == "1":
		take_cards(player, market, deck, tokens)
	elif answer == "2":
		sell_cards(player, tokens)
	elif answer == "3":
		display_tokens(tokens)
	elif answer == "4":
		print("Your hand is " + ', '.join(map(str, player.hand)))
		print()
		display_options(player, market, deck, tokens)
		print()
	elif answer == "5":
		print()
		print("The market is " + ', '.join(map(str, market)))
		print()
		display_options(player, market, deck, tokens)
	elif answer == "6":
		print()
		print("display help")
		print()
		display_options(player, market, deck, tokens)
	else:
		print("Please enter 1 or 2")
		display_options(player, market, deck)


# Take Goods
def take_cards(player, market, deck, tokens):
	print("Enter:")
	print("1 to take several goods")
	print("2 to take a single good")
	print("3 to take camels")
	answer = input()
	if answer == "1":
		if player.num_non_camel_cards > 6:
			print("You can only have 7 cards in your end")
			display_options(player, market, deck, tokens)
		else:
			take_several_goods(player, market, deck)
	elif answer == "2":
		if player.num_non_camel_cards > 6:
			print("You can only have 7 cards in your end")
			display_options(player, market, deck, tokens)
		else:
			take_single_good(player, market, deck)
	elif answer == "3":
		take_camels(player, market, deck)
	else:
		print("Please enter 1 or 2 or 3")
		take_cards(player, market, deck, tokens)


def take_several_goods(player, market, deck):
	cards_given_up = set()
	card_number_given = set()
	cards_requested = set()
	print()
	display_cards(market)
	print()
	print("Please indicate which cards you'd like to take.")
	print('Continue to enter numbers, enter "Done" when complete')
	answer = None
	while answer != "Done":
		answer = input()
		if answer == "Done":
			break
		if answer != "1" and answer != "2" and answer != "3" and answer != "4" and answer != "5":
			print("Please enter 1, 2, 3, 4, or 5")
		else:
			if market[int(answer) - 1] == "Camel":
				print("You can only take goods when exchanging, not camels.")
			else:
				if (int(answer) - 1) in cards_requested:
					print("You've already picked that card.")
				else:
					cards_requested.add(market[int(answer) - 1])

	print()
	display_cards(player.hand)
	print()
	print('Please indicate which cards you would give up.')
	print('Continue to enter numbers, enter "Done" when complete')
	answer = None
	cards_in_hand = set()
	for count, item in enumerate(player.hand):
		count += 1
		cards_in_hand.add(str(count))

	while answer != "Done":
		answer = input()
		if answer == "Done":
			break
		if answer not in cards_in_hand:
			print("Please enter a valid number.")
		elif answer in card_number_given:
			print("You already selected that number, please try again.")
		else:
			card_number_given.add(answer)
			cards_given_up.add(player.hand[int(answer) - 1])

	# Validate that at least 2 cards were traded and the amount given up and
	# requested matches
	print(len(cards_given_up))
	print(len(cards_requested))

	if len(cards_given_up) <= 1 or len(cards_requested) <= 1:
		print("You must trade at least 2 cards when you take several goods.")
		take_several_goods(player, market, deck)
	elif len(cards_given_up) != len(cards_requested):
		print("You have request and give up the same amount of cards.")
	else:
		# Remove items given up from hand and add them to the market
		for item in cards_given_up:
			player.hand.remove(item)
			market.append(item)

		# Remove items requested from the market and add them to players hand
		for item in cards_requested:
			market.remove(item)
			player.hand.append(item)


def take_single_good(player, market, deck):
	"""

	:param player: current player
	:param market: current market
	:param deck: game deck
	:return: None - provides the mechanism for a player to take a single none
	"""
	print()
	display_cards(market)
	print()
	print("Please indicate which card you would like to take 1, 2, 3, 4, or 5")
	answer = input()
	if answer == "1":
		if market[0] == "Camel":
			print("You must take all camels")
			take_single_good(player, market, deck)
		else:
			player.num_non_camel_cards += 1
			player.hand.append(market[0])
			market.pop(0)
			draw(deck, market)
	elif answer == "2":
		if market[1] == "Camel":
			print("You must take all camels")
			take_single_good(player, market, deck)
		else:
			player.num_non_camel_cards += 1
			player.hand.append(market[1])
			market.pop(1)
			draw(deck, market)
	elif answer == "3":
		if market[2] == "Camel":
			print("You must take all camels")
			take_single_good(player, market, deck)
		else:
			player.num_non_camel_cards += 1
			player.hand.append(market[2])
			market.pop(2)
			draw(deck, market)
	elif answer == "4":
		if market[3] == "Camel":
			print("You must take all camels")
			take_single_good(player, market, deck)
		else:
			player.num_non_camel_cards += 1
			player.hand.append(market[3])
			market.pop(3)
			draw(deck, market)
	elif answer == "5":
		if market[4] == "Camel":
			print("You must take all camels")
			take_single_good(player, market, deck)
		else:
			player.num_non_camel_cards += 1
			player.hand.append(market[4])
			market.pop(4)
			draw(deck, market)
	else:
		print("Please enter 1, 2, 3, 4, or 5")
		take_single_good(player, market, deck)


def take_camels(player, market, deck):
	count = 0
	for card in market:
		if card == "Camel":
			player.hand.append("Camel")
			count += 1

	for camel in range(count):
		market.remove("Camel")
		draw(deck, market)  # Draw new cards for all remove camels draw()


# Sell Cards
# Assumes if you sell you want to sell as many of a good as possible
def sell_cards(player, tokens):
	print()
	display_cards(player.hand)
	print()
	player_hand = set()
	for item in player.hand:
		if item != "Camel":
			player_hand.add(item)
	print("What good would you like to sell?")
	answer = input()
	while answer not in player_hand:
		print("That is either not valid input or you don't have the good.")
		print("Please try again, enter the good as it is displayed in your hand.")
		print()
		display_cards(player.hand)
		print()
		answer = input()
	else:
		cards_sold = []
		# Enforce expensive goods must be sold with at least 2 cards
		if (answer == "Diamond" or answer == "Gold" or answer == "Silver") and (player.hand.count(answer) < 2):
			print("Diamond, Gold, and Silver cannot be sold individually.")
			sell_cards(player, tokens)
		else:
			for card in player.hand:
				if card == answer:
					cards_sold.append(card)
			for i in range(len(cards_sold)):
				player.points += tokens[answer].pop(0)
				player.hand.remove(answer)
				player.num_non_camel_cards -= 1

		# awarding bonus tokens for selling 3, 4, or 5 cards
		if len(cards_sold) == 3:
			player.points += tokens["card_three"].pop(0)
		elif len(cards_sold) == 4:
			player.points += tokens["card_four"].pop(0)
		elif len(cards_sold) == 5:
			player.points += tokens["card_five"].pop(0)


# Handle Turns

# Create Game Handler
def turn_handler(deck, market, p1, p2, ):
	pass


# Draw a card to the market
def draw(deck, market):
	market.append(deck.pop(0))


if __name__ == "__main__":
	game_deck = make_deck()
	tokens = create_tokens()
	p1 = Player("Don", [], [], 0)
	p2 = Player("Karolina", [], [], 0)
	deal_hand(game_deck, p1, p2)
	market = create_market(game_deck)

	while SOLD_OUT_GOODS != 3 and len(game_deck) != 0:
		display_options(p1, market, game_deck, tokens)
		display_options(p2, market, game_deck, tokens)

	if p1.points > p2.points:
		print(p1.name + " wins!")
	elif p1.points < p2.points:
		print(p2.name + " wins!")
	else:
		print("TIE")