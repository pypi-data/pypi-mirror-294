""" Utils for subscriptions. """

from . import exceptions, schemas, enums


def validate_subscription_is_active(subscription: schemas.Subscription):
    """
    Validate if the subscription is active.
    """
    if not subscription.status == enums.Status.ACTIVE:
        raise exceptions.SubscriptionIsNotActive()
