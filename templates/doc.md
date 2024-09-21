### 1. **Order Medicine (`/ordermedicine/<medicines>`)**
- **Route**: `GET /ordermedicine/<medicines>`
- **Description**: Orders medicines, where `<medicines>` is a comma-separated list of medicine names.
- **Example Request**:
  ```bash
  curl https://carepoint-ecru.vercel.app/ordermedicine/Paracetamol,Ibuprofen
  ```
- **Response**:
  ```json
  [
    {"name": "Paracetamol", "price": 50, "availability": true},
    {"name": "Ibuprofen", "price": 100, "availability": false}
  ]
  ```

---

### 2. **Get Bed Availability (`/getbedavailability/<date>`)**
- **Route**: `GET /getbedavailability/<date>`
- **Description**: Fetches available beds for a specific date.
- **Example Request**:
  ```bash
  curl https://carepoint-ecru.vercel.app/getbedavailability/2024-09-17
  ```
- **Response**:
  ```json
  [
    {"bed_id": "B001", "type": "ICU", "status": "available"},
    {"bed_id": "B002", "type": "General", "status": "available"}
  ]
  ```

---

### 3. **Book an Appointment (`/bookappointment/<doctor>/<datetime>`)**
- **Route**: `GET /bookappointment/<doctor>/<datetime>`
- **Description**: Books an appointment with a doctor at a specified date and time.
- **Example Request**:
  ```bash
  curl https://carepoint-ecru.vercel.app/bookappointment/Dr.%20Benjamin%20Lee/2024-09-20%2014:00
  ```
- **Response**:
  ```json
  {"message": "Appointment booked", "id": "64f1b5ac12b4c24e004d6c33"}
  ```

---

### 4. **Book a Bed (`/bookbed/<date>`)**
- **Route**: `GET /bookbed/<date>`
- **Description**: Books the first available bed for a specified date.
- **Example Request**:
  ```bash
  curl https://carepoint-ecru.vercel.app/bookbed/2024-09-17
  ```
- **Response** (if available bed found):
  ```json
  {"message": "Bed B001 booked successfully"}
  ```

- **Response** (if no available beds):
  ```bash
  "No beds available for booking on this date"
  ```

---
