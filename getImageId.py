import requests
import json
import os

app = os.environ['app']
auth = (f'https://auth.docker.io/token?scope=repository:srqtn/{app}:' +
        'pull&service=registry.docker.io')
token = requests.get(url=auth).json()['token']


headers = {
    'Accept': 'application/vnd.docker.distribution.manifest.v2+json',
    'Authorization': f'Bearer {token}'
}

manifest = 'https://registry-1.docker.io/v2/srqtn/docker-py/manifests/latest'
r = requests.get(url=manifest,
                 headers=headers)

print(r.json()['config']['digest'])
