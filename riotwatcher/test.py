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
    summ = w.get_summoner_by_name(summ_name)
    wait()
    w.get_summoner_by_id(summ['id'])
    wait()
    w.get_summoner_by_account_id(summ['accountId'])


def main():
    print('Initiating tests...')
    summoner_test(summoner_name)
    print('summoner test passed')
    print('all tests passed, w00t. if only they were better tests...')


if __name__ == '__main__':
    main()
