from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
import certifi
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
import ssl

# Load the .env file
load_dotenv()

# Get the MongoDB connection string from environment variables
connection_string = os.environ.get('CONNECTION')
sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')

# Connect to MongoDB cluster
client = MongoClient(connection_string, tlsCAFile=certifi.where())

# Access the hospital database
db = client['HospitalData']

app = Flask(__name__)

# Route for the homepage
@app.route('/')
def index():
    return render_template("index.html")

# Route for the homepage
@app.route('/documentation')
def documentation():
    return render_template("documentation.html")

# Route for ordering medicines
@app.route('/ordermedicine/<medicine>/<emailId>')
def ordermedicine(medicine,emailId):
    all_meds = medicine.lower()
    print(all_meds, medicine, "------------")
    collection = db['medicines']
    ordered_meds = collection.find({"name":  all_meds})
    collection = db['medicineorders']
    # Prepare response 
    meds_list = {"name": ordered_meds[0]["name"], "price": ordered_meds[0]["price"], "availability": ordered_meds[0]["availability"]}
    result = collection.insert_one({"email": emailId, "order": meds_list})

    subject = "Medicine Order Confirmation - Care Point Hospital"
    
    # Customize the email content using the parameters medicine_name, price, and emailid
    html_content = f"""
    <html>
    <body>
        <h2>Medicine Order Successful - Care Point Hospital</h2>
        <p>Dear Customer,</p>
        <p>Your order for <strong>{medicine}</strong> has been successfully placed.</p>
        <p><strong>Order Details:</strong></p>
        <ul>
            <li><strong>Medicine Name:</strong> {medicine}</li>
            <li><strong>Total Price:</strong> ${ordered_meds[0]["price"]}</li>
            <li><strong>Email:</strong> {emailId}</li>
        </ul>
        <p>We will notify you once your order is ready for pickup or delivery.</p>
        <p>Thank you for choosing Care Point Hospital for your medical needs!</p>
        <p>Best Regards,<br>Care Point Hospital Pharmacy Team</p>
    </body>
    </html>
    """

    send_email(emailId, subject, html_content)

    return jsonify(meds_list) if meds_list else "Medicines not found"


# @app.route('/ordermedicine/<medicines>/<emailId>')
# def ordermedicine(medicines,emailId):
#     all_meds = medicines
#     collection = db['medicines']
#     ordered_meds = collection.find({"name": all_meds, "emailId": emailId})
    
#     # Prepare response
#     meds_list = [{"name": med["name"], "price": med["price"], "availability": med["availability"]} for med in ordered_meds]
    
#     return jsonify(meds_list) if meds_list else "Medicines not found"

# Route for checking bed availability on a specific date
@app.route('/getbedavailability/<date>')
def getbedavailability(date):
    collection = db['beds']
    available_beds = collection.find({"date": date, "status": "available"})
    
    # Prepare response with multiple available beds
    beds_list = [{"bed_id": bed["bed_id"], "type": bed["type"], "status": bed["status"]} for bed in available_beds]
    
    return jsonify(beds_list) if beds_list else jsonify({"response": "No beds available on this date"})

# Route for booking an appointment with a doctor
@app.route('/bookappointment/<doctor>/<datetime>/<emailId>')
def bookappointment(doctor, datetime, emailId):
    collection = db['appointments']
    result = collection.insert_one({"doctor": doctor, "datetime": datetime, "status": "booked", "emailId": emailId})
    subject = "Doctor Appointment Confirmation - Care Point Hospital"
    
    # Customize the email content using the parameters doctor_name, emailid, and date
    html_content = f"""
    <html>
    <body>
        <h2>Appointment Booking Successful - Care Point Hospital</h2>
        <p>Dear Patient,</p>
        <p>Your appointment with Dr. <strong>{doctor}</strong> has been successfully confirmed.</p>
        <p><strong>Appointment Details:</strong></p>
        <ul>
            <li><strong>Doctor's Name:</strong> Dr. {doctor}</li>
            <li><strong>Appointment Date:</strong> {datetime}</li>
            <li><strong>Email:</strong> {emailId}</li>
        </ul>
        <p>Please arrive 15 minutes early and bring any relevant medical records with you.</p>
        <p>We look forward to seeing you!</p>
        <p>Best Regards,<br>Care Point Hospital Team</p>
    </body>
    </html>
    """
    send_email(emailId, subject ,html_content )

    
    return jsonify({"message": "Appointment booked", "id": str(result.inserted_id)})

# Route for booking a bed on a specific date
@app.route('/bookbed/<date>/<emailId>')
def bookbed(date, emailId):
    collection = db['beds']
    
    # Find the first available bed for the given date
    available_bed = collection.find_one({"date": date, "status": "available"})
    
    if available_bed:
        # Mark the bed as booked
        result = collection.update_one({"_id": available_bed["_id"]}, {"$set": {"status": "booked", "emailId": emailId}})
        subject = "Bed Booking Confirmation - Care Point Hospital"
    
    # Customize the email content using the parameters id, emailid, and date
        html_content = f"""
        <html>
        <body>
            <h2>Bed Booking Successful - Care Point Hospital</h2>
            <p>Dear Patient,</p>
            <p>We are pleased to inform you that your bed booking at Care Point Hospital has been successfully confirmed.</p>
            <p><strong>Booking Details:</strong></p>
            <ul>
                <li><strong>Booking ID:</strong> {available_bed["_id"]}</li>
                <li><strong>Email:</strong> {emailId}</li>
                <li><strong>Date of Booking:</strong> {date}</li>
            </ul>
            <p>Thank you for choosing Care Point Hospital. We are committed to providing you with the best care.</p>
            <p>Best Regards,<br>Care Point Hospital Team</p>
        </body>
        </html>
        """
        send_email(emailId, subject ,html_content )
        return jsonify({"message": f"Bed {available_bed['bed_id']} booked successfully"})
    else:
        return jsonify({"message":"No beds available for booking on this date"})



# Disable SSL verification (insecure)
ssl._create_default_https_context = ssl._create_unverified_context


def send_email(to_email,subject,html_content):
    message = Mail(
        from_email='aakashferrari@gmail.com',
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )

    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        print(f"Email sent successfully! Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")



if __name__ == "__main__":
    app.run(debug=True, port=5000)
