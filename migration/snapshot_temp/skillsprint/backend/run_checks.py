import json, urllib.request, sys

def do_request(method, url, headers=None, data=None):
    if headers is None: headers={}
    req = urllib.request.Request(url, data=(data.encode() if isinstance(data, str) else data), headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            print(f"== {method} {url} -> {r.status}")
            for k,v in r.getheaders():
                print(f"{k}: {v}")
            body = r.read()
            if body:
                try:
                    print(body.decode())
                except:
                    print(repr(body[:200]))
    except Exception as e:
        print(f"ERROR {method} {url}:", e)

# load token
try:
    tok = json.load(open('token.json'))
    access = tok.get('access_token','')
except Exception as e:
    print('Failed to load token.json:', e)
    access = ''

origin = 'http://localhost:5173'

# OPTIONS preflight for /users/me
print('\n--- PREFLIGHT /users/me')
do_request('OPTIONS', 'http://127.0.0.1:8000/api/v1/users/me', headers={
    'Origin': origin,
    'Access-Control-Request-Method': 'GET',
    'Access-Control-Request-Headers': 'authorization,content-type'
})

# GET /users/me with token
print('\n--- GET /users/me')
headers = {'Origin': origin}
if access:
    headers['Authorization'] = f'Bearer {access}'
do_request('GET', 'http://127.0.0.1:8000/api/v1/users/me', headers=headers)

# OPTIONS preflight for /leaderboard
print('\n--- PREFLIGHT /leaderboard')
do_request('OPTIONS', 'http://127.0.0.1:8000/api/v1/leaderboard/', headers={
    'Origin': origin,
    'Access-Control-Request-Method': 'GET',
    'Access-Control-Request-Headers': 'authorization,content-type'
})

# GET leaderboard
print('\n--- GET /leaderboard')
do_request('GET', 'http://127.0.0.1:8000/api/v1/leaderboard/', headers=headers)
