from copy import deepcopy
from enum import Enum
from random import shuffle
from typing import Iterable, Iterator, Optional, Self

from colorama import Fore, Style

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
    
    COLORS = [Color.RED, Color.BLACK]
    SUITS = [Suit.SPADES, Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS]
    SUITS_RED = [Suit.HEARTS, Suit.DIAMONDS]
    SUITS_BLACK = [Suit.SPADES, Suit.CLUBS] 
    RANKS = [Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE, Rank.SIX, 
             Rank.SEVEN, Rank.EIGHT, Rank.NINE, Rank.TEN, Rank.JACK, 
             Rank.QUEEN, Rank.KING, Rank.ACE]
    FACE_CARDS = [Rank.JACK, Rank.QUEEN, Rank.KING]

    def __init__(self, _rank: Rank | str, _suit: Suit | str, /, _face_up: bool = False, *, \
                 _deck: Optional['Deck'] = None, _hand: Optional['Hand'] = None):
        """Initialize a new playing card.
        
        Args:
            _rank: (Rank | str) The rank/value of the card (e.g., ACE, TWO, KING). Can also be represented \
                with string representations (e.g., 'A', '2', 'K').
            _suit: (Suit) The suit of the card (HEARTS, DIAMONDS, SPADES, CLUBS)
            _face_up: (bool): Determines whether card is face up or down.
            _deck: (Optional[Deck]) The deck this card belongs to. Defaults to None. Can also be represented \
                with string representations (e.g., '♥', '♦', '♠', '♣' or 'H', 'D', 'S', 'C').
            
        Note:
            The card's color is automatically determined based on the suit:
            - RED for HEARTS and DIAMONDS
            - BLACK for SPADES and CLUBS
        """

        if isinstance(_rank, str):
            self._rank = next((r for r in Rank if r.value == _rank), None)
            if self._rank is None:
                raise ValueError(f"Invalid rank: {_rank}")
        elif isinstance(_rank, Rank):
            self._rank = _rank
        else:
            raise TypeError(f"Invalid rank type: {type(_rank)}")

        if isinstance(_suit, str):
            self._suit = next((s for s in Suit if s.value == _suit or s.name[0] == _suit), None)
            if self._suit is None:
                raise ValueError(f"Invalid suit: {_suit}")
        elif isinstance(_suit, Suit):
            self._suit = _suit
        else:
            raise TypeError(f"Invalid suit type: {type(_suit)}")
        
        self._color = Color.RED if self.suit in Card.SUITS_RED else Color.BLACK if self.suit in \
            Card.SUITS_BLACK else None
        
        self._face_up = bool(_face_up)

        self.deck = _deck
        self.hand = _hand # TODO: Add getters and setters

    @property
    def rank(self) -> Rank:
        return self._rank
    
    @rank.setter
    def rank(self, value: Rank):
        if not isinstance(value, Rank):
            raise TypeError(f"Invalid rank type: {type(value)}")
        self._rank = value

    @property
    def suit(self) -> Suit:
        return self._suit
    
    @suit.setter
    def suit(self, value: Suit):
        if isinstance(value, str):
            value = next((s for s in Suit if s.value == value or s.name[0] == value), None)
            if value is None:
                raise ValueError(f"Invalid suit: {value}")
            self._suit = value
            self._color = Color.RED if value in Card.SUITS_RED else Color.BLACK if value in \
                Card.SUITS_BLACK else None
        elif isinstance(value, Suit):
            self._suit = value
            self._color = Color.RED if value in Card.SUITS_RED else Color.BLACK if value in \
                Card.SUITS_BLACK else None
        else:
            raise TypeError(f"Invalid suit type: {type(value)}")

    @property
    def color(self) -> Color:
        return self._color
    
    @color.setter
    def color(self, value: Color):
        raise AttributeError("Color cannot be modified - it is determined by suit")

    @property
    def face_up(self) -> bool:
        return self._face_up
    
    @face_up.setter
    def face_up(self, value: bool):
        if not isinstance(value, (bool, int)):
            raise TypeError(f"Invalid face_up type: {type(value)}")
        self._face_up = bool(value)

    def flip(self) -> Self:
        """Flip card face up/down"""
        self.face_up = not self.face_up

        return self

    def __eq__(self, other):
        if not isinstance(other, Card):
            return TypeError('Cannot compare Card with non-Card object')
        
        return self.rank == other.rank and self.suit == other.suit

    def __lt__(self, other: 'Card') -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return Card.ranks.index(self.rank) < Card.ranks.index(other.rank)
    
    def __gt__(self, other: 'Card') -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return Card.ranks.index(self.rank) > Card.ranks.index(other.rank)

    def __str__(self):
        return f"{Fore.BLACK}{self.rank.value}{self.suit.value}{Style.RESET_ALL}" \
                if self.face_up else f"{Style.DIM}Card{Style.RESET_ALL}"

    def __repr__(self):
        if not self.face_up:
            return f'Card({self.face_up=})'
        elif self.deck and self.hand:
            return f'Card({self.rank}, {self.suit}, {self.face_up=}, {self.deck=}, {self.hand=})'
        elif self.deck:
            return f'Card({self.rank}, {self.suit}, {self.face_up=}, {self.deck=})'
        elif self.hand:
            return f'Card({self.rank}, {self.suit}, {self.face_up=}, {self.hand=})'
        else:
            return f'Card({self.rank}, {self.suit}, {self.face_up=})'
    
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

    STANDARD_SIZE = 52

    def __init__(self, cards: Iterable[Card] = None, *, init: bool = False, deck_count: Optional[int] = 1):
        """Initialize a deck
        
        Args:
            cards: (Card) Additional cards in an iterable, such as a list, to initialize the deck with. \
                If init is True, these cards are added on top of the standard deck.
            init: (bool) If True, create a standard 52-card deck, else initialize an empty deck.
            deck_count: (int) Number of decks to create (duplicates cards). Defaults to 1. deck_count = 2 is \
                is equivalent to creating a standard 52-card deck and adding another standard 52-card deck on top of it.
        """
        self.cards = [Card(rank, suit, _deck=self) for rank in Rank for suit in Suit] if init else []
        if cards:
            if not isinstance(cards, Iterable) or not all(isinstance(card, Card) for card in cards):
                raise TypeError("Can only add an iterable of Card objects to deck")
        
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
        """Add a card to the top of the deck"""
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

    def peek(self, from_top: bool = True) -> Card:
        """Look at the top or bottom card without removing it. Returns single card"""
        if self.is_empty():
            raise ValueError("Cannot peek at a card in an empty deck")
        return self.cards[-1] if from_top else self.cards[0]

    def peek_multiple(self, count: int = 1, from_top: bool = True) -> list[Card]:
        """Look at the top or bottom cards without removing them. Returns list of multiple cards"""
        if count > len(self):
            raise ValueError(f"Cannot peek at {count} cards in deck with {len(self)} cards")
        return self.cards[-count:] if from_top else self.cards[:count]

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

    def __add__(self, other: Iterable[Card]) -> 'Deck':
        """Allow deck1 + deck2 or deck + iterable of cards. Returns new instance."""
        try:
            other = list(other)
        except:
            raise TypeError("Can only add an iterable of Card objects")

        if not all(isinstance(card, Card) for card in other):
            raise TypeError("Can only add an iterable of Card objects")

        return Deck(self.cards + other)

    def __iadd__(self, other: Iterable[Card]) -> Self:
        """Allow deck1 += deck2 or deck += iterable of cards"""
        try:
            other = list(other)
        except:
            raise TypeError("Can only add an iterable of Card objects")

        if not all(isinstance(card, Card) for card in other):
            raise TypeError("Can only add an iterable of Card objects")

        self.extend(other)

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

    def __imul__(self, other: int) -> Self:
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

    def __repr__(self) -> str:
        return f'Deck({self.cards=})'
 
    def __str__(self) -> str:
        return f'Deck of {len(self.cards)} cards: {[str(card) for card in self.cards]}'


