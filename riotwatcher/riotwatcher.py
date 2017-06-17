from collections import deque
import time
import requests
import urllib.parse

# Constants
BRAZIL = 'BR'
EUROPE_NORDIC_EAST = 'EUNE'
EUROPE_WEST = 'EUW'
JAPAN = 'JP'
KOREA = 'KR'
LATIN_AMERICA_NORTH = 'LAN'
LATIN_AMERICA_SOUTH = 'LAS'
NORTH_AMERICA = 'NA'
OCEANIA = 'OCE'
TURKEY = 'TR'
RUSSIA = 'RU'
PBE = 'PBE'

endpoint_hosts = {
    BRAZIL: 'br1.api.riotgames.com',
    EUROPE_NORDIC_EAST: 'eun1.api.riotgames.com',
    EUROPE_WEST: 'euw1.api.riotgames.com',
    JAPAN: 'jp1.api.riotgames.com',
    KOREA: 'kr.api.riotgames.com',
    LATIN_AMERICA_NORTH: 'la1.api.riotgames.com',
    LATIN_AMERICA_SOUTH: 'la2.api.riotgames.com',
    NORTH_AMERICA: 'na1.api.riotgames.com',
    OCEANIA: 'oc1.api.riotgames.com',
    TURKEY: 'tr1.api.riotgames.com',
    RUSSIA: 'ru.api.riotgames.com',
    PBE: 'pbe1.api.riotgames.com'
}

# Platforms
platforms = {
    BRAZIL: 'BR1',
    EUROPE_NORDIC_EAST: 'EUN1',
    EUROPE_WEST: 'EUW1',
    JAPAN: 'JP1',
    KOREA: 'KR',
    LATIN_AMERICA_NORTH: 'LA1',
    LATIN_AMERICA_SOUTH: 'LA2',
    NORTH_AMERICA: 'NA1',
    OCEANIA: 'OC1',
    TURKEY: 'TR1',
    RUSSIA: 'RU',
    PBE: 'PBE1'
}

queue_types = [
    'CUSTOM',  # Custom games
    'NORMAL_5x5_BLIND',  # Normal 5v5 blind pick
    'BOT_5x5',  # Historical Summoners Rift coop vs AI games
    'BOT_5x5_INTRO',  # Summoners Rift Intro bots
    'BOT_5x5_BEGINNER',  # Summoner's Rift Coop vs AI Beginner Bot games
    'BOT_5x5_INTERMEDIATE',  # Historical Summoner's Rift Coop vs AI Intermediate Bot games
    'NORMAL_3x3',  # Normal 3v3 games
    'NORMAL_5x5_DRAFT',  # Normal 5v5 Draft Pick games
    'ODIN_5x5_BLIND',  # Dominion 5v5 Blind Pick games
    'ODIN_5x5_DRAFT',  # Dominion 5v5 Draft Pick games
    'BOT_ODIN_5x5',  # Dominion Coop vs AI games
    'RANKED_SOLO_5x5',  # Ranked Solo 5v5 games
    'RANKED_PREMADE_3x3',  # Ranked Premade 3v3 games
    'RANKED_PREMADE_5x5',  # Ranked Premade 5v5 games
    'RANKED_TEAM_3x3',  # Ranked Team 3v3 games
    'RANKED_TEAM_5x5',  # Ranked Team 5v5 games
    'BOT_TT_3x3',  # Twisted Treeline Coop vs AI games
    'GROUP_FINDER_5x5',  # Team Builder games
    'ARAM_5x5',  # ARAM games
    'ONEFORALL_5x5',  # One for All games
    'FIRSTBLOOD_1x1',  # Snowdown Showdown 1v1 games
    'FIRSTBLOOD_2x2',  # Snowdown Showdown 2v2 games
    'SR_6x6',  # Hexakill games
    'URF_5x5',  # Ultra Rapid Fire games
    'BOT_URF_5x5',  # Ultra Rapid Fire games played against AI games
    'NIGHTMARE_BOT_5x5_RANK1',  # Doom Bots Rank 1 games
    'NIGHTMARE_BOT_5x5_RANK2',  # Doom Bots Rank 2 games
    'NIGHTMARE_BOT_5x5_RANK5',  # Doom Bots Rank 5 games
    'ASCENSION_5x5',  # Ascension games
    'HEXAKILL',  # 6v6 games on twisted treeline
    'KING_PORO_5x5',  # King Poro game games
    'COUNTER_PICK',  # Nemesis games,
    'BILGEWATER_5x5',  # Black Market Brawlers games
]

