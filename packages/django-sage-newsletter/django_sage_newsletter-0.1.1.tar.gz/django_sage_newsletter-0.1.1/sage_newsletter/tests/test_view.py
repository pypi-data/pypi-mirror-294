import pytest
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.exceptions import ImproperlyConfigured
from django.test import RequestFactory
from django.urls import reverse
from django.views.generic import TemplateView
from sage_newsletter.forms import NewsletterSubscriptionForm
from sage_newsletter.models import NewsletterSubscriber
from sage_newsletter.views import NewsletterViewMixin


class TestNewsletterView(NewsletterViewMixin, TemplateView):
    """
    A simple test view to use the NewsletterViewMixin.
    """
    template_name = "test_template.html"
    success_url_name = "home"  # Assuming 'home' is a valid URL name


def add_middleware(request):
    """Helper function to add necessary middleware to the request."""
    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request)
    request.session.save()

    middleware = MessageMiddleware(lambda req: None)
    middleware.process_request(request)


@pytest.mark.django_db
def test_newsletter_view_mixin_improperly_configured():
    """
    Test that the mixin raises an ImproperlyConfigured exception if success_url_name is not set.
    """
    with pytest.raises(ImproperlyConfigured):
        class InvalidView(NewsletterViewMixin, TemplateView):
            template_name = "test_template.html"
        InvalidView()  # This should raise the ImproperlyConfigured exception


@pytest.mark.django_db
def test_get_context_data():
    """
    Test that the newsletter form is added to the context.
    """
    view = TestNewsletterView()
    request = RequestFactory().get("/")
    view.setup(request)

    context = view.get_context_data()

    assert "newsletter_form" in context, "The form should be in the context."
    assert isinstance(context["newsletter_form"], NewsletterSubscriptionForm), "The form should be an instance of NewsletterSubscriptionForm."


@pytest.mark.django_db
def test_post_valid_form():
    """
    Test that a valid form submission redirects and sets the success message.
    """
    view = TestNewsletterView()
    request = RequestFactory().post("/", data={"email": "test@example.com"})

    # Add session and message middleware
    add_middleware(request)

    view.setup(request)

    response = view.post(request)

    assert response.status_code == 302, "The response should be a redirect."
    assert len(request._messages) == 1, "There should be one success message."
    assert list(request._messages)[0].message == "You have successfully subscribed to the newsletter."

    # Verify that the subscriber was actually created
    assert NewsletterSubscriber.objects.filter(email="test@example.com").exists()


# @pytest.mark.django_db
# def test_post_invalid_form():
#     """
#     Test that an invalid form submission re-renders the template with errors.
#     """
#     view = TestNewsletterView()
#     request = RequestFactory().post("/", data={"email": ""})  # Invalid because email is required

#     # Add session and message middleware
#     add_middleware(request)

#     view.setup(request)

#     response = view.post(request)

#     assert response.status_code == 200, "The response should render the template again."
#     assert "newsletter_form" in response.context_data, "The form should be in the context."
#     assert response.context_data["newsletter_form"].errors, "The form should contain errors."