class Hand:


    def __init__(self, cards: Iterable[Card] = None, *, _Deck: Optional[Deck] = None):
        """Initialize a hand
        
        Args:
            cards: (Card) Additional cards in an iterable, such as a list, to initialize the deck with. \
                If init is True, these cards are added on top of the standard deck.
        """
        if cards:
            if not isinstance(cards, Iterable) or not all(isinstance(card, Card) for card in cards):
                raise TypeError("Can only add an iterable of Card objects to hand")
            self.cards: list[Card] = [card for card in cards]
        else:
            self.cards: list[Card] = []

        self.deck = _Deck if _Deck else None

    def append(self, card: Card) -> Self:
        """Add a card to the top of the hand"""
        if not isinstance(card, Card):
            raise TypeError("Can only add Card objects to hand")
        self.cards.append(card)

        return self

    def clear(self) -> Self:
        '''
        Clears hand.
        '''
        self.cards.clear()

        return self

    def copy(self) -> 'Hand':
        """Create a shallow copy of the hand"""
        return Hand(self.cards.copy())

    def count(self, card: Card) -> int:
        """Count occurrences of a card in the hand"""
        if not isinstance(card, Card):
            raise TypeError("Can only count Card objects")
        return self.cards.count(card)

    def cut(self, index: int = None) -> Self:
        """Cut the hand at specified index or roughly in half"""
        if index is None:
            index = len(self) // 2
        if not 0 <= index <= len(self):
            raise ValueError(f"Invalid cut index: {index}")
        self.cards = self.cards[index:] + self.cards[:index]
        return self

    def play(self) -> Card:
        '''
        Plays card from top of the hand. To ensure hand is shuffled beforehand, use shuffle() method.
        '''
        
        if self.is_empty():
            raise ValueError("Cannot draw card and play from empty hand")

        return self.cards.pop()

    def play_multiple(self, count: int) -> list[Card]:
        """Plays multiple cards from the deck"""
        if count > len(self):
            raise ValueError(f"Cannot draw {count} cards from hand with {len(self)} cards")
        return [self.draw() for _ in range(count)]

    def extend(self, cards: Iterable[Card]) -> Self:
        """Add multiple cards to the hand"""
        if not all(isinstance(card, Card) for card in cards):
            raise TypeError("Can only add Card objects to hand")
        self.cards.extend(cards)

        return self

    def index(self, card: Card, start: int = 0, stop: int = None) -> int:
        """Find index of a card in the hand"""
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
        """Check if hand is empty"""
        return len(self) == 0

    def peek(self, *, from_top: bool = True) -> Card:
        """Look at the top or bottom card without removing it. Returns single card"""
        if self.is_empty():
            raise ValueError("Cannot peek at a card in an empty hand")
        return self.cards[-1] if from_top else self.cards[0]

    def peek_multiple(self, count: int = 1, from_top: bool = True) -> list[Card]:
        """Look at the top or bottom cards without removing them. Returns list of multiple cards"""
        if count > len(self):
            raise ValueError(f"Cannot peek at {count} cards in hand with {len(self)} cards")
        return self.cards[-count:] if from_top else self.cards[:count]

    def remove(self, card: Card) -> Self:
        """Remove first occurrence of a hand"""
        if not isinstance(card, Card):
            raise TypeError("Can only remove Card objects")
        self.cards.remove(card)
        return self

    def reverse(self) -> Self:
        """Reverse the order of cards in the hand"""
        self.cards.reverse()
        return self

    def shuffle(self) -> Self:
        """Shuffle the hand"""
        shuffle(self.cards)

        return self

    def sort(self, *, ranks: list[Rank] = None, suits: list[Suit] = None, reverse: bool = False) -> Self:
        """Sort the hand by rank and suit
        
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
        """Allow len(hand) to work"""
        return len(self.cards)

    def __getitem__(self, index):
        """Allow hand[0] and hand[1:3] slicing"""
        return self.cards[index]

    def __setitem__(self, index, value):
        """Allow hand[0] = card"""
        if not isinstance(value, Card):
            raise TypeError("Can only add Card objects to hand")
        self.cards[index] = value

    def __delitem__(self, index):
        """Allow del hand[0]"""
        del self.cards[index]

    def __iter__(self) -> Iterator[Card]:
        """Allow for card in hand:"""
        return iter(self.cards)
    
    def __contains__(self, card) -> bool:
        """Allow card in hand"""
        if not isinstance(card, Card):
            raise TypeError("Can only check for Card objects in hand")
        return card in self.cards

    def __add__(self, other: Iterable[Card]) -> 'Hand':
        """Allow hand1 + hand2 or hand + iterable of cards. Returns new instance."""
        try:
            other = list(other)
        except:
            raise TypeError("Can only add an iterable of Card objects")

        if not all(isinstance(card, Card) for card in other):
            raise TypeError("Can only add an iterable of Card objects")

        return Hand(self.cards + other)


    def __iadd__(self, other: Iterable[Card]) -> Self:
        """Allow hand1 += hand2 or hand += iterable of cards"""
        try:
            other = list(other)
        except:
            raise TypeError("Can only add an iterable of Card objects")

        if not all(isinstance(card, Card) for card in other):
            raise TypeError("Can only add an iterable of Card objects")

        self.extend(other)

        return self

    def __mul__(self, other: int) -> 'Hand':
        """Allow hand * 3. Returns new instance."""
        if not isinstance(other, int):
            return TypeError('Cannot multiply hand by non-integer')
        if other < 0:
            raise ValueError("Cannot multiply hand by negative number")
        
        result = Hand(self.cards)  # Create new hand with current cards
        if other == 0:
            result.clear()
        elif other > 1:
            result.cards = [deepcopy(card) for card in self.cards for _ in range(other)]
       
        return result

    def __rmul__(self, other: int) -> 'Hand':
        """Allow 3 * deck"""
        return self * other

    def __imul__(self, other: int) -> Self:
        """Allow hand *= 3"""
        if not isinstance(other, int):
            TypeError("deck_count must be an integer")
        if other < 0:
            raise ValueError("Cannot multiply deck by negative number")
        
        if other == 0:
            self.clear()
        elif other > 1:
            self.cards = [deepcopy(card) for card in self.cards for _ in range(other)]
       
        return self

    def __repr__(self) -> str:
        return f'Hand({self.cards=})'
 
    def __str__(self) -> str:
        return f'Hand ({len(self.cards)}):, cards: {[str(card) for card in self.cards]}'


if __name__ == '__main__':
    card = Card(Rank.ACE, Suit.SPADES)
    card2 = Card(Rank.TEN, Suit.DIAMONDS, False)

    print(repr(card), card2, sep='\n')