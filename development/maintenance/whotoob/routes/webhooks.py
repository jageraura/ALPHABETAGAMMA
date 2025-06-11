from flask import Blueprint, request, jsonify
import stripe
from models.user import User
from flask import current_app
from models.user import User

webhooks_bp = Blueprint('webhooks', __name__)

stripe.api_key = "YOUR_SECRET_KEY"
endpoint_secret = "YOUR_WEBHOOK_SECRET"

@webhooks_bp.route('/stripe-webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return jsonify({"error": "Invalid payload"}), 400
    except stripe.error.SignatureVerificationError:
        return jsonify({"error": "Invalid signature"}), 400

    # Handle subscription events
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_email = session['customer_email']
        
        # Find user and update subscription status
        user = User.query.filter_by(email=user_email).first()
        if user:
            user.is_premium = True
            db.session.commit()
    
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        customer_email = stripe.Customer.retrieve(subscription['customer'])['email']
        
        # Find user and remove premium status
        user = User.query.filter_by(email=customer_email).first()
        if user:
            user.is_premium = False
            db.session.commit()

    return jsonify({'status': 'success'}), 200
