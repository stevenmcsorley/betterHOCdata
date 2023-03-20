import requests
import json
import pymysql.cursors
import os

API_URL = "https://members-api.parliament.uk/api/Members/Search"

def fetch_members_data(skip, take):
    params = {
        # IsCurrentMember=true
        #PartyId=4
        # "PartyId": 4,
        "IsCurrentMember": "true",
        "skip": skip,
        "take": take
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    return None

def save_data_to_json(members, file_name):
    with open(file_name, 'w') as json_file:
        json.dump(members, json_file, indent=2)

def load_data_from_json(file_name):
    with open(file_name, 'r') as json_file:
        return json.load(json_file)

def scrape_members_data():
    members = []
    total_members = 1
    page_size = 20
    current_page = 0

    while len(members) < total_members:
        data = fetch_members_data(current_page * page_size, page_size)
        if data:
            members.extend(data["items"])
            total_members = data["totalResults"]
            current_page += 1
        else:
            break

    json_file_name = 'members_data.json'

    # Save the data to a JSON file
    save_data_to_json(members, json_file_name)

    # Load the data from the JSON file
    members = load_data_from_json(json_file_name)

    # Process the data as needed and store it in MySQL
    conn = pymysql.connect(
        host='db',
        port=3306,
        user='root',
        password='password',
        database='members_data',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with conn.cursor() as cursor:
            for member in members:
                membership_status = member['value']['latestHouseMembership']['membershipStatus']
                member_data = {
                    'member_id': member['value']['id'],
                    'nameListAs': member['value']['nameListAs'],
                    'nameDisplayAs': member['value']['nameDisplayAs'],
                    'nameFullTitle': member['value']['nameFullTitle'],
                    'nameAddressAs': member['value']['nameAddressAs'],
                    'latestPartyId': member['value']['latestParty']['id'],
                    'latestPartyName': member['value']['latestParty']['name'],
                    'latestPartyAbbreviation': member['value']['latestParty']['abbreviation'],
                    'latestPartyBackgroundColour': member['value']['latestParty']['backgroundColour'],
                    'latestPartyForegroundColour': member['value']['latestParty']['foregroundColour'],
                    'latestPartyIsLordsMainParty': member['value']['latestParty']['isLordsMainParty'],
                    'latestPartyIsLordsSpiritualParty': member['value']['latestParty']['isLordsSpiritualParty'],
                    'latestPartyGovernmentType': member['value']['latestParty']['governmentType'],
                    'latestPartyIsIndependentParty': member['value']['latestParty']['isIndependentParty'],
                    'gender': member['value']['gender'],
                    'membershipFrom': member['value']['latestHouseMembership']['membershipFrom'],
                    'membershipFromId': member['value']['latestHouseMembership']['membershipFromId'],
                    'house': member['value']['latestHouseMembership']['house'],
                    'membershipStartDate': member['value']['latestHouseMembership']['membershipStartDate'],
                    'membershipEndDate': member['value']['latestHouseMembership']['membershipEndDate'],
                    'membershipEndReason': member['value']['latestHouseMembership']['membershipEndReason'],
                    'membershipEndReasonNotes': member['value']['latestHouseMembership']['membershipEndReasonNotes'],
                    'membershipEndReasonId': member['value']['latestHouseMembership']['membershipEndReasonId'],
                    'membershipStatusIsActive': membership_status['statusIsActive'],
                    'membershipStatusDescription': membership_status['statusDescription'],
                    'membershipStatusNotes': membership_status['statusNotes'],
                    'membershipStatusId': membership_status['statusId'],
                    'membershipStatus': membership_status['status'],
                    'membershipStatusStartDate': membership_status['statusStartDate'],
                    'thumbnailUrl': member['value']['thumbnailUrl']
                }
                columns = ', '.join(member_data.keys())
                placeholders = ', '.join(['%s'] * len(member_data))
                sql = f"INSERT INTO members ({columns}) VALUES ({placeholders}) ON DUPLICATE KEY UPDATE "
                updates = ', '.join([f"{column} = VALUES({column})" for column in member_data.keys()])
                sql += updates
                cursor.execute(sql, list(member_data.values()))
        conn.commit()

    finally:
        conn.close()

    # Remove the JSON file after importing data to MySQL
    os.remove(json_file_name)

if __name__ == '__main__':
    scrape_members_data()

