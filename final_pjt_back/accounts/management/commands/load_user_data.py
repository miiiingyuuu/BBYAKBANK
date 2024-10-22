import json
from django.core.management.base import BaseCommand
from accounts.models import User
from finance.models import DepositProduct

class Command(BaseCommand):
    help = 'Load user data from JSON file into the database'

    def handle(self, *args, **kwargs):
        json_file_path = 'accounts/fixtures/accounts/user_data.json'

        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for entry in data:
            user, created = User.objects.get_or_create(
                username=entry['fields']['username'],
                defaults={
                    'age': entry['fields']['age'],
                    'gender': entry['fields']['gender'],
                    'salary': entry['fields']['salary'],
                    'wealth': entry['fields']['wealth'],
                    'tendency': entry['fields']['tendency'] if 'tendency' in entry['fields'] else 1,
                }
            )

            if not created:
                user.age = entry['fields']['age']
                user.gender = entry['fields']['gender']
                user.salary = entry['fields']['salary']
                user.wealth = entry['fields']['wealth']
                user.tendency = entry['fields']['tendency'] if 'tendency' in entry['fields'] else 1
                user.save()

            financial_product_ids = entry['fields']['financial_products'].split(',')
            deposit_products = DepositProduct.objects.filter(deposit_code__in=financial_product_ids)
            user.deposit.set(deposit_products)
            user.save()

        self.stdout.write(self.style.SUCCESS('Successfully loaded user data'))
