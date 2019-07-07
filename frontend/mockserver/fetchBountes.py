import urllib.request, json 
import sqlite3 

conn = sqlite3.connect("mockserver.sqlite3")
conn_c = conn.cursor()

if len(conn_c.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'bountiesSync'").fetchall()) <= 0:
    # create database
    conn_c.execute("create table bountiesSync(bounty_url, founded_by, status, github_url, date_last_reviewed, title, created_on, standard_bounties_id, last_reviewed_by)")
    conn.commit()

 
bountyPreload = []
with urllib.request.urlopen("https://gitcoin.co/api/v0.1/bounties/?format=json") as url:
    data = json.loads(url.read().decode())
    for obj in data:
        i = {
            "bounty_url": obj["url"],
            "founded_by": f'{obj["bounty_owner_name"]} (GitHub: {obj["bounty_owner_github_username"]})',
            "status": obj["status"],
            "github_url": obj["github_url"],
            "date_last_reviewed": None,
            "title": obj["title"],
            "created_on": obj["created_on"],
            "standard_bounties_id": obj["standard_bounties_id"],
            "last_reviewed_by": None
        }
        if len(conn_c.execute("select standard_bounties_id from bountiesSync where standard_bounties_id=?", (obj["standard_bounties_id"],) ).fetchall()) <= 0:
            conn_c.execute("INSERT INTO bountiesSync VALUES (?,?,?,?,?,?,?,?,?)",
                ( i["bounty_url"],
                  i["founded_by"],
                  i["status"],
                  i["github_url"],
                  i["date_last_reviewed"],
                  i["title"],
                  i["created_on"],
                  i["standard_bounties_id"],
                  i["last_reviewed_by"]
                )
            )
        bountyPreload.append(i)
        print("Bounty: "+json.dumps(i))

conn.commit()
