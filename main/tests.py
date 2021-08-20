from datetime import datetime

from django.test import TestCase

from main.models import Logger, UserDemo


class BasicTest(TestCase):

    def test_logger_fields(self):
        l1 = Logger(email='Nir@gmail.com', threshold=0.8, command='1=1 or true', type_attack='SQL', if_warn=True,
                    date=datetime.now())
        l1.save()
        record = Logger.objects.get(pk=1)
        self.assertEqual(record, l1)

    def test_userdemo_fields(self):

        u1 = UserDemo(username='Nir@gmail.com', password='123')
        u1.save()

        record = UserDemo.objects.get(pk=1)
        self.assertEqual(record, u1)
