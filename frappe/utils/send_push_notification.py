import os
import firebase_admin
from firebase_admin import credentials, messaging
import frappe


def find_file_in_parents(filename, current_dir=None):
    if current_dir is None:
        current_dir = os.path.dirname(os.path.realpath(__file__))

    # Build the absolute path of the file in the current directory
    potential_path = os.path.join(current_dir, filename)

    # Check if the file exists
    if os.path.exists(potential_path):
        return potential_path

    # If we have reached the root directory and haven't found the file, return None
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    if current_dir == parent_dir:
        return None

    # Recursively check in the parent directory
    return find_file_in_parents(filename, parent_dir)

# Example usage
file = find_file_in_parents("firebase.json")
cred = credentials.Certificate(file) 
app =  firebase_admin.initialize_app(cred)

def send_notification(fcm_token, title, body, data=None):
    notification = messaging.Notification(title=title, body=body)
    message = messaging.Message(notification=notification, token=fcm_token, data=data)
    messaging.send(message)


def get_user_fcm_token_by_email(email):
    fcm_token = frappe.db.get_value("Employee", {"user_id": email}, ["custom_fcm_token"])
    print("inside token function:", email, fcm_token)
    return fcm_token


def get_doc_owner_name(email):
    name = frappe.db.get_value("Employee", {"user_id": email}, ["employee_name"])
    return name
