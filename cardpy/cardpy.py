from enum import Enum

class Suit(Enum):
    HEARTS = '♥'
    DIAMONDS = '♦'
    CLUBS = '♣'
    SPADES = '♠'

class Rank(Enum):
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE = '9'
    TEN = '10'
    JACK = 'J'
    QUEEN = 'Q'
    KING = 'K'
    ACE = 'A'
    
    # JOKER = NotImplemented # TODO

class Color(Enum):
    RED = 'red'
    BLACK = 'black'

class Card:
    suits = [Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS, Suit.SPADES]
    ranks = [Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE, Rank.SIX, 
             Rank.SEVEN, Rank.EIGHT, Rank.NINE, Rank.TEN, Rank.JACK, 
             Rank.QUEEN, Rank.KING, Rank.ACE]

    def __init__(self, _rank: Rank, _suit: Suit):
        self.rank = _rank
        self.suit = _suit
        self.color = Color.RED if self.suit in [Suit.HEARTS, Suit.DIAMONDS] else Color.BLACK if self.suit in [Suit.SPADES, Suit.CLUBS] else None

    def __eq__(self, other):
        if not isinstance(other, Card):
            return ValueError('Cannot compare Card with non-Card object')
        
        return self.rank == other.rank and self.suit == other.suit

    def __str__(self):
        return f'{self.rank.name} of {self.suit.name} {self.suit.value}'

    def __repr__(self):
        return f'Card({self.rank=}, {self.suit=})'
    
    def __format__(self, format_spec):
        match format_spec:
            case 'rank':
                return self.rank.value
            case 'suit':
                return self.suit.value
            case 'color':
                return self.color.value
            case _:
                raise ValueError(f'Invalid format specifier: {format_spec}')
    
if __name__ == '__main__':
    card1 = Card(Rank.ACE, Suit.SPADES)
    card2 = Card(Rank.ACE, Suit.SPADES)
    print(f'{card1:rank}, {card1:suit}, {card1:color}')