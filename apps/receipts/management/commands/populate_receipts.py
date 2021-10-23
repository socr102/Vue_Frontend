from django.core.management.base import BaseCommand, CommandError

from apps.receipts.utils.receipt_generator import ReceiptGenerator
from apps.receipts.models import Receipt
from apps.user_panel.models import CustomUser
from apps.members.models import Member
from backend.utils import positive_int

class Command(BaseCommand):
    help = 'Populate database with fake receipts data'

    def add_arguments(self, parser):
        parser.add_argument('--stores', type=positive_int, required=True, help='')
        parser.add_argument('--categories', type=positive_int, required=True, help='')
        parser.add_argument('--products', type=positive_int, required=True, help='')
        parser.add_argument('--articles', type=positive_int, required=True, help='')
        parser.add_argument('--receipts', type=positive_int, required=True, help='')
        parser.add_argument('--members', type=positive_int, nargs='+',
                            help='List of member ids for whome receipts will be generated')
        parser.add_argument('--merchantId', type=int, help='')

    def handle(self, *args, **options):
        members = self.get_members(options)
        generator = ReceiptGenerator(options['stores'],
                                     options['categories'],
                                     options['products'],
                                     options['articles'],
                                     members)

        merchant = self.get_merchant(options)

        page_size = options['receipts'] // 10
        for _ in range(10):
            data = [generator.getReceipt() for _ in range(page_size)]
            Receipt.bulk_import(data, merchant, members)

    def get_merchant(self, options):
        if options['merchantId'] is None:
            # get any merchant user from db
            merchant = CustomUser.objects.filter(is_active=True,
                                                is_superuser=False,
                                                is_staff=False).\
                                                first()
            if not merchant:
                raise CommandError("Please add at least 1 merchant to the Database")
        else:
            merchant = CustomUser.objects.filter(id=options['merchantId'],
                                                    is_active=True).first()

            if not merchant:
                raise CommandError("There no merchants in Database with provided id")

        return merchant

    def get_members(self, options):
        if options['members'] is None:
            return Member.objects.all()
        else:
            return Member.objects.filter(id__in=options['members'])
