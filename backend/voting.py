import requests
import json
import math
import mysql.connector

# Database connection
db = mysql.connector.connect(
    host="db",
    user="root",
    password="password",
    database="members_data"
)
cursor = db.cursor()

# Fetch all Member IDs from the 'members' table
cursor.execute("SELECT member_id FROM members ORDER BY member_id DESC")
member_ids = [member_id[0] for member_id in cursor.fetchall()]
member_ids.sort(reverse=True)

# Define function to fetch voting data
def fetch_voting_data(member_id):
    print(f"Processing Member ID: {member_id}")
    url = f"https://commonsvotes-api.parliament.uk/data/divisions.json/membervoting?queryParameters.memberId={member_id}"
    response = requests.get(url)
    data = json.loads(response.text)
    return data

# Iterate through all Member IDs
# Iterate through all Member IDs
for member_id in member_ids:
    # Get voting data for the member
    data = fetch_voting_data(member_id)

    # Check if the data is empty
    if not data:
        print(f"No data found for Member ID: {member_id}")
        continue
    
    # Save voting data to MySQL
    for item in data:
        member_voting = item
        published_division = item["PublishedDivision"]
        
        division_id = published_division["DivisionId"]
        date = published_division["Date"]
        title = published_division["Title"]
        member_voted_aye = member_voting["MemberVotedAye"]
        member_was_teller = member_voting["MemberWasTeller"]
        
        # Insert or update record in the 'membervoting' table
        cursor.execute("""
            INSERT INTO membervoting (member_id, division_id, date, title, member_voted_aye, member_was_teller)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                date = VALUES(date),
                title = VALUES(title),
                member_voted_aye = VALUES(member_voted_aye),
                member_was_teller = VALUES(member_was_teller)
        """, (member_id, division_id, date, title, member_voted_aye, member_was_teller))
        db.commit()
    print(f"Finished processing Member ID: {member_id}")
cursor.close()
db.close()

