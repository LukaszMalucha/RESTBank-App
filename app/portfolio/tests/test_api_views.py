from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from portfolio import serializers
from core import models

INSTRUMENTS_URL = reverse("portfolio:instruments-list")
CASH_BALANCE_URL = reverse("portfolio:cash-balance-list")
ASSET_MANAGER_URL = reverse("portfolio:asset-manager-list")
BUY_URL = reverse("portfolio:buy-list")
SELL_URL = reverse("portfolio:sell-list")


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
    instrument = models.Instrument.objects.create(**payload)
    return instrument


def sample_cash():
    payload = {"name": "USD",
               "symbol": "USD",
               "category": "cash",
               "price": 1.00
               }
    instrument = models.Instrument.objects.create(**payload)
    return instrument


def sample_cash_asset(owner, cash):
    payload = {"instrument": cash,
               "quantity": 1000.00,
               "owner": owner,
               }
    asset = models.Asset.objects.create(**payload)
    return asset


def sample_asset(owner, instrument):
    payload = {"instrument": instrument,
               "quantity": 1.00,
               "owner": owner,
               }
    asset = models.Asset.objects.create(**payload)
    return asset


class InstrumentApiTests(TestCase):
    """Test instruments view"""

    def setUp(self):
        self.client = APIClient()

        self.superuser = get_user_model().objects.create_superuser(
            'test@gmail.com',
            'testpass'
        )
        self.client.force_authenticate(self.superuser)
        models.Instrument.objects.create(
            name="Test",
            symbol="TST",
            category="test",
            price=1.00
        )
        models.Instrument.objects.create(
            name="Test1",
            symbol="TST1",
            category="test1",
            price=1.00
        )

    def test_retrieve_instruments_list(self):
        """Test retrieving instruments list"""

        instruments = models.Instrument.objects.all()
        serializer = serializers.InstrumentSerializer(instruments, many=True)
        response = self.client.get(INSTRUMENTS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_create_instrument_successful(self):
        """Test create new company by admin user"""
        self.client.force_authenticate(self.superuser)
        payload = {"name": "Test",
                   "symbol": "TST",
                   "category": "test",
                   "price": 1.00
                   }
        self.client.post(INSTRUMENTS_URL, payload)

        exist = models.Instrument.objects.filter(
            name=payload['name'],
        ).exists()
        self.assertTrue(exist)


class CashBalanceViewTests(TestCase):
    """Test cash balance view view"""

    def setUp(self):
        self.client = APIClient()

        self.user = sample_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_cash_balance(self):
        """Test accessing cash balance"""
        response = self.client.get(CASH_BALANCE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_top_up_cash_balance(self):
        """Test topping up cash balance"""
        cash = models.Instrument.objects.filter(name="USD")
        payload = {"instrument": cash,
                   "quantity": 1000,
                   "owner": self.user,
                   }

        response = self.client.post(CASH_BALANCE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
                         "You've successfully transferred 1000 $ to your Account. Your current cash balance is 1000.00$.")

    def test_top_up_above_maximum_amount(self):
        """Testing top up above maximum amount"""
        cash = models.Instrument.objects.filter(name="USD")
        payload = {"instrument": cash,
                   "quantity": 1000000,
                   "owner": self.user,
                   }
        response = self.client.post(CASH_BALANCE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_top_up_invalid_amount(self):
        """Testing top up above maximum amount"""
        cash = models.Instrument.objects.filter(name="USD")
        payload = {"instrument": cash,
                   "quantity": 0,
                   "owner": self.user,
                   }
        response = self.client.post(CASH_BALANCE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AssetManagerViewSetTests(TestCase):
    """Test asset manager view"""

    def setUp(self):
        self.client = APIClient()

        self.user = sample_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_user_assets(self):
        """Test accessing user assets"""
        response = self.client.get(ASSET_MANAGER_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BuyAssetViewSetTests(TestCase):
    """Test buy asset view"""

    def setUp(self):
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_buy_transactions(self):
        """Test accessing buy transactions"""
        response = self.client.get(BUY_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_buying_asset(self):
        """Test buying asset"""
        cash_balance = models.Asset.objects.get(instrument__name="USD", owner=self.user)
        cash_balance.quantity = 1000
        cash_balance.save()
        instrument = sample_instrument()
        buy_transaction = {"instrument": instrument.id,
                           "quantity": 1,
                           "owner": self.user,
                           }
        response = self.client.post(BUY_URL, buy_transaction)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_buying_insufficient_cash(self):
        """Test buying asset"""
        instrument = sample_instrument()
        buy_transaction = {"instrument": instrument.id,
                           "quantity": 1,
                           "owner": self.user,
                           }
        response = self.client.post(BUY_URL, buy_transaction)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0],
                         "You have insufficient funds to proceed with transaction.")

    def test_invalid_usd_to_usd_transaction(self):
        """Test error occurs when usd to usd transaction"""
        instrument = models.Instrument.objects.get(name="USD")
        buy_transaction = {"instrument": instrument.id,
                           "quantity": 1,
                           "owner": self.user,
                           }
        response = self.client.post(BUY_URL, buy_transaction)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], "USD to USD - invalid transaction")

class SellAssetViewSetTests(TestCase):
    """Test sell asset view"""

    def setUp(self):
        self.client = APIClient()

        self.user = sample_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_sell_transactions(self):
        """Test accessing sell transactions"""
        response = self.client.get(SELL_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_selling_asset(self):
        """Test selling asset"""
        instrument = sample_instrument()
        asset = sample_asset(self.user, instrument)
        sell_transaction = {"instrument": instrument.id,
                            "quantity": 1,
                            "owner": self.user,
                            }
        response = self.client.post(SELL_URL, sell_transaction)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_selling_asset_not_owned(self):
        """Test selling asset not owned by user"""
        instrument = sample_instrument()
        sell_transaction = {"instrument": instrument.id,
                            "quantity": 1,
                            "owner": self.user,
                            }
        response = self.client.post(SELL_URL, sell_transaction)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], "You don't own this asset.")

    def test_selling_insufficient_cash(self):
        """Test selling asset"""
        instrument = sample_instrument()
        sell_transaction = {"instrument": instrument.id,
                           "quantity": 5,
                           "owner": self.user,
                           }
        asset = sample_asset(self.user, instrument)
        response = self.client.post(SELL_URL, sell_transaction)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0],
                         "You have insufficient asset quantity to proceed with transaction.")

    def test_invalid_usd_to_usd_transaction(self):
        """Test error occurs when usd to usd transaction"""
        instrument = models.Instrument.objects.get(name="USD")
        sell_transaction = {"instrument": instrument.id,
                           "quantity": 1,
                           "owner": self.user,
                           }
        response = self.client.post(SELL_URL, sell_transaction)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], "USD to USD - invalid transaction")