import os
from dotenv import load_dotenv

# import .env file
load_dotenv()

#driver path setting
driver_path = os.getenv('DRIVER_PATH')

#invoice save directory setting
invoice_dir = os.getenv('INVOICE_DIR')

#Amazon Link
amazon_address="https://www.amazon.co.jp/"

#Amazon login info setting
login_link="nav-link-accountList"
email_input_id="ap_email"
your_email=os.getenv('EMAIL')
continue_button_id="continue"
password_input_id="ap_password"
your_password=os.getenv('PASSWORD')
login_button_id="signInSubmit"

#Amazon order history setting
order_history_link="nav-orders"