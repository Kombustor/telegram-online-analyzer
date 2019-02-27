import pyrogram
import schedule
import time
import pandas as pd

from collect.code.collector import fetch_users
from utils.database import Database

query_create = "CREATE TABLE IF NOT EXISTS `onlineData` (\
    `time` VARCHAR(10) NOT NULL,\
    `userId` INT NOT NULL,\
    `name_first` TEXT,\
    `name_last` TEXT,\
    `name_user` TEXT,\
    `phone` TEXT,\
    `status` TEXT,\
    `status_was_online` INT,\
    PRIMARY KEY (`time`, `userId`) \
)\
DEFAULT CHARACTER SET utf8 \
COLLATE utf8_general_ci\
;"


def main():
    # Initialize db & scheduler
    db = Database('./config.ini')
    db.query(query_create)
    scheduler = schedule.Scheduler()

    # Create telegram API client & start it
    app = pyrogram.Client("data-collector")
    app.start()

    # Run process_users every 10 seconds
    scheduler.every(10).seconds.do(process_users, app, db)

    while True:
        scheduler.run_pending()
        time.sleep(1)


def process_users(app, db):
    # Fetch users
    users = fetch_users(app)

    # Insert users into database
    insert_users(db, users)

    pd_users = pd.DataFrame(users)
    print(pd_users.loc[pd_users['status'] == 'online'])


def insert_users(db, users):
    if len(users) == 0:
        return

    # Create & run insert query
    for user in users:
        placeholder = ", ".join(["%s"] * len(user))
        stmt = "INSERT INTO `{table}` ({columns}) VALUES ({values});".format(
            table=db.table_name,
            columns=",".join(user.keys()),
            values=placeholder
        )
        db.query(stmt, list(user.values()))


if __name__ == '__main__':
    main()
