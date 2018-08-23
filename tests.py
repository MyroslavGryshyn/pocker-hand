import unittest

from custom_exceptions import (SameCardException, WrongAmountException,
                        WrongCardStringLenException, WrongCardValueException,
                        WrongSuitException, WrongTypeException)

from hand import Hand
from constants import (FLUSH, FOUR_OF_A_KIND, FULL_HOUSE, HIGH_CARD, ONE_PAIR,
                       ROYAL_FLUSH, STRAIGHT, STRAIGHT_FLUSH, THREE_OF_A_KIND,
                       TWO_PAIR)


class HandCreationTestCase(unittest.TestCase):
    def test_validates_from_string_type(self):
        with self.assertRaises(WrongTypeException):
            Hand.from_string(25)

    def test_validates_amount_of_cards(self):
        with self.assertRaises(WrongAmountException):
            Hand.from_string('4C 4D 4H 7H 8D 9D')

        with self.assertRaises(WrongAmountException):
            Hand.from_string('4C 4D 4H 7H')

    def test_validate_card_string_len(self):
        with self.assertRaises(WrongCardStringLenException):
            Hand.from_string('4C 4D 4H H KD')

    def test_validates_suit(self):
        with self.assertRaises(WrongSuitException):
            Hand.from_string('4A 4D 4H 7H 8D')

    def test_validates_card_value(self):
        with self.assertRaises(WrongCardValueException):
            Hand.from_string('4C 4D 4H SH KD')

    def test_validates_same_cards(self):
        with self.assertRaises(SameCardException):
            Hand.from_string('4D 4D 4D 7H 8D')

    def test_creates_hand(self):
        Hand.from_string('4C 4D 4H 5H KD')


class HandEvaluationCase(unittest.TestCase):
    def test_evaluetes_pair(self):
        hand = Hand.from_string('4C 4D 7H 5H KD')
        hand_value = hand.get_hand_value()

        self.assertEquals(hand_value, ONE_PAIR)

    def test_evaluetes_flush(self):
        hand = Hand.from_string('4C 5C 7C KC 8C')
        hand_value = hand.get_hand_value()

        self.assertEquals(hand_value, FLUSH)

    def test_evaluetes_set(self):
        hand = Hand.from_string('4C 4D 4H 5H KD')
        hand_value = hand.get_hand_value()

        self.assertEquals(hand_value, THREE_OF_A_KIND)

    def test_evaluetes_straight(self):
        hand = Hand.from_string('4D 5D 6D 7H 8D')
        hand_value = hand.get_hand_value()

        self.assertEquals(hand_value, STRAIGHT)

    def test_evaluetes_high_card(self):
        hand = Hand.from_string('4D 5D 6D TH 8D')
        hand_value = hand.get_hand_value()

        self.assertEquals(hand_value, HIGH_CARD)

    def test_evaluetes_straight_flush(self):
        hand = Hand.from_string('4D 5D 6D 7D 8D')
        hand_value = hand.get_hand_value()

        self.assertEquals(hand_value, STRAIGHT_FLUSH)

    def test_evaluetes_royal_flush(self):
        hand = Hand.from_string('TS JS QS KS AS')
        hand_value = hand.get_hand_value()

        self.assertEquals(hand_value, ROYAL_FLUSH)

    def test_evaluetes_full_house(self):
        hand = Hand.from_string('TS TD TH KS KH')
        hand_value = hand.get_hand_value()

        self.assertEquals(hand_value, FULL_HOUSE)

    def test_evaluetes_2_pairs(self):
        hand = Hand.from_string('TS TD 9H KS KH')
        hand_value = hand.get_hand_value()

        self.assertEquals(hand_value, TWO_PAIR)


class HandComparisonCase(unittest.TestCase):
    def test_compare_pair_and_set(self):
        three_of_a_kind = Hand.from_string('4C 4D 4H 5H KD')
        one_pair = Hand.from_string('4D 3D 3H 7H AD')

        self.assertTrue(three_of_a_kind > one_pair)

    def test_compare_pair_and_pair(self):
        one_pair = Hand.from_string('4D 3D 3H 7H AD')
        one_pair_2 = Hand.from_string('5D 7D 9H 5H TD')

        self.assertTrue(one_pair_2 > one_pair)

    def test_compare_2_equal_pairs(self):
        one_pair = Hand.from_string('5S 5C 3H 7H AD')
        one_pair_2 = Hand.from_string('5D 7D 9H 5H TD')

        self.assertTrue(one_pair > one_pair_2)

    def test_compare_2_equal_hands(self):
        one_pair = Hand.from_string('5S 5C 3H 7H AD')
        one_pair_2 = Hand.from_string('5C 5S 3D 7D AH')

        self.assertTrue(one_pair == one_pair_2)

    def test_compare_2_royal_flashes(self):
        royal_flush = Hand.from_string('AS KS QS JS TS')
        royal_flush_2 = Hand.from_string('AD KD QD JD TD')

        self.assertTrue(royal_flush == royal_flush_2)

    def test_compare_2_two_pairs(self):
        one_pair = Hand.from_string('AS AC KH KS AD')
        one_pair_2 = Hand.from_string('AD AH KD 5C TD')

        self.assertTrue(one_pair > one_pair_2)

    def test_compare_2_high_cards(self):
        one_pair = Hand.from_string('AS KC QH TS TD')
        one_pair_2 = Hand.from_string('AD KH JD 5C TD')

        self.assertTrue(one_pair > one_pair_2)

if __name__ == '__main__':
    unittest.main()
