import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone as tz
from django.utils.translation import gettext_lazy as _

from .helpers.text_choices import ContentPreferences, FrequencyPreferences


class NewsletterSubscriber(models.Model):
    """Newsletter Subscriber."""

    email = models.EmailField(
        unique=True,
        verbose_name=_("Email Address"),
        help_text="The email address of the subscriber.",
        db_comment="Unique email address used for newsletter subscription.",
    )
    date_subscribed = models.DateTimeField(
        default=tz.now,
        verbose_name=_("Date Subscribed"),
        help_text="The date and time when the subscription was created.",
        db_comment="Timestamp of when the subscriber was added to the list.",
    )
    confirmed = models.BooleanField(
        default=False,
        verbose_name=_("Confirmed Subscription"),
        help_text="Whether the subscriber has confirmed their email address.",
        db_comment="Boolean flag indicating confirmed subscription status.",
    )
    unsubscribe_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name=_("Unsubscribe Token"),
        help_text="A unique token used for securely unsubscribing from the newsletter.",
        db_comment="Unique token for secure unsubscribe functionality.",
    )
    preferences = models.CharField(
        max_length=50,
        choices=ContentPreferences.choices,
        default="NEWS",
        verbose_name=_("Content Preferences"),
        help_text="The type of content the subscriber prefers to receive.",
        db_comment="Subscriber's content preference selection.",
    )
    frequency = models.CharField(
        max_length=50,
        choices=FrequencyPreferences.choices,
        default="WEEKLY",
        verbose_name=_("Frequency Preferences"),
        help_text="How often the subscriber wishes to receive the newsletter.",
        db_comment="Subscriber's preferred frequency of newsletter delivery.",
    )
    language = models.CharField(
        max_length=10,
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE,
        verbose_name=_("Language Preference"),
        help_text="The preferred language for the newsletter.",
        db_comment="Subscriber's preferred language for the newsletter.",
    )
    gdpr_consent = models.BooleanField(
        default=False,
        verbose_name=_("GDPR Consent"),
        help_text="Whether the subscriber has given consent under GDPR.",
        db_comment="Flag indicating GDPR consent has been given by the subscriber.",
    )
    last_sent = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Last Newsletter Sent"),
        help_text="The date and time when the last newsletter was sent to this subscriber.",
        db_comment="Timestamp of the last newsletter sent to the subscriber.",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active"),
        help_text="Whether the subscription is currently active.",
        db_comment="Boolean flag indicating whether the subscription is active.",
    )

    objects = models.Manager()

    class Meta:
        """Meta."""

        verbose_name = _("Newsletter Subscriber")
        verbose_name_plural = _("Newsletter Subscribers")
        db_table = "sage_newsletter_subscriber"
        db_table_comment = "Table for storing newsletter subscriber information."

    def __str__(self):
        return self.email

    def __repr__(self):
        return self.email
