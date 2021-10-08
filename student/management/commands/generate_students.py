from django.core.management.base import BaseCommand
from student.models import Student


class Command(BaseCommand):
    help = 'Generates <count> students'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Count of students')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        Student.generate_instances(count)
