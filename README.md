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
# Install ubuntu dependencies
apt-get update
apt-get install python3
apt install python3.12-venv -y
# Clone the repo
git clone https://<fine-grained-token>@github.com/GeorgeNagel/childcare-vt-search.git
cd childcare-vt-search
# Create virtualenv
python3 -m venv venv
# Install dependencies
source venv/bin/activate
(venv) pip install -r requirements.txt
```

## Update crontab
`crontab -e`

## Test the script
`python3 collect_site_urls.py`

## TODO
- Cron job to run scraper daily
- Cron job to run aggregator daily
- Cron job to push data to github daily
- Make Github token
- Make Github page to chart data
