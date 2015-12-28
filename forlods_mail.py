import mail
from consultants import Consultants
import os

PATH = r'C:\Users\kradalby\Dropbox\Årsavsluttning\2015\faktura_forlods'

text_consultant = '''Hei

Vedlagt ligger faktura for forlods fra 2015.

--
Mvh
Kristoffer Dalby
Tupperware lageret'''

text_teamleader = '''Hei

Vedlagt ligger faktura for forlods fra 2015.

Legg merke til at fakturaen din er i minus og at du har {} kroner totalt til gode.

--
Mvh
Kristoffer Dalby
Tupperware lageret'''



def send_invoice(year, consultant_number):
    consultants = Consultants()

    mailtext = ''
    if str(consultant_number)[2:] == '01':
        money = input('Hvor mye til gode?: ')
        if money == 'no':
            mailtext = text_consultant
        else:
            mailtext = text_teamleader.format(money)
    else:
        mailtext = text_consultant
    print('Sending email for {} to {}'.format(
        consultant_number,
        consultants.get_email(consultant_number))
    )

    mail.send_mail(
        [consultants.get_email(consultant_number), 'kradalby@klatrerosen.no'],
        #['kradalby@klatrerosen.no'],
        'Forlods faktura for {}'.format(year),
        mailtext,
        files=[os.path.join(PATH, '{}{}'.format(consultant_number, '.pdf'))]
    )
