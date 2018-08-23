from functools import total_ordering
from collections import Counter

from constants import (
    CARD_VALUES, FLUSH, FOUR_OF_A_KIND, FULL_HOUSE, HIGH_CARD, ONE_PAIR,
    ROYAL_FLUSH, STRAIGHT, STRAIGHT_FLUSH, SUITS, THREE_OF_A_KIND, TWO_PAIR,
    HAND_VALUES_ORDER
)
from custom_exceptions import (
    SameCardException, WrongAmountException, WrongCardStringLenException,
    WrongCardValueException, WrongSuitException, WrongTypeException
)


class Card:
    CARD_STRING_LEN = 2

    def validate_suit(self, suit):
        if suit not in SUITS:
            raise WrongSuitException(
                "Card element's suit should be in {}".format(SUITS)
            )
        return suit

    def validate_card_value(self, card_value):
        if card_value not in CARD_VALUES:
            raise WrongCardValueException(
                "Card element's value should be in {}".format(CARD_VALUES)
            )
        return card_value

    def __init__(self, card_string):
        if len(card_string) != self.CARD_STRING_LEN:
            raise WrongCardStringLenException(
                "Card element's length should be {}"
                .format(self.CARD_STRING_LEN)
            )

        self.suit = self.validate_suit(card_string[-1])
        self.card_value = self.validate_card_value(card_string[0])


class BaseHand:
    NUMBER_OF_CARDS = 5
    cards = []

    def __init__(self, cards):
        if len(cards) != self.NUMBER_OF_CARDS:
            raise WrongAmountException(
                'The amount of cards should be {}'
                .format(self.NUMBER_OF_CARDS)
            )

        if len(cards) != len(set(cards)):
            raise SameCardException('Cards should be different')

        self.cards = [Card(card_string) for card_string in cards]
        self.suits = [card.suit for card in self.cards]

        self.card_values = sorted([
            CARD_VALUES[card.card_value] for card in self.cards
        ])

        self.counted_values = sorted(
            Counter(self.card_values).most_common(),
            key=lambda pair: (pair[1], pair[0]),
            reverse=True
        )


@total_ordering
class Hand(BaseHand):
    @classmethod
    def from_string(cls, cards_string):
        try:
            cards = cards_string.split()
        except AttributeError:
            raise WrongTypeException('from_string argument should be str')
        return Hand(cards=cards)

    def __init__(self, cards):
        super().__init__(cards)
        self.hand_value = self.get_hand_value()
        self.hand_value_code = HAND_VALUES_ORDER.index(self.hand_value)

    def get_hand_value(self):
        if self._has_one_pair():
            if self._is_set():
                if self._is_4_of_a_kind():
                    return FOUR_OF_A_KIND
                if self._has_another_pair():
                    return FULL_HOUSE
                return THREE_OF_A_KIND
            if self._has_another_pair():
                return TWO_PAIR
            return ONE_PAIR
        elif self._is_flush():
            if self._is_straight():
                if self._contains_ace():
                    return ROYAL_FLUSH
                return STRAIGHT_FLUSH
            return FLUSH
        elif self._is_straight():
            return STRAIGHT
        else:
            return HIGH_CARD

    def _get_highest_card(self):
        return self.card_values[0]

    def _has_one_pair(self):
        if len(set(self.card_values)) < len(self.card_values):
            return True

    def _is_flush(self):
        if len(set(self.suits)) == 1:
            return True

    def _is_set(self):
        return self.counted_values[0][1] == 3

    def _is_straight(self):
        for i, card_value in enumerate(self.card_values[:-1]):
            if card_value != self.card_values[i + 1] - 1:
                return False
        return True

    def _contains_ace(self):
        return CARD_VALUES['A'] in self.card_values

    def _is_4_of_a_kind(self):
        return self.counted_values[0][1] == 4

    def _has_another_pair(self):
        return self.counted_values[1][1] == 2

    def __gt__(self, other):
        if self.hand_value_code > other.hand_value_code:
            return True
        for i, card_value in enumerate(self.counted_values[1:]):
            if card_value[0] > other.counted_values[i][0]:
                return True
            elif card_value[0] < other.counted_values[i][0]:
                return False
        return False

    def __eq__(self, other):
        if self.hand_value_code != other.hand_value_code:
            return False
        for i, card_value in enumerate(self.counted_values[1:]):
            if card_value[0] != other.counted_values[i+1][0]:
                return False
        return True

    def __ne__(self, other):
        if self.hand_value_code != other.hand_value_code:
            return True
        for i, card_value in enumerate(self.counted_values[1:]):
            if card_value[0] != other.counted_values[i][0]:
                return True
        return False

    def __str__(self):
        return (
            "<{} {}, '{}'>"
            .format(
                self.__class__.__name__,
                [card.card_value + card.suit for card in self.cards],
                self.hand_value)
        )
