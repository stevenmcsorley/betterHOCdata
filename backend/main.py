from flask import Flask, jsonify
from scraper import scrape_members_data
import pymysql.cursors
from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def update_members_data():
    data = scrape_members_data()

    # Store the data in MySQL
    connection = pymysql.connect(
        host='db',
        user='root',
        password='password',
        db='members_data',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    with connection.cursor() as cursor:
        # Delete any existing data
        cursor.execute("TRUNCATE TABLE members;")

        # Insert the new data
        for member in data:
            query = """
            INSERT INTO members (
                member_id,
                nameListAs,
                nameDisplayAs,
                nameFullTitle,
                nameAddressAs,
                latestPartyId,
                latestPartyName,
                latestPartyAbbreviation,
                latestPartyBackgroundColour,
                latestPartyForegroundColour,
                latestPartyIsLordsMainParty,
                latestPartyIsLordsSpiritualParty,
                latestPartyGovernmentType,
                latestPartyIsIndependentParty,
                gender,
                membershipFrom,
                membershipFromId,
                house,
                membershipStartDate,
                membershipEndDate,
                membershipEndReason,
                membershipEndReasonNotes,
                membershipEndReasonId,
                membershipStatusIsActive,
                membershipStatusDescription,
                membershipStatusNotes,
                membershipStatusId,
                membershipStatus,
                membershipStatusStartDate,
                thumbnailUrl
            ) VALUES (
                %(id)s,
                %(nameListAs)s,
                %(nameDisplayAs)s,
                %(nameFullTitle)s,
                %(nameAddressAs)s,
                %(latestPartyId)s,
                %(latestPartyName)s,
                %(latestPartyAbbreviation)s,
                %(latestPartyBackgroundColour)s,
                %(latestPartyForegroundColour)s,
                %(latestPartyIsLordsMainParty)s,
                %(latestPartyIsLordsSpiritualParty)s,
                %(latestPartyGovernmentType)s,
                %(latestPartyIsIndependentParty)s,
                %(gender)s,
                %(membershipFrom)s,
                %(membershipFromId)s,
                %(house)s,
                %(membershipStartDate)s,
                %(membershipEndDate)s,
                %(membershipEndReason)s,
                %(membershipEndReasonNotes)s,
                %(membershipEndReasonId)s,
                %(membershipStatusIsActive)s,
                %(membershipStatusDescription)s,
                %(membershipStatusNotes)s,
                %(membershipStatusId)s,
                %(membershipStatus)s,
                %(membershipStatusStartDate)s,
                %(thumbnailUrl)s
            );
        """


            cursor.execute(query, member["value"])

    connection.commit()
    connection.close()

@app.route('/api/members')
def get_members_data():
    connection = pymysql.connect(
        host='db',
        user='root',
        password='password',
        db='members_data',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    with connection.cursor() as cursor:
        # Retrieve the members data
        cursor.execute("SELECT * FROM members;")
        data = cursor.fetchall()

    connection.close()

    return jsonify(data)

@app.route('/api/members/<int:member_id>/votes/<int:vote_type>')
def get_member_votes_by_type(member_id, vote_type):
    if vote_type not in [0, 1]:
        return jsonify({"error": "Invalid vote type. Allowed values: 0 (No), 1 (Yes)"}), 400

    connection = pymysql.connect(
        host='db',
        user='root',
        password='password',
        db='members_data',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    with connection.cursor() as cursor:
        query = "SELECT * FROM membervoting WHERE member_id=%s AND member_voted_aye=%s;"
        cursor.execute(query, (member_id, vote_type))
        votes = cursor.fetchall()

    connection.close()

    return jsonify(votes)





@app.route('/api/members/status/<status>')
def get_members_by_status(status):
    connection = pymysql.connect(
        host='db',
        user='root',
        password='password',
        db='members_data',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    with connection.cursor() as cursor:
        # Retrieve the members data with the given status
        query = "SELECT * FROM members WHERE membershipEndReason=%s;"
        cursor.execute(query, status)
        data = cursor.fetchall()

    connection.close()

    return jsonify(data)

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_members_data, 'interval', hours=24)
    scheduler.start()

    # Update the data when the server starts

    app.run(host='0.0.0.0', port=5000)
