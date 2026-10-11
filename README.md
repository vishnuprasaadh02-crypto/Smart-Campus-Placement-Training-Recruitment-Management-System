# Placify: Smart Campus Placement Management System

A comprehensive, full-stack college placement management portal designed with a luxurious Royal Blue & Gold theme.

## Features
- **Role-based Access**: Admin and Student dashboards.
- **Company Management**: Track recruiting organizations, their profiles, and contact points.
- **Job Drives**: Post placement drives with specific eligibility criteria (CGPA, 10th/12th marks, departments).
- **Application Tracking**: End-to-end status tracking from 'Applied' to 'Selected' or 'Rejected'.
- **Interviews**: Schedule interviews, technical assessments, and HR rounds.
- **Placement Records**: Showcase successful placements and salary packages.
- **Reporting**: Advanced analytics, charts, and downloadable CSV reports.
- **Premium UI**: Glassmorphism elements, fully responsive layout, Dark/Light mode toggle, and an animated SVG wave background.

## Technology Stack
- **Backend**: Python 3, Flask, SQLAlchemy (ORM)
- **Database**: MySQL (Primary), SQLite (Fallback for quick setup)
- **Frontend**: HTML5, Vanilla CSS3 (Custom Design System), Bootstrap 5 (Grid/Components), Chart.js
- **Security**: Werkzeug password hashing, Flask-Login session management

## Quick Setup
1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   pip install -r requirements.txt
   ```
2. Initialize the Database:
   ```bash
   python database/init_db.py
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Access at `http://localhost:5000`
   - Default Admin: `admin` / `Admin@123`
