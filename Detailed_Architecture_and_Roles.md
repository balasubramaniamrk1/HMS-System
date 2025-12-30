# Detailed System Architecture & Roles Document

**Project:** HealthPlus Management System (HMS)
**Date:** December 24, 2025
**Version:** 1.0

---

## 1. User Roles & Access Control Matrix

The application uses a **Role-Based Access Control (RBAC)** system. Users are assigned to specific Groups, which determine their access levels.

| Role / Group | Description | Accessible Modules | Key Permissions |
| :--- | :--- | :--- | :--- |
| **Admin (Superuser)** | Full System Access | All Modules + Admin Panel | Manage Users, Groups, Database, View all logs. |
| **Doctors** | Medical Professionals | Doctor Console, Reports | • Book/Reschedule Appointments<br>• Conduct Consultations<br>• Write Prescriptions<br>• View *Own* Patient Reports |
| **Inventory Managers** | Supply Chain Staff | Inventory Dashboard, AMC | • Add/Edit Equipment & Vendors<br>• Manage AMCs<br>• Track Consumables<br>• View QR Codes |
| **Staff** | Reception / Front Desk | Staff Dashboard, Attendance | • Book Appointments (for patients)<br>• Check-In/Check-Out Patients<br>• Mark Attendance (Self) |
| **Public User** | Unauthenticated | Core Pages, Reviews | • View Doctors/Departments<br>• Book Appointment (Public Form)<br>• Read Reviews |

---

## 2. Functional Modules & Database Schema (Table Level)

### A. Inventory Management (`apps.inventory`)
**Purpose:** Track hospital assets, maintain stock levels, and manage vendor contracts.

#### 1. Table: `Vendor`
*Stores details of suppliers and service providers.*
* **name** (Char): Company name.
* **contact_person** (Char): Point of contact.
* **phone/email** (Char/Email): Contact info.
* **rating** (Int): Performance rating (1-5).

#### 2. Table: `EquipmentCategory`
*Classifies assets (e.g., "Imaging", "Surgical", "IT").*
* **name** (Char): Category name.
* **description** (Text): Details.

#### 3. Table: `Equipment`
*The core asset table.*
* **name**, **serial_number** (Char): Identification.
* **vendor** (FK -> Vendor): Supplier linkage.
* **status** (Choice): `new`, `working`, `repair`, `retired`.
* **purchase_date**, **warranty_expiry** (Date): Lifecycle tracking.
* **cost**, **useful_life** (Decimal/Int): For depreciation.
* **qr_code** (Image): Auto-generated QR for tracking.

#### 4. Table: `MaintenanceContract` (AMC)
*Tracks annual maintenance agreements.*
* **equipment** (FK -> Equipment): The asset covered.
* **vendor** (FK -> Vendor): Service provider.
* **contract_start**, **contract_end** (Date): Validity period.
* **cost** (Decimal): Contract value.
* **is_active** (Property): Calculated status based on today's date.

#### 5. Table: `Consumable`
*Tracks disposable inventory (gloves, medicines).*
* **name** (Char): Item name.
* **quantity_in_stock** (Int): Current count.
* **minimum_stock_level** (Int): Threshold for "Low Stock" alerts.

---

### B. Clinical Management (`apps.appointments`)
**Purpose:** Handle the patient journey from booking to prescription.

#### 1. Table: `AppointmentRequest`
*Patient booking requests.*
* **name**, **phone** (Char): Patient details.
* **doctor** (FK -> Doctor): Selected physician.
* **date**, **time** (Date/Char): Requested slot.
* **status** (Choice): `pending`, `confirmed`, `completed`, `cancelled`.

#### 2. Table: `Consultation`
*Medical record for a completed appointment.*
* **appointment** (OneToOne -> AppointmentRequest): Links to the booking.
* **diagnosis** (Text): Doctor's findings.
* **doctor_notes** (Text): Internal observations.

#### 3. Table: `PrescriptionItem`
*Individual medicines prescribed during a consultation.*
* **consultation** (FK -> Consultation): Parent record.
* **medicine_name** (Char): Name of the drug.
* **dosage**, **duration** (Char): e.g., "1-0-1", "5 days".

---

### C. Doctor Management (`apps.doctors`)
**Purpose:** Manage doctor profiles and departments.

#### 1. Table: `Department`
*Medical specialities (e.g., Cardiology).*
* **name** (Char): Department name.
* **slug** (Slug): URL-friendly name.

#### 2. Table: `Doctor`
*Physician profiles.*
* **user** (OneToOne -> auth.User): Links to login credentials.
* **department** (FK -> Department): Speciality.
* **qualifications**, **specialization** (Char): Profesional details.
* **is_featured** (Bool): Highlight on homepage.

---

### D. Staff Management (`apps.staff_mgmt`)
**Purpose:** Internal HR and attendance tracking.

#### 1. Table: `StaffProfile`
*Employee details.*
* **user** (OneToOne -> auth.User): Login link.
* **employee_id** (Char): Unique HR ID.
* **designation** (Char): Job role.

#### 2. Table: `Attendance`
*Daily logs.*
* **staff** (FK -> StaffProfile): Employee.
* **date** (Date): Attendance date.
* **check_in**, **check_out** (Time): Punch times.
* **status** (Choice): `present`, `absent`, `half_day`.

---

## 3. Key Workflows / Processes

### 1. The Appointment Lifecycle
1.  **Booking:** Patient fills form -> `AppointmentRequest` created (Status: `pending`).
2.  **Confirmation:** Staff calls patient -> Updates status to `confirmed`.
3.  **Check-In:** Patient arrives -> Staff marks `checked_in`.
4.  **Consultation:** Doctor opens Console -> Starts Consultation -> Fills Diagnosis.
5.  **Prescription:** Doctor adds medicines -> System generates PDF.
6.  **Completion:** Consultation saved -> Appointment marked `completed`.

### 2. Inventory Procurement & AMC
1.  **Add Vendor:** Manager registers a new supplier.
2.  **Add Equipment:** Manager logs new asset -> Links to Vendor -> QR Code generated.
3.  **AMC Management:** Manager creates Contract -> Links Asset + Vendor.
    *   *System Check:* Daily check for expiry dates -> Shows alerts on Dashboard.

### 3. Staff Attendance
1.  **Login:** Staff logs in.
2.  **Check-In:** Clicks "Check In" -> System captures timestamp.
3.  **Work:** Performs duties.
4.  **Check-Out:** Clicks "Check Out" -> System captures end time.