game_maps = [
    {'map_id': 1, 'name': "Summoner's Rift", 'notes': "Summer Variant"},
    {'map_id': 2, 'name': "Summoner's Rift", 'notes': "Autumn Variant"},
    {'map_id': 3, 'name': "The Proving Grounds", 'notes': "Tutorial Map"},
    {'map_id': 4, 'name': "Twisted Treeline", 'notes': "Original Version"},
    {'map_id': 8, 'name': "The Crystal Scar", 'notes': "Dominion Map"},
    {'map_id': 10, 'name': "Twisted Treeline", 'notes': "Current Version"},
    {'map_id': 11, 'name': "Summoner's Rift", 'notes': "Current Version"},
    {'map_id': 12, 'name': "Howling Abyss", 'notes': "ARAM Map"},
    {'map_id': 14, 'name': "Butcher's Bridge", 'notes': "ARAM Map"},
]

game_modes = [
    'CLASSIC',  # Classic Summoner's Rift and Twisted Treeline games
    'ODIN',  # Dominion/Crystal Scar games
    'ARAM',  # ARAM games
    'TUTORIAL',  # Tutorial games
    'ONEFORALL',  # One for All games
    'ASCENSION',  # Ascension games
    'FIRSTBLOOD',  # Snowdown Showdown games
    'KINGPORO',  # King Poro games
]

game_types = [
    'CUSTOM_GAME',  # Custom games
    'TUTORIAL_GAME',  # Tutorial games
    'MATCHED_GAME',  # All other games
]

sub_types = [
    'NONE',  # Custom games
    'NORMAL',  # Summoner's Rift unranked games
    'NORMAL_3x3',  # Twisted Treeline unranked games
    'ODIN_UNRANKED',  # Dominion/Crystal Scar games
    'ARAM_UNRANKED_5v5',  # ARAM / Howling Abyss games
    'BOT',  # Summoner's Rift and Crystal Scar games played against AI
    'BOT_3x3',  # Twisted Treeline games played against AI
    'RANKED_SOLO_5x5',  # Summoner's Rift ranked solo queue games
    'RANKED_TEAM_3x3',  # Twisted Treeline ranked team games
    'RANKED_TEAM_5x5',  # Summoner's Rift ranked team games
    'ONEFORALL_5x5',  # One for All games
    'FIRSTBLOOD_1x1',  # Snowdown Showdown 1x1 games
    'FIRSTBLOOD_2x2',  # Snowdown Showdown 2x2 games
    'SR_6x6',  # Hexakill games
    'CAP_5x5',  # Team Builder games
    'URF',  # Ultra Rapid Fire games
    'URF_BOT',  # Ultra Rapid Fire games against AI
    'NIGHTMARE_BOT',  # Nightmare bots
    'ASCENSION',  # Ascension games
    'HEXAKILL',  # Twisted Treeline 6x6 Hexakill
    'KING_PORO',  # King Poro games
    'COUNTER_PICK',  # Nemesis games
    'BILGEWATER',  # Black Market Brawlers games
]

player_stat_summary_types = [
    'Unranked',  # Summoner's Rift unranked games
    'Unranked3x3',  # Twisted Treeline unranked games
    'OdinUnranked',  # Dominion/Crystal Scar games
    'AramUnranked5x5',  # ARAM / Howling Abyss games
    'CoopVsAI',  # Summoner's Rift and Crystal Scar games played against AI
    'CoopVsAI3x3',  # Twisted Treeline games played against AI
    'RankedSolo5x5',  # Summoner's Rift ranked solo queue games
    'RankedTeams3x3',  # Twisted Treeline ranked team games
    'RankedTeams5x5',  # Summoner's Rift ranked team games
    'OneForAll5x5',  # One for All games
    'FirstBlood1x1',  # Snowdown Showdown 1x1 games
    'FirstBlood2x2',  # Snowdown Showdown 2x2 games
    'SummonersRift6x6',  # Hexakill games
    'CAP5x5',  # Team Builder games
    'URF',  # Ultra Rapid Fire games
    'URFBots',  # Ultra Rapid Fire games played against AI
    'NightmareBot',  # Summoner's Rift games played against Nightmare AI
    'Hexakill',  # Twisted Treeline 6x6 Hexakill games
    'KingPoro',  # King Poro games
    'CounterPick',  # Nemesis games
    'Bilgewater',  # Black Market Brawlers games
]

