from django.test import TestCase

# Create your tests here.
from index.models import *

t = Product.objects.filter(id=1)