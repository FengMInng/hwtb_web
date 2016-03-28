'''
Created on Mar 23, 2016

@author: mfeng
'''

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help='collect config for www'
    
    def add_arguments(self, parser):
        parser.add_argument('--config',
                            action='store_true',
                            dest='config',
                            default=False,
                            help='collect all base config')
    
    def handle(self, *args, **options):
        if options['config']:
            print 'will colloct config from file'