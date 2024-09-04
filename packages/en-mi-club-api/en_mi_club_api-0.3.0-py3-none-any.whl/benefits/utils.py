""" Utils and validations for benefits. """

from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session
from benefits import exceptions
from benefits.in_person_benefits import crud as in_person_benefits_crud
from benefits.online_benefits import crud as online_benefits_crud
from subscriptions import (
    crud as subscription_crud,
    schemas as subscription_schemas,
    utils as subscriptions_utils,
)
from plans import crud as plans_crud, schemas as plans_schemas


def validate_if_user_can_get_benefit(
    db: Session, user_id: int, benefit_id: int, is_online: bool
):
    """
    Validate if the user can obtain a benefit based on their subscription limits.
    This function orchestrates the other validation functions.
    """
    subscription = subscription_crud.get_user_subscription(db, user_id)
    plan = plans_crud.get_plan_by_id(db, subscription.plan_id)

    start_date, end_date = get_subscription_dates(plan, subscription)

    subscriptions_utils.validate_subscription_is_active(subscription)

    validate_if_user_exceeded_max_amount_of_benefits_given(
        db, user_id, plan, start_date, end_date
    )
    validate_if_user_exceeded_max_amont_of_uses_per_benefit_given(
        db, user_id, benefit_id, plan, start_date, end_date, is_online
    )


def validate_if_user_exceeded_max_amount_of_benefits_given(
    db: Session,
    user_id: int,
    plan: plans_schemas.Plan,
    start_date: datetime,
    end_date: datetime,
):
    """
    Validate if the user has reached the limit of total benefits for the current month.
    """
    benefits_obtained = (
        in_person_benefits_crud.count_in_person_benefits_obtained_by_user(
            db, user_id, start_date, end_date
        )
        + online_benefits_crud.count_online_benefits_obtained_by_user(
            db, user_id, start_date, end_date
        )
    )

    if benefits_obtained >= plan.max_amount_of_benefits_given:
        raise exceptions.BenefitLimitExceededError()


def validate_if_user_exceeded_max_amont_of_uses_per_benefit_given(
    db: Session,
    user_id: int,
    benefit_id: int,
    plan: plans_schemas.Plan,
    start_date: datetime,
    end_date: datetime,
    is_online: bool,
):
    """
    Validate if the user has reached the limit for obtaining the same benefit.
    """
    if is_online:
        benefits_obtained_per_benefit = (
            online_benefits_crud.count_online_benefit_by_user_and_benefit(
                db, user_id, benefit_id, start_date, end_date
            )
        )
    else:
        benefits_obtained_per_benefit = (
            in_person_benefits_crud.count_in_person_benefit_by_user_and_benefit(
                db, user_id, benefit_id, start_date, end_date
            )
        )

    if (
        benefits_obtained_per_benefit
        >= plan.max_amont_of_uses_per_benefit_given
    ):
        raise exceptions.BenefitLimitExceededError()


def get_subscription_dates(
    plan: plans_schemas.Plan, subscription: subscription_schemas.Subscription
):
    """
    Calculate the start and end dates based on the subscription and plan.
    """
    start_date = subscription.created_at
    current_time = datetime.now()

    if plan.months_duration == 12:
        while start_date + relativedelta(months=1) <= current_time:
            start_date += relativedelta(months=1)

    end_date = start_date + relativedelta(months=1)

    return start_date, end_date
