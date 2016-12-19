import uuid
from datetime import datetime
from consultants import Consultants

consultants = Consultants()

vcf = ''

for c in consultants.all:
    uid = uuid.uuid5(uuid.NAMESPACE_DNS, c.number).__str__().upper()
    rev = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    vcf += '''BEGIN:VCARD
VERSION:3.0
N:{};{}
FN:{} {}
ORG:{}
TITLE:{}
TEL;type=HOME;type=VOICE:{}
TEL;type=CELL;type=VOICE:{}
item1.ADR;type=HOME;type=pref:;;{};{};;{};{}
EMAIL;TYPE=PREF,INTERNET:{}
REV:{}
UID:{}
END:VCARD
'''.format(c.last_name, c.first_name, c.first_name, c.last_name, 'Klatrerosen', 'TW Konsulent ' + c.number, c.phone1, c.phone2, c.address, c.town, c.zip_code, c.country, c.email, rev, uid,)

print(vcf)
