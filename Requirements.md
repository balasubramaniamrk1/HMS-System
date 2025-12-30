# Hospital Management System (HMS) - Requirements Document

## 1. Project Overview
The Hospital Management System (HMS) is a web-based application designed to streamline hospital operations, improve patient engagement, and manage clinical workflows efficiently. The system facilitates doctor appointment bookings, content management for health blogs, and career applications.

## 2. Functional Requirements

### 2.1 Core Module
*   **Health Packages**: 
    *   Display various health check-up packages (e.g., "Full Body Checkup").
    *   Show pricing, discounted prices, and detailed lists of inclusions.
    *   Support for image uploads for package visualization.
*   **Contact Management**: 
    *   Allow users to submit contact queries (Name, Email, Phone, Subject, Message).
*   **Career Portal**: 
    *   Allow candidates to apply for positions.
    *   Collect applicant details (Name, Contact Info, Position) and resume uploads.

### 2.2 Doctor & Department Management
*   **Department Management**: 
    *   Categorize doctors into departments (e.g., Cardiology, Neurology).
    *   Manage department descriptions and icons.
*   **Doctor Directory**: 
    *   Display doctor profiles with photos, qualifications, specializations, and experience.
    *   "Featured" status for highlighting specific doctors on the home page.
    *   Search/Filter by department.

### 2.3 Appointment System
*   **Booking**: 
    *   Patients can request appointments by selecting a doctor/department and preferred date/time.
    *   Capture patient contact details (Name, Phone, Email) and reason for visit.
*   **Status Tracking**: 
    *   Track appointment status: *Pending*, *Confirmed*, *Completed*, *Cancelled*.
*   **Consultations (Clinical)**: 
    *   Link consultations to confirmed appointments.
    *   Record clinical data: *Doctor Notes*, *Diagnosis*, *Prescription*.

### 2.4 Blog & Content
*   **Health Blog**: 
    *   Publish health-related articles with titles, images, and content.
    *   Support for draft/published status.

### 2.5 User Access & Administration
*   **Authentication**: 
    *   Standard login/logout functionality for staff and admins.
    *   Custom admin access route (`/admin-access/`).
*   **Administration**: 
    *   Backend admin panel (using Django Jazzmin) to manage all data entities.

## 3. Technical Requirements
*   **Backend**: Python / Django (5.2.x).
*   **Database**: PostgreSQL.
*   **Storage**: Local filesystem for media (Images, Resumes).
*   **Frontend**: Responsive web interface using Django Templates and Custom CSS.
*   **Deployment**: Dockerized environment with Gunicorn and Nginx.

## 4. Future / Pending Features (Inferred from Empty Directories)
*   **Wellness**: Potential module for wellness programs (currently empty).
*   **Services**: Potential module for general hospital services listing (currently empty).
