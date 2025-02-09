from enum import Enum
from typing import Iterator, Optional

class Suit(Enum):
    '''
    Suits of playing cards.
    '''
    HEARTS = '♥'
    DIAMONDS = '♦'
    CLUBS = '♣'
    SPADES = '♠'

class Rank(Enum):
    '''
    Ranks of playing cards.
    '''
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

    def __init__(self, _rank: Rank, _suit: Suit, _deck: Optional['Deck'] = None):
        """Initialize a new playing card.
        
        Args:
            _rank: (Rank) The rank/value of the card (e.g., ACE, TWO, KING)
            _suit: (Suit) The suit of the card (HEARTS, DIAMONDS, SPADES, CLUBS)
            _deck: (Optional[Deck]) The deck this card belongs to. Defaults to None.
            
        Note:
            The card's color is automatically determined based on the suit:
            - RED for HEARTS and DIAMONDS
            - BLACK for SPADES and CLUBS
        """

        self.rank = _rank
        self.suit = _suit
        self.color = Color.RED if self.suit in [Suit.HEARTS, Suit.DIAMONDS] else Color.BLACK if self.suit in [Suit.SPADES, Suit.CLUBS] else None
        self.deck = _deck

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

class Deck:

    def __init__(self, init: bool = False, *cards: Card):
        """Initialize a deck
        
        Args:
            init: (bool) If True, create a standard 52-card deck
            *args: (Card) Additional cards to optionally add to deck
        """
        self.cards = [Card(rank, suit, self) for rank in Rank for suit in Suit] if init else []

    def __len__(self) -> int:
        """Allow len(deck) to work"""
        return len(self.cards)

    def __getitem__(self, index):
        """Allow deck[0] and deck[1:3] slicing"""
        return self.cards[index]

    def __setitem__(self, index, value):
        """Allow deck[0] = card"""
        if not isinstance(value, Card):
            raise TypeError("Can only add Card objects to deck")
        self.cards[index] = value

    def __delitem__(self, index):
        """Allow del deck[0]"""
        del self.cards[index]

    def __iter__(self) -> Iterator[Card]:
        """Allow for card in deck:"""
        return iter(self.cards)
    
    def __contains__(self, card) -> bool:
        """Allow card in deck"""
        if not isinstance(card, Card):
            raise TypeError("Can only check for Card objects in deck")
        return card in self.cards

    def append(self, card: Card) -> None:
        """Add a card to the deck"""
        if not isinstance(card, Card):
            raise TypeError("Can only add Card objects to deck")
        self.cards.append(card)

    def extend(self, cards: list[Card]) -> None:
        """Add multiple cards to the deck"""
        if not all(isinstance(card, Card) for card in cards):
            raise TypeError("Can only add Card objects to deck")
        self.cards.extend(cards)

    def __repr__(self):
        return f'Deck({self.cards=})'
 
    def __str__(self):
        return f'Deck of {len(self.cards)} cards: {[str(card) for card in self.cards]}'

if __name__ == '__main__':
    card1 = Card(Rank.ACE, Suit.SPADES)
    card2 = Card(Rank.ACE, Suit.SPADES)
    print(f'{card1:rank}, {card1:suit}, {card1:color}')
    deck = Deck(init=True)
    print(deck)