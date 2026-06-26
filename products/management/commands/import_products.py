import csv
import json
from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Import products from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        
        self.stdout.write(self.style.NOTICE(f'Reading from {csv_file}...'))
        
        imported = 0
        skipped = 0
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # id,product_name,product_description,category,tags
                    product_id = row.get('id')
                    name = row.get('product_name')
                    desc = row.get('product_description')
                    category = row.get('category')
                    tags_str = row.get('tags', '')
                    
                    # Split tags by comma
                    tags_list = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
                    
                    # Check for duplicates by name or id
                    # If duplicate, we can either skip or update. Let's update or skip.
                    if Product.objects.filter(product_name=name).exists():
                        skipped += 1
                        continue
                        
                    Product.objects.create(
                        product_name=name,
                        product_description=desc,
                        category=category,
                        tags=tags_list
                    )
                    imported += 1
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing data: {e}'))
            return
            
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {imported} products. Skipped {skipped} duplicates.'))
