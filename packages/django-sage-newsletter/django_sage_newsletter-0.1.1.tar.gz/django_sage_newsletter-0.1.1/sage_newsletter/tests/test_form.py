import pytest
from django.core.exceptions import ValidationError

from sage_newsletter.forms import NewsletterSubscriptionForm
from sage_newsletter.models import NewsletterSubscriber


@pytest.mark.django_db
def test_newsletter_subscription_form_valid_new_subscriber():
    """
    Test that the form is valid when a new email is submitted.
    """
    form_data = {"email": "newuser@example.com"}
    form = NewsletterSubscriptionForm(data=form_data)

    assert form.is_valid(), "The form should be valid for a new email."


@pytest.mark.django_db
def test_newsletter_subscription_form_existing_active_subscriber():
    # Create an active subscriber
    active_subscriber = NewsletterSubscriber.objects.create(
        email="activeuser@example.com", is_active=True
    )

    form_data = {"email": "activeuser@example.com"}
    form = NewsletterSubscriptionForm(data=form_data)

    # Validate the form to populate cleaned_data
    is_valid = form.is_valid()
    
    # The form should not be valid since the email is already subscribed and active
    assert not is_valid, "The form should not be valid for an active email."

    # Check if the email field has the expected error
    assert "email" in form.errors, "The form should have an error for the email field."
    assert form.errors["email"] == ["This email address is already subscribed and active."]


@pytest.mark.django_db
def test_newsletter_subscription_form_existing_inactive_subscriber():
    """
    Test that the form reactivates an inactive subscription.
    """
    # Create an inactive subscriber
    inactive_subscriber = NewsletterSubscriber.objects.create(
        email="inactiveuser@example.com", is_active=False
    )

    form_data = {"email": "inactiveuser@example.com"}
    form = NewsletterSubscriptionForm(data=form_data)

    assert form.is_valid(), "The form should be valid for an inactive email."

    # Save the form and check if the subscription is reactivated
    form.save()
    inactive_subscriber.refresh_from_db()

    assert inactive_subscriber.is_active, "The subscriber should be reactivated."


@pytest.mark.django_db
def test_newsletter_subscription_form_blank_email():
    """
    Test that the form is invalid if the email is blank.
    """
    form_data = {"email": ""}
    form = NewsletterSubscriptionForm(data=form_data)

    assert not form.is_valid(), "The form should not be valid without an email."
    assert "email" in form.errors, "The form should have an error for the email field."
