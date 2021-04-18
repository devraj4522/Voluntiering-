import os
import stripe

def init_strip():
    stripe_keys = {
    'secret_key': os.environ['STRIPE_SECRET_KEY'],
    'publishable_key': os.environ['STRIPE_PUBLISHABLE_KEY']
    }

    stripe.api_key = stripe_keys['secret_key']
    return stripe_keys

def get_publishable_key(stripe_keys):
    public_key = stripe_keys["publishable_key"]
    return public_key