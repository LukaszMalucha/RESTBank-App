from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse  # generate urls for django admin page
from core.models import Instrument, Asset, BuyTransaction, SellTransaction
import datetime


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@gmail.com',
            password='test123'
        )
        self.client.force_login(self.admin_user)  ## helper function to force user login
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='test123',
            name='Test user full name'
        )
        self.instrument = Instrument(name='test', symbol='test', category='test', price=5)
        self.instrument.save()

        self.asset = Asset(owner=self.user, instrument=self.instrument, quantity=5)
        self.asset.save()
        self.buy_transaction = BuyTransaction(owner=self.user, instrument=self.instrument, quantity=5,
                                              created_at=datetime.datetime.now())
        self.buy_transaction.save()
        self.sell_transaction = BuyTransaction(owner=self.user, instrument=self.instrument, quantity=5,
                                              created_at=datetime.datetime.now())
        self.sell_transaction.save()

    def test_users_listed(self):
        """Test that users are listed on user page"""
        url = reverse('admin:core_user_changelist')  ## generate user list page, check django admin docs
        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_user_change_page(self):
        """Test that the User edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])  # /admin/core/user/1
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_create_user_page(self):
        """Test that the crate user page works"""
        url = reverse('admin:core_user_add')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_instrument_listed(self):
        """Test that created instrument is listed on admin page"""
        url = reverse('admin:core_instrument_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.instrument.name)
        self.assertContains(response, self.instrument.symbol)

    def test_asset_listed(self):
        """Test that created instrument is listed on admin page"""
        url = reverse('admin:core_asset_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.asset.instrument)
        self.assertContains(response, self.asset.quantity)

    def test_buy_transaction_listed(self):
        """Test that created instrument is listed on admin page"""
        url = reverse('admin:core_buytransaction_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.buy_transaction.instrument)
        self.assertContains(response, self.buy_transaction.quantity)

    def test_sell_transaction_listed(self):
        """Test that created instrument is listed on admin page"""
        url = reverse('admin:core_selltransaction_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.sell_transaction.instrument)
        self.assertContains(response, self.sell_transaction.quantity)