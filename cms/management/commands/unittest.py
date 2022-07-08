import pytest
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Run unit tests'

    def add_arguments(self, parser):
        parser.add_argument('-k', '--filter', type=str, required=False),
        parser.add_argument(
            '-V',
            '--verbose',
            action="store_true",
            required=False,
        ),

    def handle(self, *args, **options):
        filter = options['filter']
        verbose = options['verbose']
        k = ['-k', filter] if filter else []
        v = "-vv" if verbose else ""
        result = pytest.main(k + ["--failed-first", v, "."])
        if result != pytest.ExitCode.OK:
            raise CommandError(result)
