import json
import re
import time
from datetime import datetime

from urllib.parse import urlparse, parse_qs, unquote

import webbrowser

from loaders import NoDriver


class DoctolibNotifier:
    def __init__(self):
        self.driver = NoDriver()
        self.tld = ""

    def parse_initial_url(self, url):
        """Parse the initial URL to extract necessary query parameters and the practice name."""
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)#
        practice_name = unquote(parsed_url.path.split('/')[3])
        self.tld = parsed_url.netloc.split('.')[-1]
        practice_id = query_params.get('placeId', [""])[0].split("-")[1]
        motive_ids = query_params.get('motiveIds[]', [])
        practitioner_id = query_params.get('practitionerId', [])
        practitioner_id = [p_id for p_id in practitioner_id if p_id != 'NO_PREFERENCE']

        return practice_name, practice_id, motive_ids, practitioner_id

    def fetch_practice_data(self, practice_name):
        url = f"https://www.doctolib.{self.tld}/online_booking/api/slot_selection_funnel/v1/info.json?profile_slug={practice_name}"
        response_json = self.query_doctolib_to_json(url)
        return response_json

    def extract_agenda_ids(self, data, motive_ids, practitioner_id):
        """Extract agenda IDs from practice data that match the specified motive IDs."""
        agenda_ids = []
        if 'data' in data and 'agendas' in data.get('data'):
            for agenda in data['data']['agendas']:
                # Check if 'visit_motive_ids' exists and has any matching motive_id
                if 'visit_motive_ids' in agenda:
                    if any(int(motive_id) in agenda.get('visit_motive_ids') for motive_id in motive_ids):
                        if not practitioner_id or str(agenda.get('practitioner_id')) in practitioner_id:
                            agenda_id = agenda.get('id')
                            if agenda_id is not None:
                                agenda_ids.append(str(agenda_id))
        return agenda_ids

    def construct_final_url(
        self, motive_ids, agenda_ids, practice_id, insurance_sector, telehealth, start_date, limit
    ):
        """Construct the final URL to fetch availabilities."""
        motive_ids = ','.join(motive_ids)
        agenda_ids = '-'.join(agenda_ids)
        url = (
            f"https://www.doctolib.{self.tld}/availabilities.json?visit_motive_ids={motive_ids}&agenda_ids={agenda_ids}"
            f"&practice_ids={practice_id}&insurance_sector={insurance_sector}&telehealth={telehealth}"
            f"&start_date={start_date}&limit={limit}"
        )
        return url

    def query_doctolib_to_json(self, url):
        response = self.driver.get_response(url)

        match = re.search(r'<pre>(.*?)</pre>', response, re.DOTALL)

        json_string = match.group(1)
        response_json = json.loads(json_string)
        return response_json

    def search_loop(self, final_url, initial_url):
        while True:
            available_dates = []
            response_json = self.query_doctolib_to_json(final_url)
            for availability in response_json['availabilities']:
                if availability.get("slots"):
                    available_dates.append(availability["date"])

            if available_dates:
                webbrowser.open(initial_url)
                print(f"The following dates are available: {available_dates}")
                break

            next_slot = response_json.get('next_slot')
            if next_slot:
                print(f"The next slot later than 15 days is: {next_slot}")

            print("Sleeping for 60s...")
            time.sleep(61)

    def main(self, initial_url):
        # Construct final query url
        practice_name, practice_id, motive_ids, practitioner_id = self.parse_initial_url(initial_url)
        practice_data = self.fetch_practice_data(practice_name)
        raw_agenda_ids = self.extract_agenda_ids(practice_data, motive_ids, practitioner_id)
        final_url = self.construct_final_url(
            motive_ids, raw_agenda_ids, practice_id, 'public', 'false', datetime.today().strftime('%Y-%m-%d'), '15'
        )

        print(f"The final query url is {final_url}")
        self.search_loop(final_url, initial_url)


if __name__ == "__main__":
    url = input("Please paste in the URL of the practice:\n")
    DoctolibNotifier().main(url)
