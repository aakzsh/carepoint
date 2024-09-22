# Care Point Hospital API

### Live Project: **[Care Point](https://carepoint-ecru.vercel.app/)**

This repository contains the Flask backend for the Care Point Hospital AI assistant, which integrates with IBM Watson Orchestrate to automate hospital services like appointment booking, bed availability, medicine ordering, and more. This project is being submitted for the **Orchestrate Path** challenge.

## Features
- AI-powered appointment booking and bed management
- Medicine ordering and patient information access
- Real-time data storage and retrieval using MongoDB and OpenAPI
- Seamless integration with Watson Orchestrate for AI-driven automation
- Twilio Segment integration for knowledge base
- Emergency contact handling

## How to Run Manually

### Prerequisites:
- Python 3.x
- MongoDB connection string (Please setup a database and cluster)

### Steps:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/aakzsh/carepoint
   cd https://github.com/aakzsh/carepoint
   ```

2. **Set Up Environment Variables**
   - Get your own MongoDB connection string and create a `.env` file in the root directory.
   - Add the following line to the `.env` file:
     ```
     CONNECTION=<your-mongodb-connection-string>
     ```

3. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application**
   You can start the app with either of these commands:
     ```bash
     python app.py
     ```
     or
     
     ```bash
     flask run
     ```

Your Flask server should now be running locally! 🎉
