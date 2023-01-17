from zope.interface import implementer
from functools import cached_property
from .. import handhistory as hh
import re
from datetime import datetime
import pytz
from poker.constants import Game, Limit, GameType
from pprint import pprint as pp
from decimal import Decimal


UTC = pytz.timezone('UTC')

@implementer(hh.IHandHistory)
class PokerNowHandHistory(hh._BaseHandHistory):
    _start_hand_re = re.compile(r'''\"-- starting hand \#(?P<handnum>\d+) \(id: (?P<handid>[a-z0-9]+)\)  \((?P<gametype>.*?)\) \(dealer: \"\"(?P<buttonplayer>.*?)\"\"\) --\",(?P<handutc>.*?),(?P<handseqno>.*$)''')
    _stack_size_re = re.compile(r'''\"Player stacks:(?P<players>(( \|)? \#(\d+) \"\"(?P<playername>.*?)\"\" \((?P<stacksize>\d+)\))+)\",(?P<handutc>.*?),(?P<handseqno>.*$)''')
    _post_sb_re = re.compile(r'''\"\"\"(?P<playername>.*?)\"\" posts a small blind of (?P<sbamt>\d+)\",(?P<handutc>.*?),(?P<handseqno>.*$)''')
    _post_bb_re = re.compile(r'''\"\"\"(?P<playername>.*?)\"\" posts a big blind of (?P<bbamt>\d+)\",(?P<handutc>.*?),(?P<handseqno>.*$)''')

    # not corresponding to a line
    _player_re = re.compile(r'''( \|)? \#(?P<seatno>\d+) \"\"(?P<playername>.*?)\"\" \((?P<stacksize>\d+)''')

    def parse(self):
        raise NotImplementedError()
        self._table_match = 100
        self.parsed = True

    @staticmethod
    def parse_game_type(gametypestr):
        if gametypestr == "No Limit Texas Hold'em":
            return Game.HOLDEM

        raise ValueError(f'Game string {gametypestr} not recognized')

    @staticmethod
    def parse_limit_type(gametypestr):
        if gametypestr == "No Limit Texas Hold'em":
            return Limit.NL

    def parse_header(self):
        self.max_players = 9 # TODO is this true?
        self.game_type = GameType.CASH

        # START HAND LINE
        match_start_hand = self._start_hand_re.match(self.lines[0])
        start_hand_d = match_start_hand.groupdict()

        self.ident = start_hand_d['handid']

        handutcstr = start_hand_d['handutc']
        handutcfmt = "%Y-%m-%dT%H:%M:%S.%fZ"
        self.date = UTC.localize(datetime.strptime(handutcstr, handutcfmt))

        self.game = self.parse_game_type(start_hand_d['gametype'])
        self.limit = self.parse_limit_type(start_hand_d['gametype'])

        buttonplayername = start_hand_d['buttonplayer']

        # PLAYER STACK SIZE LINE
        match_stack_size = self._stack_size_re.match(self.lines[1])
        stack_size_d = match_stack_size.groupdict()
        playersstr = stack_size_d['players']
        self.players = self._init_seats(self.max_players)
        for playermatch in re.finditer(self._player_re, playersstr): 
            _d = playermatch.groupdict()
            index = int(_d['seatno'])
            self.players[index] = hh._Player(
                name=_d['playername'],
                stack=int(_d['stacksize']),
                seat=int(_d['seatno']),
                combo=None,
            )

        # now that we have the players, get the button player
        _l = list(filter(lambda player: player.name==buttonplayername, self.players))
        if len(_l) != 1:
            raise Exception() # TODO
        self.button = _l[0]

        # SB, BB
        for line in self.lines:
            match = self._post_sb_re.match(line)
            if match:
                _d = match.groupdict()
                self.sb = Decimal(int(_d['sbamt']))
                break
        else:
            self.sb = None

        for line in self.lines:
            match = self._post_bb_re.match(line)
            if match:
                _d = match.groupdict()
                self.bb = Decimal(int(_d['bbamt']))
                break
        else:
            self.bb = None

        # other properties the header is expected to populate
        self.tournament_ident = None
        self.tournament_level = None
        self.currency = None
        self.buyin = None
        self.rake = None

        # breakpoint()

        # raise NotImplementedError()

    @cached_property
    def lines(self):
        return list(reversed(self.raw.split('\n')))