import yaml
from glob import glob
from os.path import basename, dirname
from pySMART import Device
from twilio.rest import Client

with open('/etc/diskmon/config.yaml', 'r', encoding='utf8') as f:
  config = yaml.safe_load(f)

twilio_account_sid = config['twilio']['account_sid']
twilio_auth_token = config['twilio']['auth_token']
from_number = config['twilio']['from_number']
to_number = config['twilio']['to_number']

sms_body = ""

def send_sms(message):
  client = Client(twilio_account_sid, twilio_auth_token)
  message = client.messages \
                  .create(
                    body=message,
                    from_=from_number,
                    to=to_number
                  )

  print(message.sid)

def physical_drives():
  drive_glob = '/sys/block/*/device'
  return [basename(dirname(d)) for d in glob(drive_glob)]

for disk in physical_drives():
  if disk not in config['disks']:
    print(disk + ' found on system. Consider adding it to config.yaml to monitor it')

for disk in config['disks']:
  smart_status = Device('/dev/' + disk)
  print(smart_status.assessment)
  if smart_status.assessment is not None:
    if smart_status.assessment not in 'PASS':
      print('Disk ' + disk + ' failed smart test')
      sms_body = sms_body + 'Disk ' + disk + ' failed smart test'
  else:
    print('Disk ' + disk + " doesn't exist")
    sms_body = sms_body + 'Disk ' + disk + ' not found on system. Could indicate broken disk\n'

if sms_body and config['debug']['enabled'] is not True:
  send_sms(sms_body)
