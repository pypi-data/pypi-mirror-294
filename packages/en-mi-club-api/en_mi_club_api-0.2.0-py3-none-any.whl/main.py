""" Main module for the FastAPI application. """

from fastapi import FastAPI
from user_entities.admin.endpoints import router as admin_router
from user_entities.users.endpoints import router as users_router
from user_entities.commerce.endpoints import router as account_commerce_router
from commerces.endpoints import router as commerce_router
from commerces.contact_form.endpoints import router as contact_form_router
from raffles.endpoints import router as raffles_router
from tickets.endpoints import router as tickets_router
from auth.endpoints import router as auth_router
from benefits.online_benefits.endpoints import router as online_benefits_router
from benefits.in_person_benefits.endpoints import (
    router as in_person_benefits_router,
)
from plans.endpoints import router as plans_router
from subscriptions.endpoints import router as subscriptions_router
from wallet.endpoints import router as wallets_router
from wallet.payment_requests.endpoints import router as payment_requests_router
from verification_code.endpoints import router as verification_code_router

app = FastAPI()

app.include_router(users_router)
app.include_router(raffles_router)
app.include_router(tickets_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(online_benefits_router)
app.include_router(in_person_benefits_router)
app.include_router(account_commerce_router)
app.include_router(commerce_router)
app.include_router(plans_router)
app.include_router(subscriptions_router)
app.include_router(wallets_router)
app.include_router(payment_requests_router)
app.include_router(contact_form_router)
app.include_router(verification_code_router)


@app.get("/")
def read_root():
    """Default route for the FastAPI application"""
    return {"message": "Hello, World!"}
