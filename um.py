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

if year_input:
    year = year_input

if week_input:
    week = week_input

print('Folgende teamledere vil faa rapport:')
print('For uke {} i aar {}'.format(week, year))
for teamleader in consultants.teamleaders:
    print(teamleader.number)
    #print(teamleader.number, teamleader.first_name, teamleader.last_name)

print('Hvis dette ikke ser korrekt ut, kjor pgm 1-6-5 og 1-6-6')
teamleader_input = input('Ser dette korrekt ut? [ja/nei] ')

if teamleader_input != 'ja':
    sys.exit(1)

files = tupy.generate_um_analyses(year, week, consultants.teams)

mailtext = '''Hei

Her har du ukens Teamleder Analyse:)

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
        'Teamleder analyse for uke {}'.format(week),
        mailtext,
        files=[path]
    )

input()