solo_queue, ranked_5s, ranked_3s = 'RANKED_SOLO_5x5', 'RANKED_TEAM_5x5', 'RANKED_TEAM_3x3'

preseason_3, season_3, preseason_2014, season_2014, preseason_2015, season_2015, preseason_2016, season_2016 = [
    'PRESEASON3', 'SEASON3',
    'PRESEASON2014', 'SEASON2014',
    'PRESEASON2015', 'SEASON2015',
    'PRESEASON2016', 'SEASON2016',
]

api_versions = {
    'champion': 1.2,
    'current-game': 1.0,
    'featured-games': 1.0,
    'game': 1.3,
    'league': 2.5,
    'lol-static-data': 1.2,
    'lol-status': 1.0,
    'matchlist': 2.2,
    'stats': 1.3,
    'summoner': 'v3',
    'spectator': 'v3',
    'match': 'v3',
    'team': 2.4
}


class LoLException(Exception):
    def __init__(self, error, response):
        self.error = error
        self.headers = response.headers

    def __str__(self):
        return self.error

    def __eq__(self, other):
        if isinstance(other, "".__class__):
            return self.error == other
        elif isinstance(other, self.__class__):
            return self.error == other.error and self.headers == other.headers
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return super(LoLException).__hash__()


error_400 = "Bad request"
error_401 = "Unauthorized"
error_403 = "Blacklisted key"
error_404 = "Game data not found"
error_429 = "Too many requests"
error_500 = "Internal server error"
error_503 = "Service unavailable"
error_504 = 'Gateway timeout'


def raise_status(response):
    if response.status_code == 400:
        raise LoLException(error_400, response)
    elif response.status_code == 401:
        raise LoLException(error_401, response)
    elif response.status_code == 403:
        raise LoLException(error_403, response)
    elif response.status_code == 404:
        raise LoLException(error_404, response)
    elif response.status_code == 429:
        raise LoLException(error_429, response)
    elif response.status_code == 500:
        raise LoLException(error_500, response)
    elif response.status_code == 503:
        raise LoLException(error_503, response)
    elif response.status_code == 504:
        raise LoLException(error_504, response)
    else:
        response.raise_for_status()


class RateLimit:
    def __init__(self, allowed_requests, seconds):
        self.allowed_requests = allowed_requests
        self.seconds = seconds
        self.made_requests = deque()

    def __reload(self):
        t = time.time()
        while len(self.made_requests) > 0 and self.made_requests[0] < t:
            self.made_requests.popleft()

    def add_request(self):
        self.made_requests.append(time.time() + self.seconds)

    def request_available(self):
        self.__reload()
        return len(self.made_requests) < self.allowed_requests


