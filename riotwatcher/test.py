import time

from riotwatcher import RiotWatcher

key = '<key>'
summoner_name = 'Bandejão'

w = RiotWatcher(key, default_region='BR')


def wait():
    while not w.can_make_request():
        time.sleep(1)


def summoner_test(summ_name):
    wait()
    summoner = w.get_summoner_by_name(summ_name)
    wait()
    w.get_summoner_by_id(summoner['id'])
    wait()
    w.get_summoner_by_account_id(summoner['accountId'])


def spectate_test():
    wait()
    featured_games = w.get_featured_games()
    wait()
    sample_player_name = featured_games['gameList'][0]['participants'][0]['summonerName']
    summoner_id = w.get_summoner_by_name(sample_player_name)['id']
    wait()
    w.get_current_game(summoner_id)


def match_test(summ_name):
    account_id = w.get_summoner_by_name(summ_name)['accountId']

    sample_match_id = w.get_recent_match_list(account_id)['matches'][0]['gameId']
    w.get_match(sample_match_id)
    w.get_match_timeline(sample_match_id)

    w.get_match_list(account_id, queue_ids=None, season_ids=None, champion_ids=None,
                     begin_time=None, end_time=None, begin_index=None, end_index=None)


# def tournament_match_test():
#    w.get_match_ids_by_tournament(tournament_code)
#    w.get_match_by_id_and_tournament_code(_id, tournament_code)


def main():
    print('Initiating tests...')
    summoner_test(summoner_name)
    print('summoner test passed.')
    spectate_test()
    print('spectate test passed.')
    match_test(summoner_name)
    print('match test passed.')
    print('all tests passed, w00t. if only they were better tests...')


if __name__ == '__main__':
    main()
