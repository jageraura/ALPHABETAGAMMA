from flask import Blueprint, request, jsonify
import stripe

subscription_bp = Blueprint('subscription', __name__)

stripe.api_key = "YOUR_SECRET_KEY"

@subscription_bp.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.json
    try:
        customer = stripe.Customer.create(email=data['email'], source=data['token'])
        stripe.Subscription.create(
            customer=customer.id,
            items=[{'plan': 'YOUR_STRIPE_PLAN_ID'}]
        )
        return jsonify({"message": "Subscription successful!"}), 200
    except stripe.error.StripeError as e:
        return jsonify({"error": str(e)}), 400
