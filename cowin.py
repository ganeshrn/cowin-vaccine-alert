import requests
import json
import time
import datetime

from twilio.rest import Client

from typing import List
from typing import Optional
from typing import Tuple
from typing import Dict

MSG = "Covid vaccine slot available, check https://www.cowin.gov.in/home"
TWILIO_SID = "change-me"
TWILIO_TOKEN = "change-me"


def get_slot_available_by_pin(pincodes: List, on_dates: List) -> Tuple[Dict, bool, str, str]:
    slot_available = False
    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={0}&date={1}"

    on_date = []
    pincode = []
    for on_date in on_dates:
        for pincode in pincodes:
            get_url = URL.format(pincode, on_date)
            response = requests.get(get_url)
            try:
                obj = json.loads(response.text)
                if obj.get('sessions'):
                    for session in obj['sessions']:
                        if int(session['min_age_limit']) < 45:
                            slot_available = True
                            print(f"Available session details: \n{obj}")
                            break
            except Exception:
                pass
            time.sleep(2)
        if slot_available:
            break
    
    return slot_available, on_date, pincode


def notify_on_phone(from_ph: str, to_ph: List, msg: str) -> None:


    client = Client(TWILIO_SID, TWILIO_TOKEN)

    for num in to_ph:
        client.messages.create(from_=from_ph,
                            to=num,
                            body=msg)


def notify_on_whatsapp(from_ph: str, to_ph: List, msg: str) -> None:
    client = Client(TWILIO_SID, TWILIO_TOKEN)

    for num in to_ph:
        client.messages.create(from_="whatsapp:" + from_ph,
                            to="whatsapp:" + num,
                            body=msg)


def notify_on_call(from_ph: str, to_ph: List, msg: str) -> None:
    client = Client(TWILIO_SID, TWILIO_TOKEN)

    for num in to_ph:
        client.calls.create(from_=from_ph,
                            to=num,
                            url="https://handler.twilio.com/twiml/EHc4fb4b061d9df20da476d1344b765c7c")


def generate_next_n_dates(num=7) -> List:
    day_1 = datetime.date.today()
    on_dates = [day_1.strftime("%d-%m-%Y")]
    # dd-mm-YY
    for index in range(1, num):
        day = day_1 + datetime.timedelta(index)
        on_dates.append(day.strftime("%d-%m-%Y"))
    
    return on_dates

if __name__ == "__main__":
    notified = []
    pincodes = ["411027", "411001", "411028", "411011", "411006", "411017", "411033"]
    from_ph = "+<twilio account whatsapp number>"
    whatsapp_from_ph = "<twilio account whatsapp number>"
    to_phs = ["<notif-ph-1>", "<notif-ph-1>"]

    on_dates = generate_next_n_dates(num=2)
    print(on_dates)
    print(pincodes)
    try:
        star_msg = f"Vaccine slot script running for dates {on_dates} with pincodes {pincodes}"
        print(star_msg)
        notify_on_phone(from_ph, to_phs, star_msg)
        notify_on_whatsapp(whatsapp_from_ph, to_phs, star_msg)
        while True:
            today = datetime.date.today().strftime("%d-%m-%Y")
            # increment date
            if today != on_dates[0]:
                notified = []
                on_dates = generate_next_n_dates()
                update_dates_msg = f"vaccine slot script run updated for dates {on_dates}"
                print(update_dates_msg)
    
            is_slot_available, date, pincode = get_slot_available_by_pin(pincodes, on_dates)
            if is_slot_available:
                msg = MSG + f" at pincode {pincode} on date {date}"
                print(msg)
                notify_on_phone(from_ph, to_phs, msg)
                notify_on_whatsapp(whatsapp_from_ph, to_phs, msg)
                notify_on_call(from_ph, to_phs, msg)
                notified.append(pincode)
            time.sleep(30)
    finally:
        end_msg = f"Vaccine slot script stopped running for dates {on_dates} with pincodes {pincodes}"
        print(end_msg)
        #notify_on_phone(from_ph, to_phs, end_msg)
        notify_on_whatsapp(whatsapp_from_ph, to_phs, end_msg)

