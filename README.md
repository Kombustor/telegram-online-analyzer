# Telegram Online Analyzer (WIP)
This project uses the Telegram MTProto API (using [Pyrogram](https://docs.pyrogram.ml/)) to collect and analyze the online status of a user's contacts.

## Setup
Use docker-compose and run `docker-compose up` in the main directory to run the collector & a mariadb database. 

## Roadmap
- [X] Collect and store data
- [ ] Analyze data (WIP)

## Disclaimer
This is only a proof-of-concept project. It should only be used under test conditions, and to monitor contacts whose permission has been obtained. I assume no liability for any damages.
