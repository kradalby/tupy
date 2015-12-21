import configparser
import os

PATH = os.path.dirname(os.path.abspath(__file__))

class Consultants:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(PATH, 'config.ini'))
        self.all = self.parse_consultant_file(config['path']['consultants'])

    def parse_consultant_file(self, path):
        with open(path) as f:
            f = f.read()
            consultants = [x.split(',') for x in f.split('\n')]
            consultants.pop(-1)

            consultant_objects = []

            for c in consultants:
                c = [x.strip('"') for x in c]
                consultant = Consultant(
                    long_unique_TW_number=c[0],
                    ship=c[1],
                    team=c[2],
                    number=c[3],
                    position=c[4],
                    y=c[5],
                    #first_name=bytes(c[6], 'ibm775').decode('utf-8'),
                    #last_name=bytes(c[7], 'ibm775').decode('utf-8'),
                    first_name=c[6],
                    last_name=c[7],
                    address=c[8],
                    zip_code=c[9],
                    town=c[10],
                    country=c[11],
                    phone1=c[12],
                    phone2=c[13],
                    email=c[14],
                    password=c[15],
                    y2=c[16],
                )
                consultant_objects.append(consultant)
            return consultant_objects
    @property
    def teamleaders(self):
        return [c for c in self.all if c.number[2:] == '01']

    @property
    def teams(self):
        return set([t.team for t in self.teamleaders])

    def get_teamleader_for_team(self, team_number):
        for teamleader in self.teamleaders:
            if teamleader.team == str(team_number):
                return teamleader

class Consultant:
    def __init__(self,
        long_unique_TW_number=None,
        ship=None,
        team=None,
        number=None,
        position=None,
        y=None,
        first_name=None,
        last_name=None,
        address=None,
        zip_code=None,
        town=None,
        country=None,
        phone1=None,
        phone2=None,
        email=None,
        password=None,
        y2=None,
    ):
        self.long_unique_TW_number = long_unique_TW_number
        self.ship = ship
        self.team = team
        self.number = number
        self.position = position
        self.y = y
        self.y2 = y2
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.zip_code = zip_code
        self.town = town
        self.country = country
        self.phone1 = phone1
        self.phone2 = phone2
        self.email = email
        self.password = password

    def __str__(self):
        return '{} - {} {}'.format(
            self.number,
            self.first_name,
            self.last_name
        )

    def __repr__(self):
        return self.__str__()
