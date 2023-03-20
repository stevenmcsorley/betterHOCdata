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
cursor.execute("SELECT id FROM members")
member_ids = [member_id[0] for member_id in cursor.fetchall()]

# Define function to fetch voting data
def fetch_voting_data(member_id, page):
    url = f"https://members-api.parliament.uk/api/Members/{member_id}/Voting?house=1&page={page}"
    response = requests.get(url)
    data = json.loads(response.text)
    return data

# Iterate through all Member IDs
for member_id in member_ids:
    # Get first page of voting data for the member
    data = fetch_voting_data(member_id, 1)
    total_results = data["totalResults"]
    results_per_page = data["take"]
    total_pages = math.ceil(total_results / results_per_page)

    # Loop through all pages of voting data for the member
    for page in range(1, total_pages + 1):
        if page > 1:
            data = fetch_voting_data(member_id, page)
        
        # Save voting data to MySQL
        for item in data["items"]:
            vote_data = item["value"]
            vote_id = vote_data["id"]
            house = vote_data["house"]
            in_affirmative_lobby = vote_data["inAffirmativeLobby"]
            acted_as_teller = vote_data["actedAsTeller"]
            title = vote_data["title"]
            date = vote_data["date"]
            division_number = vote_data["divisionNumber"]
            number_in_favour = vote_data["numberInFavour"]
            number_against = vote_data["numberAgainst"]

            # Insert or update record in the 'member_votes' table
            cursor.execute("""
                INSERT INTO member_votes (division_id, member_id, house, in_affirmative_lobby, acted_as_teller, title, date, division_number, number_in_favour, number_against)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    house = VALUES(house),
                    in_affirmative_lobby = VALUES(in_affirmative_lobby),
                    acted_as_teller = VALUES(acted_as_teller),
                    title = VALUES(title),
                    date = VALUES(date),
                    division_number = VALUES(division_number),
                    number_in_favour = VALUES(number_in_favour),
                    number_against = VALUES(number_against)
            """, (vote_id, member_id, house, in_affirmative_lobby, acted_as_teller, title, date, division_number, number_in_favour, number_against))
            db.commit()

cursor.close()
db.close()
