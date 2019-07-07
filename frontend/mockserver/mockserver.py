import flask
import flask_cors
import urllib.request, json 

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
            "standard_bounties_id": obj["standard_bounties_id"]

        }
        bountyPreload.append(i)
        print("Bounty: "+json.dumps(i))

app = flask.Flask("app")
cors = flask_cors.CORS(app)

@app.route('/api/v1/checkin/bounties')
def getBounties():
    return json.dumps(bountyPreload)

app.run(port=8000)