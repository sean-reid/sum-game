# Sum Game
A card game, about addition and subtraction, played in the terminal against bots

## How to play
The goal of the game is for the sum of the cards in your hidden hand to be as close as possible to the sum of your opponent's matching hand.

### Setup
Each player is dealt 6 cards, face-down. Of those 6 cards, 3 are randomly chosen and set aside. These cards form each player's "matching hand"; the remaining three face-down cards are the player's "hidden hand" and can not be viewed by opponents. Before turns begin, the matching hands are turned face-up simultaneously. 

### Turn Order
Each player, in turn, must do each of the following three actions, in order:
1. Draw a card from the top of the deck and place it in their hidden hand
2. Swap a card from their hidden hand with a card from any player's matching hand
3. Discard a card from their hidden hand

### Game End
The game continues until there are no more cards in the deck to draw.

### Scoring
At the end of the game, each player sums the values of the cards in their hidden hand. They then choose a matching hand on the table that has a sum which is closest to their sum.

The winning player has the smallest difference between sums. Ties are possible, in which case there are multiple winners.

## Run Script
Play the game by running the command.
```
python src/main.py
```

## Author
* [Sean Reid](mailto:seanreid.mail@gmail)
