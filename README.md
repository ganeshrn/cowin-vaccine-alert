# cowin-vaccine-alert

Required python>=3.6

Steps:

1) Step virtualenv

2) Install required libraries

$ pip install -r requirements.txt

3) Setup twilio account phone number

https://www.twilio.com/docs/sms/quickstart/python

4) Setup twilio account whatsapp account

https://www.twilio.com/docs/whatsapp/quickstart/python

5) Update below variables in ``cowin.py`` script
    -> ``TWILIO_SID`` 
    -> ``TWILIO_TOKEN``
    -> ``from_ph`` (Twilio number used to send SMS to regisetered phones numbers)
    -> ``whatsapp_from_ph`` (Twilio number used to send whatsapp to regisetered phones numbers)
    -> ``to_phs`` (registered phone numbers to receive message and calls )

6) Run script

$ git clone https://github.com/ganeshrn/cowin-vaccine-alert
$ cat cowin-vaccine-alert
$ python cowin.py 



