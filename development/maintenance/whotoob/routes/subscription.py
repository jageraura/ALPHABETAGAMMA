from flask import Blueprint, request, jsonify
import stripe

subscription_bp = Blueprint('subscription', __name__)

# Set your Stripe secret key
stripe.api_key = "YOUR_SECRET_KEY"

@subscription_bp.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        data = request.json
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='subscription',
            line_items=[{'price': 'YOUR_STRIPE_PRICE_ID', 'quantity': 1}],
            success_url='https://yourwebsite.com/success',
            cancel_url='https://yourwebsite.com/cancel',
        )
        return jsonify({'sessionId': checkout_session.id})
    except stripe.error.StripeError as e:
        return jsonify({'error': str(e)}), 400

@subscription_bp.route('/verify-subscription', methods=['GET'])
def verify_subscription():
    user_id = request.args.get('user_id')
    # Placeholder: Query your database to check premium status
    is_premium = check_user_subscription(user_id)
    
    if is_premium:
        return jsonify({'status': 'Active'})
    else:
        return jsonify({'status': 'Inactive'}), 403

def check_user_subscription(user_id):
    # Replace this with a real database lookup
    return False  # Default to non-premium user
