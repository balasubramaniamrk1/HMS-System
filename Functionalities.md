# Comprehensive Feature List (HMS Development) 
*Last Updated: 2025-12-24*

This document outlines the complete list of functionalities implemented from the start of development for the HealthPlus Management System (HMS).

## 1. Core Platform Features (`apps.core`)
The foundation of the web application.
- **Home Page**: Modern landing page with prominent call-to-actions.
- **Role-Based Redirects**: Smart logic to redirect users to their specific dashboards upon login (e.g., Inventory Managers -> Inventory Dashboard, Doctors -> Doctor Console).
- **Static Content**: About Us, Contact, Careers, International Patients, Insurance & TPA information pages.
- **Service Listings**: Display of available Health Packages.

## 2. Doctor & Department Management (`apps.doctors`)
- **Doctor Directory**: Public-facing list of all doctors with search/filter capabilities.
- **Doctor Profiles**: Detailed view for each doctor profile.
- **Speciality Directory**: Listing of all medical departments/specialities.
- **Speciality Details**: Detailed view for each department.

## 3. Inventory Management (`apps.inventory`)
A comprehensive module for tracking hospital assets, contracts, and supplies.
- **Access Control**: Secured specifically for users in the "Inventory Managers" group.
- **Dashboard**:
    - Real-time overview of Total Assets, Assets Under Repair, and expiring contracts.
    - Low Stock Alerts for consumables.
    - AMC Expiry warnings (Color-coded: Yellow for expiring soon, Red for expired).
- **Equipment Management**:
    - **Asset List**: Searchable table of all hospital equipment with status badges.
    - **Add/Edit Equipment**: Forms to manage asset details (Serial #, Model, Purchase Date, Warranty).
    - **QR Code Generation**: Auto-generates QR codes for each asset for easy tracking.
    - **Depreciation Calculation**: Automated calculation of current asset value based on useful life.
    - **View QR**: Dedicated page to view/print asset QR codes.
- **Maintenance Contracts (AMC)**:
    - **AMC List**: Tracker for all active and expired maintenance contracts.
    - **Add/Edit Contract**: Form to link equipment to vendors with contract dates.
    - **Validation**: Smart checks to ensure equipment/vendors exist before adding a contract.
- **Vendor Management**:
    - **Vendor List**: Directory of all suppliers and service providers.
    - **Add/Edit Vendor**: Manage contact details and ratings for vendors.
- **Consumables Management**:
    - **Stock Tracking**: Track quantity, unit cost, and restock levels for supplies.
    - **Add/Edit Consumable**: Manage inventory of items like gloves, syringes, etc.
- **Maintenance Logs**:
    - **Log History**: Track repair and service history for individual equipment.
    - **Add Log**: Record new maintenance activities and costs.

## 4. Appointment & Clinical Management (`apps.appointments`)
- **Appointment Booking**: Public form for patients to book consultations.
- **Staff Dashboard**:
    - Complete list of today's appointments.
    - Status management (Mark as Checked-In, Completed, Cancelled).
    - Ability to reschedule appointments.
- **Doctor Console**:
    - **My Appointments**: Personalized view for logged-in doctors to see their schedule.
    - **Consultation Mode**: Digital interface to conduct patient exams.
    - **Prescription Generation**:
        - Digital prescription writing.
        - Auto-generated PDF prescriptions for patients.
    - **History**: View past consultation history.
- **Reports Dashboard**:
    - Administrative view of all consultations.
    - Filterable by Doctor (RBAC enforced: Doctors see only their own reports).

## 5. Staff Management (`apps.staff_mgmt`)
- **Staff Portal**: Dedicated dashboard for hospital staff.
- **Attendance System**:
    - **Check-In/Check-Out**: Simple digital clock-in system for daily attendance.
    - **Status Indicators**: Visual feedback on current attendance status.

## 6. Reputation Management (`apps.reputation`)
- **Public Reviews**: System to display patient testimonials and feedback.

## 7. Security & Infrastructure
- **Role-Based Access Control (RBAC)**: Strict permission enforcement using Custom Decorators (`@group_required`).
    - *Inventory Managers*: Full access to Inventory module.
    - *Doctors*: Access to Clinical Console and own reports.
    - *Staff*: Access to Attendance and Reception dashboards.
- **Authentication**: Secure Login/Logout workflow.
- **Django Admin**: Custom-themed administrative backend for superusers.
