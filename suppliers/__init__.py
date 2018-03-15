from ccapi import CCAPI
from django.template import Template, Context
from django.template.engine import Engine
from django.conf import settings
import os
import webbrowser


settings.configure(DEBUG=False)

template_path = os.path.join(os.path.dirname(__file__), 'template.html')

with open(template_path, 'r') as f:
    template_string = f.read()

template = Template(template_string, engine=Engine())

options = CCAPI.get_product_options()
suppliers = [o for o in options if o.option_name == 'Supplier'][0].values
suppliers.sort(key=lambda x: x.value)

supplier_id = None

while supplier_id is None:
    print('Enter name of supplier or enter "list" or a list of suppliers.')
    supplier_name = input('Supplier Name: ').strip().lower()
    if supplier_name == 'list':
        print()
        for supplier in suppliers:
            print(supplier.value)
        print()
    else:
        try:
            supplier = [
                s for s in suppliers if s.value.lower() == supplier_name][0]
            supplier_id = supplier.id
            supplier_name = supplier.value
        except IndexError as e:
            print('Supplier not recognised.')

print('Loading Products...')

product_ranges = CCAPI.get_ranges(option_matches_id=supplier_id)
product_ranges.sort(key=lambda x: x.name)
context = Context(
    {'product_ranges': product_ranges, 'supplier': supplier_name})
html = template.render(context)

OUTPUT_PATH = os.path.join(os.getcwd(), 'HTML')

if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

OUTPUT_FILE = os.path.join(OUTPUT_PATH, '{}.html'.format(supplier_name))

with open(OUTPUT_FILE, 'w') as f:
    f.write(html)

webbrowser.open(OUTPUT_FILE)
