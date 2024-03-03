from flask import request, jsonify
from config import app, db
from models import Contact
from sqlalchemy.exc import IntegrityError
import re

def is_valid_email(email):
    """Check if the email is valid."""
    email_regex = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
    return re.match(email_regex, email, re.IGNORECASE)


@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()
    json_contacts = [contact.to_json() for contact in contacts]
    return jsonify({"contacts": json_contacts})


@app.route("/create_contact", methods=["POST"])
def create_contact():
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")
    
    # Check if all fields are present
    if not first_name or not last_name or not email:
        return jsonify({"message": "You must include a first name, last name, and email!"}), 400
    
    # Validate email format
    if not is_valid_email(email):
        return jsonify({"message": "Invalid email format. Please enter a valid email."}), 400
    
    new_contact = Contact(first_name=first_name, last_name=last_name, email=email)
    try:
        db.session.add(new_contact)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()  # Roll back the session to a clean state
        return jsonify({"message": "This email already exists. Please use a different email."}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": "User created successfully!"}), 201


@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    contact = db.session.get(Contact, user_id)
    if not contact:
        return jsonify({"message": "User not found"}), 404
    
    data = request.json
    new_email = data.get("email")
    
    # Validate email format if email is being updated
    if new_email and not is_valid_email(new_email):
        return jsonify({"message": "Invalid email format. Please enter a valid email."}), 400
    
    # Update fields
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = new_email if new_email else contact.email
    
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()  # Roll back the session to a clean state
        return jsonify({"message": "This email already exists. Please use a different email."}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred: " + str(e)}), 400
    
    return jsonify({"message": "User updated successfully!"}), 200


@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    contact = db.session.get(Contact, user_id)
    
    if not contact:
        return jsonify({"message": "User not found"}), 404
    
    db.session.delete(contact)
    db.session.commit()
    
    return jsonify({"message": "User deleted!"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)