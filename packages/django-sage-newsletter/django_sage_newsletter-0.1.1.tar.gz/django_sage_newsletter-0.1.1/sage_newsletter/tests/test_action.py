import pytest
from django.contrib.admin import AdminSite

from sage_newsletter.models import NewsletterSubscriber
from sage_newsletter.admin import NewsletterSubscriptionActions

@pytest.mark.django_db
def test_confirm_subscriptions():
    # Create some newsletter subscribers
    subscriber1 = NewsletterSubscriber.objects.create(email="user1@example.com", confirmed=False)
    subscriber2 = NewsletterSubscriber.objects.create(email="user2@example.com", confirmed=False)

    # Create a queryset with these subscribers
    queryset = NewsletterSubscriber.objects.filter(id__in=[subscriber1.id, subscriber2.id])

    # Simulate the admin action
    action = NewsletterSubscriptionActions.confirm_subscriptions
    action(modeladmin=None, request=None, queryset=queryset)

    # Refresh from DB to get the latest state
    subscriber1.refresh_from_db()
    subscriber2.refresh_from_db()

    # Check that the subscribers are confirmed
    assert subscriber1.confirmed is True
    assert subscriber2.confirmed is True

@pytest.mark.django_db
def test_deactivate_subscriptions():
    # Create some newsletter subscribers
    subscriber1 = NewsletterSubscriber.objects.create(email="user1@example.com", is_active=True)
    subscriber2 = NewsletterSubscriber.objects.create(email="user2@example.com", is_active=True)

    # Create a queryset with these subscribers
    queryset = NewsletterSubscriber.objects.filter(id__in=[subscriber1.id, subscriber2.id])

    # Simulate the admin action
    action = NewsletterSubscriptionActions.deactivate_subscriptions
    action(modeladmin=None, request=None, queryset=queryset)

    # Refresh from DB to get the latest state
    subscriber1.refresh_from_db()
    subscriber2.refresh_from_db()

    # Check that the subscribers are deactivated
    assert subscriber1.is_active is False
    assert subscriber2.is_active is False
