import logging
from django.core.management.base import BaseCommand
from user.models import User


class Command(BaseCommand):

    @staticmethod
    def convert_matrix_to_dict(data):
        keys = data[0]
        response = []
        for row in data[1:]:
            row_dict = {}
            for key, value in zip(keys, row):
                row_dict[key] = value
            response.append(row_dict)
        return response

    @staticmethod
    def create_admin():
        email = 'admin@baboons.api'
        password = 'MrOeshBr8lhnsQbXhay3uw'
        admin = User.objects.filter(username=email, email=email).first()
        if admin:
            logging.warning('Admin already exists!')
            return

        admin = User(username=email, email=email, is_superuser=True, is_staff=True)
        admin.set_password(password)
        admin.save()
        logging.info('Admin created!')

    def add_arguments(self, parser):
        """
        :param parser:
        """
        parser.add_argument('command', type=str)

    def handle(self, *args, **options):
        """
        :param args: setup_backend
        :param options: create_admin, all
        """
        command = options['command']
        logging.info(f'Initiating the command {command}...')

        if command == 'create_admin':
            self.create_admin()
        elif command == 'all':
            self.create_admin()
        else:
            raise ValueError('Invalid command')
        logging.info('Command completed!')
