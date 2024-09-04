from django import forms
from django.core.exceptions import ValidationError

from .models import NewsletterSubscriber


class NewsletterSubscriptionForm(forms.ModelForm):
    """A Django ModelForm for handling newsletter subscriptions.

    This form is associated with the NewsletterSubscriber model and is used for
    subscribing users to a newsletter service. It handles both new subscriptions
    and the reactivation of existing but inactive subscriptions.

    The form only exposes the 'email' field for input, as it's the primary field
    required for newsletter subscriptions.

    Attributes:
        Meta: An inner class that defines form-specific details like the associated model
              and the fields to be included in the form.

    """

    class Meta:
        model = NewsletterSubscriber
        fields = ["email"]

    def clean_email(self):
        """Validates and processes the email field input.

        Checks if the provided email already exists in the database. If it does, the method
        determines whether the associated subscription is active or inactive. Active
        subscriptions will cause the method to raise a ValidationError, indicating that
        the email is already in use. Inactive subscriptions will be reactivated.

        Returns:
            str: The cleaned email data.

        Raises:
            ValidationError: If the email address is already subscribed and active.

        """
        email = self.cleaned_data.get("email")
        try:
            subscriber = NewsletterSubscriber.objects.get(email=email)
            if subscriber.is_active:
                raise ValidationError(
                    "This email address is already subscribed and active."
                )
            else:
                # Mark the subscriber as reactivated and save
                self.instance = subscriber
                self.instance.is_active = True
                self.instance.save()
        except NewsletterSubscriber.DoesNotExist:
            # Email not found, it's a new subscriber
            pass
        return email