class RiotWatcher:
    def __init__(self, key, default_region=NORTH_AMERICA, limits=(RateLimit(10, 10), RateLimit(500, 600),)):
        self.key = key  # If you have a production key, use limits=(RateLimit(3000,10), RateLimit(180000,600),)
        self.default_region = default_region
        self.limits = limits

    def can_make_request(self):
        for lim in self.limits:
            if not lim.request_available():
                return False
        return True

    def base_request(self, url, region, static=False, **kwargs):
        """
        Base request for the API
        :param url: url to the target request
        :return: JSON returned by the Riot API
        """
        if region is None:
            region = self.default_region
        args = {'api_key': self.key}
        for k in kwargs:
            if kwargs[k] is not None:
                args[k] = kwargs[k]
        r = requests.get(
            'https://{endpoint}/{url}'.format(
                endpoint=endpoint_hosts[region],
                url=url
            ),
            params=args
        )
        if not static:
            for lim in self.limits:
                lim.add_request()
        raise_status(r)
        return r.json()

    @staticmethod
    def sanitized_name(name):
        """
        Put summoner name in the appropriate format to send to API
        """
        return urllib.parse.quote_plus(name.replace(' ', '').lower())

    def get_match_ids_by_tournament(self, tournament_code, region=None):
        """
        Get match IDs by tournament code.
        match v3
        """
        if tournament_code is not None:
            return self.base_request(
                'lol/match/{version}/matches/by-tournament-code/{tournament_code}/ids'.format(
                    version=api_versions['match'],
                    tournament_code=tournament_code
                ),
                region
            )
        return None

    def get_match(self, match_id, region=None):
        """
        Get match by match ID.
        match v3
        """
        if match_id is not None:
            return self.base_request(
                'lol/match/{version}/matches/{match_id}'.format(
                    version=api_versions['match'],
                    match_id=match_id
                ),
                region
            )
        return None

    def get_match_timeline(self, match_id, region=None):
        """
        Get match timeline by match ID.
        match v3
        """
        if match_id is not None:
            return self.base_request(
                'lol/match/v3/timelines/by-match/{match_id}'.format(
                    version=api_versions['match'],
                    match_id=match_id
                ),
                region
            )
        return None

    def get_match_by_id_and_tournament_code(self, _id, tournament_code, region=None):
        """
        Get match by match ID and tournament code.
        match v3
        """
        if _id is not None and tournament_code is not None:
            return self.base_request(
                'lol/match/{version}/matches/{match_id}/by-tournament-code/{tournament_code}/ids'.format(
                    version=api_versions['match'],
                    match_id=_id,
                    tournament_code=tournament_code
                ),
                region
            )
        return None

    def get_match_list(self, account_id, queue_ids=None, season_ids=None, champion_ids=None,
                       begin_time=None, end_time=None, begin_index=None, end_index=None, region=None):
        """
        Get matchlist for ranked games played on given account ID and platform ID and filtered
        using given filter parameters, if any.
        match v3
        """
        if account_id is not None:
            return self.base_request(
                'lol/match/{version}/matchlists/by-account/{account_id}'.format(
                    version=api_versions['match'],
                    account_id=account_id,
                ),
                region,
                queue=queue_ids,
                season=season_ids,
                champion=champion_ids,
                beginTime=begin_time,
                endTime=end_time,
                beginIndex=begin_index,
                endIndex=end_index
            )
        return None

    def get_recent_match_list(self, account_id, region=None):
        """
        Get matchlist for last 20 matches played on given account ID and platform ID.
        """
        if account_id is not None:
            return self.base_request(
                'lol/match/{version}/matchlists/by-account/{account_id}/recent'.format(
                    version=api_versions['match'],
                    account_id=account_id,
                ),
                region,
            )
        return None




    # champion-v1.2
    def _champion_request(self, end_url, region, **kwargs):
        return self.base_request(
            'v{version}/champion/{end_url}'.format(
                version=api_versions['champion'],
                end_url=end_url
            ),
            region,
            **kwargs
        )

    def get_all_champions(self, region=None, free_to_play=False):
        return self._champion_request('', region, freeToPlay=free_to_play)

    def get_champion(self, champion_id, region=None):
        return self._champion_request('{id}'.format(id=champion_id), region)

    def get_current_game(self, summoner_id, region=None):
        """
        Get current game for a summoner.
        spectator v3
        """
        return self.base_request(
            'lol/spectator/{version}/active-games/by-summoner/{summoner_id}'.format(
                version=api_versions['spectator'],
                summoner_id=summoner_id
            ),
            region
        )

    def get_featured_games(self, region=None):
        """
        Get featured games.
        spectator v3
        """
        return self.base_request('lol/spectator/{version}/featured-games'.format(
                version=api_versions['spectator']
            ),
            region
        )

    # game-v1.3
    def _game_request(self, end_url, region, **kwargs):
        return self.base_request(
            'v{version}/game/{end_url}'.format(
                version=api_versions['game'],
                end_url=end_url
            ),
            region,
            **kwargs
        )

    # league-v2.5
    def _league_request(self, end_url, region, **kwargs):
        return self.base_request(
            'v{version}/league/{end_url}'.format(
                version=api_versions['league'],
                end_url=end_url
            ),
            region,
            **kwargs
        )

    def get_league(self, summoner_ids=None, team_ids=None, region=None):
        """summoner_ids and team_ids arguments must be iterable, only one should be specified, not both"""
        if (summoner_ids is None) != (team_ids is None):
            if summoner_ids is not None:
                return self._league_request(
                    'by-summoner/{summoner_ids}'.format(summoner_ids=','.join([str(s) for s in summoner_ids])),
                    region
                )
            else:
                return self._league_request(
                    'by-team/{team_ids}'.format(team_ids=','.join([str(t) for t in team_ids])),
                    region
                )

    def get_league_entry(self, summoner_ids=None, team_ids=None, region=None):
        """summoner_ids and team_ids arguments must be iterable, only one should be specified, not both"""
        if (summoner_ids is None) != (team_ids is None):
            if summoner_ids is not None:
                return self._league_request(
                    'by-summoner/{summoner_ids}/entry'.format(
                        summoner_ids=','.join([str(s) for s in summoner_ids])
                    ),
                    region
                )
            else:
                return self._league_request(
                    'by-team/{team_ids}/entry'.format(team_ids=','.join([str(t) for t in team_ids])),
                    region
                )

    def get_challenger(self, region=None, queue=solo_queue):
        return self._league_request('challenger', region, type=queue)

    def get_master(self, region=None, queue=solo_queue):
        return self._league_request('master', region, type=queue)

    # lol-static-data-v1.2
    def _static_request(self, end_url, region, **kwargs):
        return self.base_request(
            'v{version}/{end_url}'.format(
                version=api_versions['lol-static-data'],
                end_url=end_url
            ),
            region,
            static=True,
            **kwargs
        )

    def static_get_champion_list(self, region=None, locale=None, version=None, data_by_id=None, champ_data=None):
        return self._static_request(
            'champion',
            region,
            locale=locale,
            version=version,
            dataById=data_by_id,
            champData=champ_data
        )

    def static_get_champion(self, champ_id, region=None, locale=None, version=None, champ_data=None):
        return self._static_request(
            'champion/{id}'.format(id=champ_id),
            region,
            locale=locale,
            version=version,
            champData=champ_data
        )

    def static_get_item_list(self, region=None, locale=None, version=None, item_list_data=None):
        return self._static_request('item', region, locale=locale, version=version, itemListData=item_list_data)

    def static_get_item(self, item_id, region=None, locale=None, version=None, item_data=None):
        return self._static_request(
            'item/{id}'.format(id=item_id),
            region,
            locale=locale,
            version=version,
            itemData=item_data
        )

    def static_get_mastery_list(self, region=None, locale=None, version=None, mastery_list_data=None):
        return self._static_request(
            'mastery',
            region,
            locale=locale,
            version=version,
            masteryListData=mastery_list_data
        )

    def static_get_mastery(self, mastery_id, region=None, locale=None, version=None, mastery_data=None):
        return self._static_request(
            'mastery/{id}'.format(id=mastery_id),
            region,
            locale=locale,
            version=version,
            masteryData=mastery_data
        )

    def static_get_realm(self, region=None):
        return self._static_request('realm', region)

    def static_get_rune_list(self, region=None, locale=None, version=None, rune_list_data=None):
        return self._static_request('rune', region, locale=locale, version=version, runeListData=rune_list_data)

    def static_get_rune(self, rune_id, region=None, locale=None, version=None, rune_data=None):
        return self._static_request(
            'rune/{id}'.format(id=rune_id),
            region,
            locale=locale,
            version=version,
            runeData=rune_data
        )

    def static_get_summoner_spell_list(self, region=None, locale=None, version=None, data_by_id=None, spell_data=None):
        return self._static_request(
            'summoner-spell',
            region,
            locale=locale,
            version=version,
            dataById=data_by_id,
            spellData=spell_data
        )

    def static_get_summoner_spell(self, spell_id, region=None, locale=None, version=None, spell_data=None):
        return self._static_request(
            'summoner-spell/{id}'.format(id=spell_id),
            region,
            locale=locale,
            version=version,
            spellData=spell_data
        )

    def static_get_versions(self, region=None):
        return self._static_request('versions', region)

    # match-v2.2
    def _match_request(self, end_url, region, **kwargs):
        return self.base_request(
            'v{version}/match/{end_url}'.format(
                version=api_versions['match'],
                end_url=end_url
            ),
            region,
            **kwargs
        )

    # lol-status-v1.0
    @staticmethod
    def get_server_status(region=None):
        if region is None:
            url = 'shards'
        else:
            url = 'shards/{region}'.format(region=region)
        r = requests.get('http://status.leagueoflegends.com/{url}'.format(url=url))
        raise_status(r)
        return r.json()

    # match list-v2.2
    def _match_list_request(self, end_url, region, **kwargs):
        return self.base_request(
            'v{version}/matchlist/by-summoner/{end_url}'.format(
                version=api_versions['matchlist'],
                end_url=end_url,
            ),
            region,
            **kwargs
        )

    # stats-v1.3
    def _stats_request(self, end_url, region, **kwargs):
        return self.base_request(
            'v{version}/stats/{end_url}'.format(
                version=api_versions['stats'],
                end_url=end_url
            ),
            region,
            **kwargs
        )

    def get_stat_summary(self, summoner_id, region=None, season=None):
        return self._stats_request(
            'by-summoner/{summoner_id}/summary'.format(summoner_id=summoner_id),
            region,
            season='SEASON{}'.format(season) if season is not None else None)

    def get_ranked_stats(self, summoner_id, region=None, season=None):
        return self._stats_request(
            'by-summoner/{summoner_id}/ranked'.format(summoner_id=summoner_id),
            region,
            season='SEASON{}'.format(season) if season is not None else None
        )

    # summoner-v3
    def _summoner_request(self, end_url, region, **kwargs):
        return self.base_request(
            'lol/summoner/{version}/summoners/{end_url}'.format(
                version=api_versions['summoner'],
                end_url=end_url
            ), region, **kwargs
        )

    def get_mastery_pages(self, summoner_ids, region=None):
        return self._summoner_request(
            '{summoner_ids}/masteries'.format(summoner_ids=','.join([str(s) for s in summoner_ids])),
            region
        )

    def get_rune_pages(self, summoner_ids, region=None):
        return self._summoner_request(
            '{summoner_ids}/runes'.format(summoner_ids=','.join([str(s) for s in summoner_ids])),
            region
        )

    def get_summoner_by_account_id(self, _id, region=None):
        """
            Get Summoner by account id
            version: summoner-v3
        """
        if id is not None:
            return self._summoner_request(
                'by-account/{account_id}'.format(account_id=str(_id)),
                region
            )
        return None

    def get_summoner_by_name(self, name, region=None):
        """
            Get Summoner by name
            version: summoner-v3
        """
        if name is not None:
            return self._summoner_request(
                'by-name/{summoner_name}'.format(summoner_name=self.sanitized_name(name)),
                region
            )
        return None

    def get_summoner_by_id(self, _id, region=None):
        """
            Get Summoner by id
            version: summoner-v3
        """
        if _id is not None:
            return self._summoner_request(
                '{summoner_id}'.format(summoner_id=str(_id)),
                region
            )
        return None


    # team-v2.4
    def _team_request(self, end_url, region, **kwargs):
        return self.base_request(
            'v{version}/team/{end_url}'.format(
                version=api_versions['team'],
                end_url=end_url
            ),
            region,
            **kwargs
        )

    def get_teams_for_summoner(self, summoner_id, region=None):
        return self.get_teams_for_summoners([summoner_id, ], region=region)[str(summoner_id)]

    def get_teams_for_summoners(self, summoner_ids, region=None):
        return self._team_request(
            'by-summoner/{summoner_id}'.format(summoner_id=','.join([str(s) for s in summoner_ids])),
            region
        )

    def get_team(self, team_id, region=None):
        return self.get_teams([team_id, ], region=region)[str(team_id)]

    def get_teams(self, team_ids, region=None):
        return self._team_request('{team_ids}'.format(team_ids=','.join(str(t) for t in team_ids)), region)
