from copy import deepcopy
from enum import Enum
from random import shuffle
from typing import Iterable, Iterator, Optional, Self

class Rank(Enum):
    """
    Ranks of playing cards in ascending order from TWO to ACE.
    Values are the string representations used for display.
    """
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


class Suit(Enum):
    """
    Suits of playing cards with Unicode symbols as values.
    Standard order: SPADES (♠), HEARTS (♥), DIAMONDS (♦), CLUBS (♣)
    """
    HEARTS = '♥'
    DIAMONDS = '♦'
    CLUBS = '♣'
    SPADES = '♠'


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

    def __init__(self, cards: Iterable[Card] = None, *, init: bool = False, deck_count: Optional[int] = 1):
        """Initialize a deck
        
        Args:
            cards: (Card) Additional cards in an iterable, such as a list, to initialize the deck with. \
                If init is True, these cards are added on top of the standard deck.
            init: (bool) If True, create a standard 52-card deck, else initialize an empty deck.
            deck_count: (int) Number of decks to create (duplicates cards). Defaults to 1. deck_count = 2 is \
                is equivalent to creating a standard 52-card deck and adding another standard 52-card deck on top of it.
        """
        self.cards = [Card(rank, suit, self) for rank in Rank for suit in Suit] if init else []
        if not all (isinstance(card, (Card, Deck)) for card in cards):
            raise TypeError("Can only add Card or Deck objects to deck")
        
        if isinstance(cards, Deck):
            self.cards.extend(cards.cards)
        else:
            self.cards.extend(cards) if cards else None

        match deck_count:
            case 0:
                self.clear()
            case 1:
                pass
            case _:
                if isinstance(deck_count, int) and deck_count > 1:
                    self.cards = [deepcopy(card) for card in self.cards for _ in range(deck_count)]
                else:
                    raise TypeError("deck_count must be an integer greater than 1")

    def append(self, card: Card) -> Self:
        """Add a card to the deck"""
        if not isinstance(card, Card):
            raise TypeError("Can only add Card objects to deck")
        self.cards.append(card)

        return self

    def clear(self, *, init = False, deck_count = 1) -> Self:
        '''
        Clears deck. If init is True, creates a standard 52-card deck afterwards.
        '''
        self.cards.clear()
        self.cards = [Card(rank, suit, self) for rank in Rank for suit in Suit] if init else []

        if init:
            match deck_count:
                case 0:
                    self.clear()
                case 1:
                    pass
                case _:
                    if isinstance(deck_count, int) and deck_count > 1:
                        self.cards = [deepcopy(card) for card in self.cards for _ in range(deck_count)]
                    else:
                        raise TypeError("deck_count must be an integer")

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

    def deal(self, num_players: int, cards_per_player: int) -> list[list[Card]]:
            """Deal cards to multiple players
            
            Args:
                num_players: (int) Number of players to deal to
                cards_per_player: (int) Number of cards each player should receive
                
            Returns:
                List of card lists, where each inner list represents a player's hand
            """
            if num_players * cards_per_player > len(self):
                raise ValueError(f"Not enough cards to deal {cards_per_player} cards to {num_players} players")
            
            hands = [[] for _ in range(num_players)]
            for _ in range(cards_per_player):
                for hand in hands:
                    hand.append(self.draw())
            return hands

    def draw(self) -> Card:
        '''
        Draws card from top of the deck. Ensure deck is shuffled beforehand with shuffle() method.
        '''
        
        if self.is_empty():
            raise ValueError("Cannot draw from empty deck")

        return self.cards.pop()

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

    def __mul__(self, other: int) -> 'Deck':
        """Allow deck * 3"""
        if not isinstance(other, int):
            return TypeError('Cannot multiply deck by non-integer')
        if other < 0:
            raise ValueError("Cannot multiply deck by negative number")
        
        result = Deck(self.cards)  # Create new deck with current cards
        if other == 0:
            result.clear()
        elif other > 1:
            result.cards = [deepcopy(card) for card in self.cards for _ in range(other)]
        return result

    def __rmul__(self, other: int) -> 'Deck':
        """Allow 3 * deck"""
        return self * other

    def __imul__(self, other: int) -> 'Deck':
        """Allow deck *= 3"""
        if not isinstance(other, int):
            TypeError("deck_count must be an integer")
        if other < 0:
            raise ValueError("Cannot multiply deck by negative number")
        
        if other == 0:
            self.clear()
        elif other > 1:
            self.cards = [deepcopy(card) for card in self.cards for _ in range(other)]
        return self

    def __lt__(self, other: 'Card') -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return Card.ranks.index(self.rank) < Card.ranks.index(other.rank)
    
    def __gt__(self, other: 'Card') -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return Card.ranks.index(self.rank) > Card.ranks.index(other.rank)

    def __repr__(self):
        return f'Deck({self.cards=})'
 
    def __str__(self):
        return f'Deck of {len(self.cards)} cards: {[str(card) for card in self.cards]}'


if __name__ == '__main__':
    pass