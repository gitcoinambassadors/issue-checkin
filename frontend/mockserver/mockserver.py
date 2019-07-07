import flask
import flask_cors
import sqlite3 
import json
import datetime

from flask import request

def loadBountyItems(lastCheckInSinceDays):
    bountyPreload = []
    conn = sqlite3.connect("mockserver.sqlite3")
    conn_c = conn.cursor()

    # god bless https://medium.com/@PyGuyCharles/python-sql-to-json-and-beyond-3e3a36d32853
    itms = [dict(zip([key[0] for key in conn_c.description], row)) for row in conn_c.execute("select * from bountiesSync").fetchall()]
    for itm in itms:
        if itm["date_last_reviewed"] == None or lastCheckInSinceDays == -1 or (datetime.datetime.now() - datetime.datetime.strptime(itm["date_last_reviewed"],"%Y-%m-%d %H:%M:%S.%f")).days > lastCheckInSinceDays:
            bountyPreload.append(itm)
    
    conn_c.close()
    conn.close()
    return bountyPreload

def updateBountyOnDB(stdbtyid):
    conn = sqlite3.connect("mockserver.sqlite3")
    print("UPDATE bountiesSync SET date_last_reviewed = ? WHERE standard_bounties_id = ?")
    print((str(datetime.datetime.now()), stdbtyid))
    conn.execute("UPDATE bountiesSync SET date_last_reviewed = ? WHERE standard_bounties_id = ?", (str(datetime.datetime.now()), int(stdbtyid)))
    conn.commit()
    conn.close()
    return ""



app = flask.Flask("app")
cors = flask_cors.CORS(app)

@app.route('/api/v1/checkin/bounties', methods=['GET'])
def getBounties():
    lastCheckInSinceDays = request.args.get('lastCheckInSinceDays', default = 7, type = int)
    return json.dumps(loadBountyItems(lastCheckInSinceDays))

@app.route('/api/v1/checkin/bounties', methods=['POST'])
def updateBountiesCheckInDate():
    for vals in request.values:
        print(f'{vals} - {request.values[vals]}')
    if request.values["standard_bounties_id"] != None:
        updateBountyOnDB(request.values["standard_bounties_id"])
    return {"status": "OK"}


app.run(port=8000)

print("shutting down...")