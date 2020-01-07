from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from datetime import datetime

from core.models import Instrument, Asset, BuyTransaction, SellTransaction


def sample_user():
    user = get_user_model().objects.create_superuser(
        email="superuser@gmail.com",
        password="test1234",
    )
    return user


def sample_instrument():
    payload = {"name": "Test",
               "symbol": "TST",
               "category": "test",
               "price": 1.00
               }
    instrument = Instrument.objects.create(**payload)
    return instrument


def sample_cash():
    payload = {"name": "USD",
               "symbol": "USD",
               "category": "cash",
               "price": 1.00
               }
    instrument = Instrument.objects.create(**payload)
    return instrument


def sample_cash_asset(owner, cash):
    payload = {"instrument": cash,
               "quantity": 1000.00,
               "owner": owner,
               }
    asset = Asset.objects.create(**payload)
    return asset


def sample_asset(owner, instrument):
    payload = {"instrument": instrument,
               "quantity": 1.00,
               "owner": owner,
               }
    asset = Asset.objects.create(**payload)
    return asset


class SignalTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_add_slug_to_instrument(self):
        instrument = sample_instrument()
        self.assertTrue(len(instrument.slug) > 1)

    def test_add_slug_to_asset(self):
        owner = sample_user()
        instrument = sample_instrument()
        asset = sample_asset(owner, instrument)
        self.assertTrue(len(asset.slug) > 1)

    def test_add_slug_to_buy_transaction(self):
        owner = sample_user()
        cash_balance = Asset.objects.get(instrument__name="USD", owner=owner)
        cash_balance.quantity = 1000
        cash_balance.save()
        instrument = sample_instrument()

        payload = {"instrument": instrument,
                   "quantity": 1.00,
                   "owner": owner,
                   "created_at": datetime.now()
                   }
        transaction = BuyTransaction.objects.create(**payload)
        self.assertTrue(len(transaction.slug) > 1)

    def test_add_slug_to_sell_transaction(self):
        owner = sample_user()
        instrument = sample_instrument()
        cash_balance = Asset.objects.get(instrument__name="USD", owner=owner)
        cash_balance.quantity = 1000
        cash_balance.save()
        asset = sample_asset(owner, instrument)
        payload = {"instrument": instrument,
                   "quantity": 1.00,
                   "owner": owner,
                   "created_at": datetime.now()
                   }
        transaction = SellTransaction.objects.create(**payload)
        self.assertTrue(len(transaction.slug) > 1)