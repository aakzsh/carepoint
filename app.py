from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
import certifi
import os

# Load the .env file
load_dotenv()

# Get the MongoDB connection string from environment variables
connection_string = os.environ.get('CONNECTION')

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
        return jsonify({"message": f"Bed {available_bed['bed_id']} booked successfully"})
    else:
        return jsonify({"message":"No beds available for booking on this date"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
