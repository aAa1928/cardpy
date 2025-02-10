# cardpy

A comprehensive Python module for playing cards, providing flexible card and deck management.

## Features

- Standard 52-card deck management
- Support for multiple decks (e.g., for Blackjack)
- Card comparison and sorting
- Unicode suit symbols (♠, ♥, ♦, ♣)
- Rich deck operations (shuffle, cut, deal, etc.)
- Type hints and thorough error checking
- Chainable methods for fluid syntax

## Installation

Install using pip:

```bash
pip install cardpy
```

## Quick Start

```python
from cardpy import Card, Deck, Rank, Suit

# Create and shuffle a standard deck
deck = Deck(init=True)
deck.shuffle()

# Deal 5 cards each to 4 players
hands = deck.deal(4, 5)
for i, hand in enumerate(hands, 1):
    print(f"Player {i}'s hand: {hand}")

# Create specific cards
ace_spades = Card(Rank.ACE, Suit.SPADES)
king_hearts = Card('K', '♥')  # String representations also work
```

## Core Classes

### Card

Represents a playing card with rank, suit, and color:

```python
# Create cards using enum members or strings
ace = Card(Rank.ACE, Suit.SPADES)
king = Card('K', 'H')  # 'H' for Hearts

# Compare cards
if ace > king:
    print("Ace is higher than King")

# Format card display
print(f"{ace}")  # "ACE of SPADES ♠"
print(f"{ace:rank}")  # "A"
print(f"{ace:suit}")  # "♠"
```

### Deck

Manages a collection of cards with various operations:

```python
# Create different types of decks
standard = Deck(init=True)  # 52-card deck
empty = Deck()  # Empty deck
multiple = Deck(init=True, deck_count=6)  # 6 decks for Blackjack

# Chain operations
deck.shuffle().cut().reverse()

# Draw cards
card = deck.draw()
hand = deck.draw_multiple(5)

# Peek at cards
top_cards = deck.peek(3)  # Look at top 3 cards

# Combine decks
big_deck = deck1 + deck2
deck1 *= 2  # Double the deck
```

## Advanced Features

### Custom Sorting

Sort cards using custom rank and suit orders:

```python
# Define custom ordering
custom_ranks = [Rank.ACE] + Card.ranks[:-1]  # Ace-low ordering
custom_suits = [Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS, Suit.SPADES]

# Sort using custom order
deck.sort(ranks=custom_ranks, suits=custom_suits)
```

### Deck Operations

```python
# Deal cards to multiple players
hands = deck.deal(4, 5)  # 5 cards each to 4 players

# Cut the deck
deck.cut()  # Cut in half
deck.cut(15)  # Cut at specific position

# Count specific cards
aces = deck.count(Card(Rank.ACE, Suit.SPADES))
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

[GitHub](https://github.com/aAa1928/cardpy)
[PyPi](https://pypi.org/project/cardpy/)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Risheet Lenka - [GitHub](https://github.com/aAa1928)
