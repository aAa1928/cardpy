from enum import Enum
from random import shuffle
from typing import Iterable, Iterator, Optional, Self

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
    '''
    Color of playing cards. Red for hearts and diamonds, black for spades and clubs.
    '''
    RED = 'red'
    BLACK = 'black'


class Card:
    
    colors = [Color.RED, Color.BLACK]
    suits = [Suit.SPADES, Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS]
    ranks = [Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE, Rank.SIX, 
             Rank.SEVEN, Rank.EIGHT, Rank.NINE, Rank.TEN, Rank.JACK, 
             Rank.QUEEN, Rank.KING, Rank.ACE]

    def __init__(self, _rank: Rank, _suit: Suit, *, _deck: Optional['Deck'] = None):
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
        self.color = Color.RED if self.suit in [Suit.HEARTS, Suit.DIAMONDS] else Color.BLACK if self.suit in \
            [Suit.SPADES, Suit.CLUBS] else None
        self.deck = _deck

    def __eq__(self, other):
        if not isinstance(other, Card):
            return TypeError('Cannot compare Card with non-Card object')
        
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
                raise TypeError(f'Invalid format specifier: {format_spec}')


class Deck:

    def __init__(self, cards: Iterable[Card] = None, *, init: bool = False):
        """Initialize a deck
        
        Args:
            init: (bool) If True, create a standard 52-card deck, else initialize an empty deck.
            cards: (Card) Additional cards in an iterable, such as a list, to initialize the deck with. \
                If init is True, these cards are added on top of the standard deck.
        """
        self.cards = [Card(rank, suit, self) for rank in Rank for suit in Suit] if init else []
        if not all (isinstance(card, (Card, Deck)) for card in cards):
            raise TypeError("Can only add Card or Deck objects to deck")
        
        if isinstance(cards, Deck):
            self.cards.extend(cards.cards)
        else:
            self.cards.extend(cards) if cards else None

    def append(self, card: Card) -> Self:
        """Add a card to the deck"""
        if not isinstance(card, Card):
            raise TypeError("Can only add Card objects to deck")
        self.cards.append(card)

        return self

    def clear(self, *, init = False) -> Self:
        '''
        Clears deck. If init is True, creates a standard 52-card deck afterwards.
        '''
        self.cards.clear()
        self.cards = [Card(rank, suit, self) for rank in Rank for suit in Suit] if init else []

        return self

    def copy(self) -> 'Deck':
        """Create a shallow copy of the deck"""
        return Deck(self.cards.copy())

    def count(self, card: Card) -> int:
        """Count occurrences of a card in the deck"""
        if not isinstance(card, Card):
            raise TypeError("Can only count Card objects")
        return self.cards.count(card)

    def cut(self, index: int = None) -> Self:
        """Cut the deck at specified index or roughly in half"""
        if index is None:
            index = len(self) // 2
        if not 0 <= index <= len(self):
            raise ValueError(f"Invalid cut index: {index}")
        self.cards = self.cards[index:] + self.cards[:index]
        return self

    def draw(self) -> Card:
        '''
        Draws card from top of the deck. Ensure deck is shuffled beforehand with shuffle() method.
        '''
        card = self.cards.pop()

        return card

    def draw_multiple(self, count: int) -> list[Card]:
        """Draw multiple cards from the deck"""
        if count > len(self):
            raise ValueError(f"Cannot draw {count} cards from deck with {len(self)} cards")
        return [self.draw() for _ in range(count)]

    def extend(self, cards: list[Card]) -> Self:
        """Add multiple cards to the deck"""
        if not all(isinstance(card, Card) for card in cards):
            raise TypeError("Can only add Card objects to deck")
        self.cards.extend(cards)

        return self

    def index(self, card: Card, start: int = 0, stop: int = None) -> int:
        """Find index of a card in the deck"""
        if not isinstance(card, Card):
            raise TypeError("Can only find Card objects")
        if stop is None:
            stop = len(self)
        return self.cards.index(card, start, stop)

    def insert(self, index: int, card: Card) -> Self:
        """Insert a card at a specific position"""
        if not isinstance(card, Card):
            raise TypeError("Can only insert Card objects")
        self.cards.insert(index, card)
        return self

    def is_empty(self) -> bool:
        """Check if deck is empty"""
        return len(self) == 0

    def peek(self, count: int = 1) -> list[Card]:
        """Look at the top cards without removing them"""
        if count > len(self):
            raise ValueError(f"Cannot peek at {count} cards in deck with {len(self)} cards")
        return self.cards[-count:]

    def remove(self, card: Card) -> Self:
        """Remove first occurrence of a card"""
        if not isinstance(card, Card):
            raise TypeError("Can only remove Card objects")
        self.cards.remove(card)
        return self

    def reverse(self) -> Self:
        """Reverse the order of cards in the deck"""
        self.cards.reverse()
        return self

    def shuffle(self) -> Self:
        """Shuffle the deck"""
        shuffle(self.cards)

        return self

    def sort(self, *, ranks: list[Rank] = None, suits: list[Suit] = None, reverse: bool = False) -> Self:
        """Sort the deck by rank and suit
        
        Args:
        ranks: Optional custom rank ordering. Defaults to Card.ranks
        suits: Optional custom suit ordering. Defaults to Card.suits
        reverse: If True, sort in descending order. Defaults to False
        """
        def sort_key(card):
            rank_list = ranks if ranks is not None else Card.ranks
            suit_list = suits if suits is not None else Card.suits
            return (rank_list.index(card.rank), suit_list.index(card.suit))
        
        self.cards.sort(key=sort_key, reverse=reverse)

        return self

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

    def __add__(self, other: 'Deck') -> 'Deck':
        """Allow deck1 + deck2"""
        if not isinstance(other, Deck):
            raise TypeError("Can only add Deck objects")
        return Deck(self.cards + other.cards)

    def __iadd__(self, other: 'Deck') -> 'Deck':
        """Allow deck1 += deck2"""
        if not isinstance(other, Deck):
            raise TypeError("Can only add Deck objects")
        self.extend(other.cards)
        return self

    def __repr__(self):
        return f'Deck({self.cards=})'
 
    def __str__(self):
        return f'Deck of {len(self.cards)} cards: {[str(card) for card in self.cards]}'


if __name__ == '__main__':
    card1 = Card(Rank.ACE, Suit.HEARTS)
    card2 = Card(Rank.TEN, Suit.CLUBS)
    card3 = Card(Rank.KING, Suit.SPADES)
    deck = Deck([card1, card2, card3])
    print(deck)