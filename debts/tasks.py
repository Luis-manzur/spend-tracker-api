"""Celery tasks."""

from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from debts.models import Debt


@shared_task()
def send_debt_email(debt: Debt):
    """Send account verification link to given user."""
    subject = "You have a new debt!"
    from_email = settings.EMAIL_HOST_USER
    content = render_to_string(
        "emails/debts.html",
        {"from_user": debt.from_user, "to_user": debt.to_user, "amount": debt.amount},
    )
    msg = EmailMultiAlternatives(subject, content, from_email, [debt.to_user.email])
    msg.attach_alternative(content, "text/html")
    msg.send()


@shared_task()
def send_debt_paid_email(debt: Debt):
    """Send account verification link to given user."""
    subject = "Your debt has been paid!"
    from_email = settings.EMAIL_HOST_USER
    content = render_to_string(
        "emails/debt_paid.html",
        {"from_user": debt.from_user, "to_user": debt.to_user, "amount": debt.amount},
    )
    msg = EmailMultiAlternatives(subject, content, from_email, [debt.to_user.email])
    msg.attach_alternative(content, "text/html")
    msg.send()
