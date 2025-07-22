# Setup
```
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
## Create a token with scoped read/write access for the Droplet
Go to GitHub → Settings → Developer Settings → Personal Access Tokens → Fine-grained Tokens
Create a token with:
    Access to the repo
    Repo permissions: Read & Write
    Scope only to the specific repo if possible
Save the token (you won’t see it again)

## Access droplet
`ssh root@<ip>`

## Setup droplet
```bash
apt-get update
apt-get install python3
git clone https://<fine-grained-token>@github.com/GeorgeNagel/childcare-vt-search.git
cd childcare-vt-search
```

## TODO
- Deploy scraper to Droplet
- Cron job to run scraper daily
- Cron job to run aggregator daily
- Cron job to push data to github daily
- Make Github token
- Make Github page to chart data