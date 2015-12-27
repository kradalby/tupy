from pywinauto import application
from pywinauto import timings
import pywinauto
import time
import configparser
import os

PATH = os.path.dirname(os.path.abspath(__file__))

class Tupy:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(PATH, 'config.ini'))
        self.base_path = config['path']['teamleder']
        self.app = None

    def start(self):
        if not self.app:
            self.app = application.Application()
            self.app.start(r'C:\acucorp\Acucbl720\AcuGT\bin\acuthin.exe 192.168.1.3:6525 tupo')
            return True
        else:
            return False

    def stop(self):
        if self.app:
            try:
                time.sleep(5)
                self.app.window_().TypeKeys('{ESC}')
                self.app['Warning']['&YesButton'].Click()
            except Exception as e:
                print(e)
                self.app.kill_()

            self.app = None
            return True
        else:
            return False

    def configure_printer(self, orientation):
        time.sleep(2)
        self.app['Tilpas Printer']['Setup...'].Click()
        self.app['Print Setup']['ComboBox'].Select('Microsoft Print to PDF')
        self.app['Print Setup'][orientation].Click()
        self.app['Print Setup']['OK'].Click()
        self.app['Tilpas Printer']['Ok'].Click()

    def save_pdf(self, path):
        time.sleep(3)
        self.app['Save Print Output As']['Edit'].SetText(path)
        self.app['Save Print Output As']['Save'].Click()


    def handle_lock(self):
        while self.app['T01liDialog']:
            print('handling')
            try:
                self.app['T01liDialog']['OK'].Click()
                time.sleep(5)
            except:
                return

    def go_to_program(self, sequence):
        for program in sequence:
            self.app['T01li']['Edit'].SetText('{},0'.format(program))
            self.app['T01li'].TypeKeys('{ENTER}')


    def create_path(self, list_type, year, week, team):
        path = r'{}\{}\{}\{}\uke{}'.format(
            self.base_path,
            team,
            year,
            list_type,
            week
        )
        return path

    def delete_file_if_exists(self, file):
        if os.path.isfile(file):
            os.remove(file)

    def generate_um_analyses_for_team(self, year, week, team):
        if not self.start():
            self.stop()
            self.start()
        self.go_to_program([10, 7])
        self.app['UM-analyse']['Uge:           Edit'].SetText(str(year) + str(week))
        self.app['UM-analyse']['Gruppe:        Edit'].SetText(team)
        self.app['UM-analyse']['Printer'].Click()
        self.configure_printer('Landscape')
        self.app['UM-analyse']['OK'].Click()
        path = self.create_path('weekly', year, week, team)
        self.handle_lock()
        self.save_pdf(path)
        self.stop()
        return path + '.pdf'

    def generate_um_analyses(self, year, week, teams):
        files = {}

        for team in teams:
            path = self.create_path('weekly', year, week, team) + '.pdf'
            self.delete_file_if_exists(path)

        for team in teams:
            files[team] = self.generate_um_analyses_for_team(year, week, team)
        return files

    def generate_saldo_list_for_team(self, year, week, team):
        if not self.start():
            self.stop()
            self.start()
        self.go_to_program([3, 5])
        self.configure_printer('Landscape')
        time.sleep(3)
        windows = self.app.windows_()
        if windows[0].Class() == 'AcucobolWClass':
            print(windows[0].Texts())
            windows[0].TypeKeys('{ENTER}')

        path = self.create_path('saldoliste', year, week, team)
        self.save_pdf(path)
        time.sleep(9)

        windows = self.app.windows_()
        if windows[0].Class() == 'AcucobolWClass':
            windows[0].TypeKeys('{}00'.format(team))
            windows[0].TypeKeys('{ENTER}')
            windows[0].TypeKeys('{}99'.format(team))
            windows[0].TypeKeys('{ENTER}')

        self.stop()

        print('Genererer liste for {}'.format(team))
        return path + '.pdf'

    def generate_saldo_lists(self, year, week, teams):
        files = {}

        for team in teams:
            path = self.create_path('saldoliste', year, week, team) + '.pdf'
            self.delete_file_if_exists(path)

        for team in teams:
            files[team] = self.generate_saldo_list_for_team(year, week, team)
        return files
