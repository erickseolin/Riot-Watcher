import time

from riotwatcher import RiotWatcher

key = '<key>'
summoner_name = 'GorilaMineira'

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


def main():
    print('Initiating tests...')
    summoner_test(summoner_name)
    print('summoner test passed')
    spectate_test()
    print('spectate test passed')

    print('all tests passed, w00t. if only they were better tests...')


if __name__ == '__main__':
    main()
