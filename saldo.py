from tu import Tupy
from consultants import Consultants
from pprint import pprint
import mail
from datetime import datetime
import sys

tupy = Tupy()
consultants = Consultants()

now = datetime.now()
year = now.year
week = now.isocalendar()[1] - 1

year_input = input('Hvilke aar skal generes? [{}] '.format(year))
week_input = input('Hvilke uke skal generes? [{}] '.format(week))

if not year_input:
    year_input = year

if not week_input:
    week_input = week

print('Folgende teamledere vil faa rapport:')
for teamleader in consultants.teamleaders:
    print(teamleader.number, teamleader.email)
    #print(teamleader.number, teamleader.first_name, teamleader.last_name)

print('Hvis dette ikke ser korrekt ut, kjor pgm 1-6-5 og 1-6-6')
teamleader_input = input('Ser dette korrekt ut? [ja/nei] ')

if teamleader_input != 'ja':
    sys.exit(1)

files = tupy.generate_saldo_lists(year, week, consultants.teams)

mailtext = '''Hei

Her har du ukens saldoliste:)

Dette er en automatisk generert mail som det er mulig og svare på om avsender er lager@klatrerosen.no!

Ha en god dag videre.

mvh
Tupperware lageret\n\n\n
'''

for team, path in files.items():
    print('Sending mail to {}'.format(team))
    mail.send_mail(
        [consultants.get_teamleader_for_team(team).email],
        #['kradalby@klatrerosen.no'],
        'Saldoliste for uke {}'.format(week),
        mailtext,
        files=[path]
    )


input()
