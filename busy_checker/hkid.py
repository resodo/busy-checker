import datetime

import requests

office_ids = [
    "RHK",
    "RKO",
    "RKT",
    "YLO",
    "TMO",
    "FTO",
]  # Add your office IDs here
days = 30 * 3


# Define a function to check for available slots
def check_availability():
    # Define your preferred date range and office IDs
    start_date = datetime.date.today()
    end_date = start_date + datetime.timedelta(days=days)

    url = (
        "https://eservices.es2.immd.gov.hk"
        + "/surgecontrolgate/ticket/getSituation"
    )
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "Connection": "keep-alive",
        "Referer": "https://eservices.es2.immd.gov.hk"
        + "/es/quota-enquiry-client/?l=zh-HK&appId=579",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
        + " AppleWebKit/537.36 (KHTML, like Gecko)"
        + " Chrome/114.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114",'
        + ' "Google Chrome";v="114"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
    }

    available_slots = []

    try:
        response = requests.get(url, headers=headers)
        # Raise an exception if the request was not successful
        response.raise_for_status()
        data = response.json()["data"]

        for slot in data:
            slot_date = datetime.datetime.strptime(
                slot["date"], "%m/%d/%Y"
            ).date()
            quota_r = slot["quotaR"]
            quota_k = slot["quotaK"]
            office_id = slot["officeId"]

            if (
                start_date <= slot_date <= end_date
                and (
                    quota_r != "quota-r"
                    or (quota_k != "quota-r" and quota_k != "quota-non")
                )
                and office_id in office_ids
            ):
                available_slots.append(slot)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the API request: {e}")

    return available_slots
