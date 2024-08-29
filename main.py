import os
import json
import datetime
import boto3
import requests
from pytz import timezone

def main():

    data = load_data()

    TIMEZONE = os.environ.get('TIMEZONE', 'UTC')
    use_tz = timezone(TIMEZONE)
    now = datetime.datetime.now(use_tz)
    now_datetime_text = now.strftime('%Y-%m-%d %H:%M:%S')

    print(f"Check IP address at {now_datetime_text} ({TIMEZONE}). Previous check datetime is {data['check_datetime']}.")

    if data['check_datetime']:
        check_datetime = datetime.datetime.strptime(data['check_datetime'], '%Y-%m-%d %H:%M:%S')
        check_datetime = use_tz.localize(check_datetime)
        diff_seconds = (now - check_datetime).total_seconds()
        diff_seconds = int(diff_seconds)
        MIN_INTERVAL_SECCONDS = int(os.environ.get('MIN_INTERVAL_SECCONDS', 50))
        if diff_seconds < MIN_INTERVAL_SECCONDS:
            print(f"Check interval is too short. ({diff_seconds} seconds. Min interval is {MIN_INTERVAL_SECCONDS} seconds.)")
            return

    data['check_datetime'] = now_datetime_text

    HOSTED_ZONE_ID = os.environ.get('HOSTED_ZONE_ID')
    RECORD_NAME = os.environ.get('RECORD_NAME')
    TTL = int(os.environ.get('TTL', 300))

    ip_address = requests.get('http://checkip.amazonaws.com/').text.strip()

    if data['recorded_ip_address'] == ip_address:
        print(f"IP address was not changed. No update was performed. ({ip_address})")
        save_data(data)
        return

    client = boto3.client('route53')
    response = client.change_resource_record_sets(
        HostedZoneId=HOSTED_ZONE_ID,
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': RECORD_NAME,
                        'Type': 'A',
                        'TTL': TTL,
                        'ResourceRecords': [{'Value': ip_address}],
                    }
                }
            ]
        }
    )

    print(f"Updated {RECORD_NAME} to {ip_address}")

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("Update success.")

        data['recorded_ip_address'] = ip_address
        data['recorded_datetime'] = now_datetime_text

        msg = f"Updated the IP address for Route53. [{RECORD_NAME}][{ip_address}]"
        send_discord_message(msg)

    save_data(data)

def load_data():
    file_path = 'tmp/data.json'
    if os.path.exists(file_path):
        with open(file_path) as f:
            data = json.load(f)
            return data
    else:
        return {
            'check_datetime': '',
            'recorded_datetime': '',
            'recorded_ip_address': ''
        }

def save_data(data):
    file_path = 'tmp/data.json'
    with open(file_path, 'w') as f:
        json.dump(data, f)

def send_discord_message(message):
    WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')
    if WEBHOOK_URL:
        requests.post(WEBHOOK_URL, json={'content': message})
        print(f"Sent message to Discord. ({message})")

if __name__ == "__main__":
    main()
