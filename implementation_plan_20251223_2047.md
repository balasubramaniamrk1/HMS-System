# Implementation Plan: New Hospital Modules

## Goal Description
Implement four new key modules to enhance the Hospital Management System:
1.  **Staff Attendance**: Track daily attendance (Check-in/Check-out) for employees.
2.  **Social Media Reviews**: Aggregate and display public reviews from platforms like Facebook and YouTube.
3.  **Inventory & AMC Management**: Manage hospital equipment inventory and their Annual Maintenance Contracts (AMC).
4.  **System Generated Prescriptions**: Generate structured printable PDF prescriptions from consultation data.

## User Review Required
> [!IMPORTANT]
> **Prescription PDF Library**: We are using `ReportLab` as requested. It is a robust PDF library with **zero system dependencies** (unlike WeasyPrint which requires installing cairo/pango on the OS Level). This ensures easier deployment across Mac, Windows, and Linux.

> [!IMPORTANT]
> **Dashboard Refactoring**: We are merging the Staff Attendance widget into the main Appointment Dashboard to resolve a URL conflict and improve UX. We are also implementing a 2-column layout and "Work Hours" calculation.

> [!NOTE]
> **Social Media Integration**: Direct API integration (e.g., fetching real-time tweets) is complex and requires API keys. The initial plan assumes a **manual entry/scraping** approach or a "Featured Review" model where admins curate reviews.

## Proposed Changes

### 1. New App: Staff Management (`staff_mgmt`)
Handle staff details (beyond just auth users) and attendance.

#### [NEW] [models.py](file:///apps/staff_mgmt/models.py)
*   **Model `StaffProfile`**: Extension of `User` model (Designation, Department linkage, Employee ID).
*   **Model `Attendance`**:
    *   `staff` (ForeignKey)
    *   `date` (Date)
    *   `check_in` (Time)
    *   `check_out` (Time)
    *   `status` (Present/Absent/Leave)

#### [NEW] [views.py](file:///apps/staff_mgmt/views.py)
*   `check_in_out`: View for staff to mark attendance.
*   `attendance_report`: Admin view to see monthly attendance.

### 2. New App:### Reputation Management (Manual Entry)
#### [MODIFY] [models.py](file:///Users/balasubramaniam/Desktop/HMS/apps/reputation/models.py)
*   Ensure `Review` model has `is_featured`, `rating`, `platform` (icon support).
*   Use Django Admin for manual entry of top reviews.

#### [NEW] [views.py](file:///Users/balasubramaniam/Desktop/HMS/apps/reputation/views.py)
*   Create `public_reviews` view to display featured reviews (e.g., as a carousel snippet).
*   Create `admin_dashboard` view (optional, if standard admin is insufficient).ok, YouTube, Google, Twitter).
*   **Model `Review`**:
    *   `platform` (ForeignKey)
    *   `author_name`
    *   `content` (Text)
    *   `rating` (1-5 Stars)
    *   `review_date`
    *   `is_featured` (Boolean: to show on home page)

### 3. New App: Inventory Management (`inventory`)
Track equipment and contracts.

#### [NEW] [models.py](file:///Users/balasubramaniam/Desktop/HMS/apps/inventory/models.py)
*   **Model `EquipmentCategory`**: (e.g., Surgical, Diagnostic, IT).
*   **Model `Equipment`**:
    *   `name`, `serial_number`, `model_number`
    *   `purchase_date`, `warranty_expiry`
    *   `location` (Room/Department)
    *   `status` (Active/Under Repair/Retired)
*   **Model `MaintenanceContract` (AMC)**:
    *   `equipment` (ForeignKey)
    *   `provider_name`
    *   `contract_start`, `contract_end`
    *   `cost`, `support_contact`

#### [NEW] [views.py](file:///Users/balasubramaniam/Desktop/HMS/apps/inventory/views.py)
*   `inventory_list`: List all equipment with filter by status.
*   `amc_dashboard`: Dashboard showing upcoming expiries (Red Alert < 30 days).

### 4. Enhancement: Appointments App (`appointments`)
Improve consultation to support structured prescriptions (medicines) and PDF generation.

#### [MODIFY] [models.py](file:///apps/appointments/models.py)
*   **Enhance `Consultation` Model**:
    *   Add `clinical_notes` (if not present).
    *   Add `next_visit_date`.
*   **New Model `PrescriptionItem`**:
    *   `consultation` (ForeignKey)
    *   `medicine_name`
    *   `dosage` (e.g., 1-0-1)
    *   `duration` (e.g., 5 days)
    *   `instruction` (e.g., After food)

#### [NEW] [utils.py](file:///apps/appointments/utils.py)
*   `generate_prescription_pdf`: Logic to generate PDF using `reportlab`.
    *   Setup Canvas.
    *   Draw Header (Hospital Info).
    *   Draw Patient Info table.
    *   Draw Medicines table.
    *   Draw Footer (Doctor Signature).

### 5. Enhancement: Staff Dashboard UI
*   **Layout**: 2-Column Grid (Appointments Left, Attendance Right).
*   **Widget**: Sleek Design, Pill Buttons, Work Hours Counter.

## Verification Plan

### Automated Tests
*   **Attendance**: Test check-in/out logic constraints (cannot check out without checking in).
*   **Inventory**: Test AMC expiry filtering.
*   **Prescriptions**: Verify `reportlab` generates a valid PDF file with correct content.

### Manual Verification
*   **Staff**: Log in as staff -> Check In -> Check Out -> Verify log in Admin.
*   **Reviews**: Add a review in Admin -> Verify it appears on the public "Testimonials" section.
*   **Inventory**: Add equipment with AMC expiring tomorrow -> Check Dashboard alert.
*   **Prescription**: Complete a specific consultation -> Click "Print Prescription" -> Verify PDF download and layout.
