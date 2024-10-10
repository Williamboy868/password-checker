import requests
import hashlib
import sys

def request_api_data(query):
    url = 'https://api.pwnedpasswords.com/range/' + query
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f'you got a response of {response} which shows there is a problem with your request api data')
    return response


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
        return 0

def pwned_api_check(password):
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first_5, tail = sha1_password[:5], sha1_password[5:]
    response = request_api_data(first_5)
    return get_password_leaks_count(response, tail)

pwned_api_check("shit")

def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count > 0:
            print(f'{password}has been hacked {count} times so I reccommend, you change your password!')
        else:
            print(f'There were no records found on {password},you can use it')
main(sys.argv[1:])
