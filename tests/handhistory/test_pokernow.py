from poker.room.pokernow import PokerNowHandHistory
from poker.constants import GameType, Game, Limit
import pytest
import pytz
from datetime import datetime
from decimal import Decimal

HAND1 = r'''
"-- ending hand #7 --",2023-01-14T21:51:55.296Z,167373311529604
"""brian @ Tf95qWPA1J"" collected 1160 from pot with Full House, Q's over 10's (combination: Q♥, Q♦, Q♠, 10♦, 10♣)",2023-01-14T21:51:55.296Z,167373311529603
"""brian @ Tf95qWPA1J"" shows a Q♥, 7♥.",2023-01-14T21:51:55.296Z,167373311529602
"""michael @ VEYRadLj9o"" collected 1160 from pot with Full House, Q's over 10's (combination: Q♣, Q♦, Q♠, 10♦, 10♣)",2023-01-14T21:51:55.296Z,167373311529601
"""michael @ VEYRadLj9o"" shows a Q♣, 8♥.",2023-01-14T21:51:55.296Z,167373311529600
"""michael @ VEYRadLj9o"" calls 1000",2023-01-14T21:51:54.490Z,167373311449000
"""brian @ Tf95qWPA1J"" raises to 1000",2023-01-14T21:51:43.559Z,167373310355900
"""michael @ VEYRadLj9o"" bets 400",2023-01-14T21:51:16.959Z,167373307695900
"""brian @ Tf95qWPA1J"" checks",2023-01-14T21:50:52.244Z,167373305224400
"River: Q♦, 10♦, 10♣, 2♥ [Q♠]",2023-01-14T21:50:48.194Z,167373304819400
"""brian @ Tf95qWPA1J"" calls 80",2023-01-14T21:50:47.346Z,167373304734600
"""michael @ VEYRadLj9o"" bets 80",2023-01-14T21:50:41.437Z,167373304143700
"""brian @ Tf95qWPA1J"" checks",2023-01-14T21:50:18.768Z,167373301876800
"Turn: Q♦, 10♦, 10♣ [2♥]",2023-01-14T21:50:16.567Z,167373301656700
"""brian @ Tf95qWPA1J"" calls 30",2023-01-14T21:50:15.724Z,167373301572400
"""michael @ VEYRadLj9o"" bets 30",2023-01-14T21:50:13.388Z,167373301338800
"""brian @ Tf95qWPA1J"" checks",2023-01-14T21:49:58.480Z,167373299848000
"Flop:  [Q♦, 10♦, 10♣]",2023-01-14T21:49:53.833Z,167373299383300
"""brian @ Tf95qWPA1J"" calls 50",2023-01-14T21:49:53.031Z,167373299303100
"""michael @ VEYRadLj9o"" raises to 50",2023-01-14T21:49:51.140Z,167373299114000
"""brian @ Tf95qWPA1J"" posts a big blind of 20",2023-01-14T21:49:44.596Z,167373298459605
"""michael @ VEYRadLj9o"" posts a small blind of 10",2023-01-14T21:49:44.596Z,167373298459604
"Your hand is Q♣, 8♥",2023-01-14T21:49:44.596Z,167373298459602
"Player stacks: #1 ""michael @ VEYRadLj9o"" (2040) | #6 ""brian @ Tf95qWPA1J"" (1960)",2023-01-14T21:49:44.596Z,167373298459601
"-- starting hand #7 (id: tooolqqevl05)  (No Limit Texas Hold'em) (dealer: ""michael @ VEYRadLj9o"") --",2023-01-14T21:49:44.596Z,167373298459600
'''


UTC = pytz.timezone('UTC')

@pytest.fixture
def hand_header(request):
    """Parse hand history header only defined in hand_text
    and returns a PokerNowHandHistory instance.
    """
    hh = PokerNowHandHistory(request.instance.hand_text)
    hh.parse_header()
    return hh


# class Test1:
#     hand_text = """
#         blah blah
#     """
#     @pytest.mark.parametrize(
#         ("attribute", "expected_value"),
#         [
#             ("ident", "foo"),
#             ("tournament_ident", "bar"),
#         ],
#     )
#     def test_values_after_header_parsed(self, hand_header, attribute, expected_value):
#         assert getattr(hand_header, attribute) == expected_value


class TestHeader1:
    hand_text = HAND1
    @pytest.mark.parametrize(
        ("attribute", "expected_value"),
        [
            ("ident", "tooolqqevl05"),
            ("game_type", GameType.CASH),
            ("tournament_ident", None),
            ("tournament_level", None),
            ("currency", None),
            ("buyin", None),
            ("rake", None),
            ("game", Game.HOLDEM),
            ("limit", Limit.NL),
            ("sb", Decimal(10)),
            ("bb", Decimal(20)),
            ("date", UTC.localize(datetime(2023, 1, 14, 21, 49, 44, 596000))),
        ],
    )
    def test_values_after_header_parsed(self, hand_header, attribute, expected_value):
        assert getattr(hand_header, attribute) == expected_value