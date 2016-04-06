'''
Created on Mar 23, 2016

@author: mfeng
'''

from django.core.management.base import BaseCommand, CommandError
from www.config import SITE_URL

class Command(BaseCommand):
    help='collect config for www'
    
    def add_arguments(self, parser):
        parser.add_argument('--config',
                            action='store_true',
                            dest='config',
                            default=False,
                            help='collect all base config')
        parser.add_argument('--qrcode',
                            action='store_true',
                            dest='qrcode',
                            default=False,
                            help='create qrcode for web site')
    def handle(self, *args, **options):
        if options['config']:
            print 'will colloct config from file'
        if options['qrcode']:
            print 'will create qrcode'
            import qrcode
            img = qrcode.make('http://'+SITE_URL)
            with open('www/static/www/qrcode.png', 'wb') as f:
                img.save(f)