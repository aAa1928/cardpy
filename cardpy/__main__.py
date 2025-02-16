from rich.console import Console
from rich.markdown import Markdown

MARKDOWN = '''
# cardpy

A comprehensive Python module for playing cards, providing flexible card and deck management with type hints and modern Python features.

## Features

- Standard 52-card deck management
- Support for multiple decks (e.g., for Blackjack)
- Card comparison and sorting
- Unicode suit symbols (♠, ♥, ♦, ♣)
- Rich deck operations (shuffle, cut, deal, etc.)
- Type hints and thorough error checking
- Chainable methods for fluid syntax
- Hand management for card games
- Custom sorting options
- Face-up/face-down card tracking

## Installation

```bash
pip install cardpy
```

## Quick Start

```python
from cardpy import Card, Deck, Hand, Rank, Suit

# Create and shuffle a deck
deck = Deck(init=True)  # Creates standard 52-card deck
deck.shuffle()

# Create a hand and deal cards
hand = Hand()
hand.extend(deck.draw_multiple(5))
print(f"Your hand: {hand}")

# Create specific cards
ace_spades = Card(Rank.ACE, Suit.SPADES)
king_hearts = Card('K', '♥')  # String representations work too

# Compare cards
if ace_spades > king_hearts:
    print("Ace beats King!")
```

## Core Classes

### Card

Represents a playing card with rank, suit, color and face-up status:

```python
# Multiple ways to create cards
ace = Card(Rank.ACE, Suit.SPADES)
king = Card('K', 'H')  # Using string shortcuts
ten = Card('10', '♦')  # Using Unicode symbols

# Card properties
print(f"{ace}")        # "ACE of SPADES ♠"
print(f"{ace:rank}")   # "A"
print(f"{ace:suit}")   # "♠"
print(f"{ace:color}")  # "black"

# Face-up/down handling
ace.face_up = True
ace.flip()  # Flips the card over
```

### Deck

Manages collections of cards with rich operations:

```python
# Different deck types
standard = Deck(init=True)           # 52-card deck
empty = Deck()                       # Empty deck
blackjack = Deck(init=True, deck_count=6)  # 6 decks combined

# Chain operations
deck.shuffle().cut().reverse()

# Card operations
card = deck.draw()
hand = deck.draw_multiple(5)
top_three = deck.peek_multiple(3)

# Combine decks
big_deck = deck1 + deck2
deck1 *= 2  # Double the deck
```

### Hand

Manages player hands with similar operations to Deck:

```python
# Create and manage hands
hand = Hand()
hand.extend(deck.draw_multiple(5))
hand.sort()  # Sort by rank and suit

# Play cards
played_card = hand.play()
played_multiple = hand.play_multiple(2)

# Combine hands
merged_hand = hand1 + hand2
```

## Advanced Features

### Custom Sorting

Sort cards using custom rank and suit orders:

```python
# Define custom ordering
ace_low = [Rank.ACE] + Card.RANKS[:-1]  # Ace-low ordering
hearts_high = [Suit.DIAMONDS, Suit.CLUBS, Suit.SPADES, Suit.HEARTS]

# Sort using custom order
deck.sort(ranks=ace_low, suits=hearts_high)
hand.sort(ranks=ace_low, suits=hearts_high)
```

### Multiple Deck Games

```python
# Create a 6-deck shoe for Blackjack
shoe = Deck(init=True, deck_count=6)
shoe.shuffle()

# Deal cards to multiple players
hands = shoe.deal(4, 2)  # 2 cards each to 4 players

# Track remaining cards
remaining = len(shoe)
print(f"Cards remaining: {remaining}")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

- [GitHub Repository](https://github.com/aAa1928/cardpy)
- [PyPI Package](https://pypi.org/project/cardpy/)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Risheet Lenka - [GitHub Profile](https://github.com/aAa1928)

'''

console = Console()
md = Markdown(MARKDOWN)
md = console.print(md)