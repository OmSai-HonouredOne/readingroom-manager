# Reading Room QR/Bar Code Check-in System

A Production-grade web system to manage reading room occupancy, authentication, check-in/check-out, and automatic seat allotment. Built to solve a real institutional problem. Designed for efficiency, not demos.

## Live Demo
🔗 https://readingroom-ppbn.onrender.com/

## Reading Room – Real-World System Demo/Walkthrough
This video demonstrates the Reading Room system in real use, including user interaction, authentication, and administrative workflows that require multiple devices and therefore cannot be fully shown through screenshots alone.

The focus of this video is not UI polish, but system behavior, logic flow, and how different components interact in practice.

🔗 https://youtu.be/6nVfKZjPE2o?si=3VF_U95fCDKJiSFq

## Problem

The reading room faced multiple operational issues:
- No real-time occupancy tracking(students walked long distances just to check availability)
- Manual and inefficient check-in/check-out
- No way to prevent misuse of seats (laptop vs non-laptop)
- No spatial visibility of available seats

The system needed to be:
- Secure
- Efficient usage of seats
- Admin-controlled
- Scalable for real-world usage

## Features

### Authentication & Roles
- Secure authentication system
- Role-based access (Admin / Student)
- Admin-only check-in and check-out to prevent misuse

### Check-In / Check-Out (3 Methods)
- University ID card barcode
- Unique QR code assigned to each user
- Manual registration number entry (fallback)

### Real-Time Reading Room Status
- Live occupancy tracking
- View whether the reading room is occupied or empty
- Live tracking of active sessions for administrators

### Automatic Seat (Box) Allotment (Version 2)
- Two seat types: Normal & Laptop (with plug points)
- Users specify laptop status in profile
- System assigns seats automatically using priority logic:
  - First preference: matching seat type
  - Second preference: fallback if preferred seats are unavailable
- Maximizes resource efficiency and prevents misuse

### Graphical Reading Room Layout & Seat Selection (Version 3)

- Full reading room visualized using CSS Grid
- Irregular U-shaped layout modeled using transparent pathway cells
- Color-coded seat states:
  - 🟩 Green — Available
  - 🟥 Red — Occupied
  - 🟦 Blue — Assigned to current user
  - ⬜ Transparent — Walkways
- Clickable seats with contextual popups
- Students can visually inspect availability and select preferred seats
- Admin view allows interaction with occupied seats (e.g., forced checkout)

### Entry Records & Analytics
- Complete log of:
  - Session ID
  - Student details
  - Check-in and check-out timestamps
  - Box number, which the student occupied
- Date-wise pagination for organized review and scalability

### Security & Production Practices
- Environment variables used for sensitive data
- No credentials exposed in repository
- Flash messaging for user feedback

## Tech Stack

- Backend: Flask (Python)
- Database: Supabase (PostgreSQL)
- Frontend: HTML, CSS, Bootstrap, JavaScript
- Authentication: Session-based(server-side)
- Deployment: Render

## System Design Highlights

- Authentication implemented first to ensure security from day one
- Admin-mediated check-in/check-out to avoid misuse
- Algorithmic seat allotment with priority handling
- Visual layout layered on top of backend constraints
- Date-based pagination for better scalability and readability

## Development Timeline & Iteration

This project was developed iteratively, with each version solving newly observed constraints.

### Version 1 — Core System (~13 hours)

- Authentication and role-based access
- QR / barcode check-in and check-out
- Manual fallback handling
- Admin dashboard
- Persistent session logging
Focus: Correctness, security, and real-world usability

### Version 2 — Automatic Seat Allotment (+2 hours)

- Laptop vs non-laptop seat classification
- Priority-based seat assignment algorithm
- Misuse prevention and optimization logic
Focus: System efficiency and resource optimization

### Version 3 — Visual Layout & User Choice (+4 hours)

- CSS Grid-based reading room layout
- Irregular shaped layout made using transparent pathway cells
- Seat-level interaction with popups
- User-driven seat preference selection
- Admin-side interaction with occupied seats
Focus: Human-computer interaction and spatial reasoning

### Total Development Time

- Version 1: ~13 hours
- Version 2: ~2 hours
- Version 3: ~4 hours
- Total: ~19 hours
Planned, implemented, tested, and deployed solo.

## Installation and Usage

### Installation

```bash
git clone "https://github.com/OmSai-HonouredOne/readingroom-manager.git"
cd readingroom-manager
pip install -r requirements.txt
```

Create a ```.env``` file in the repo folder and fill make environment variables:
```bash
FLASK_APP=rrbook
SECRET_KEY="SUPERSECRETKEY"
DATABASE_URL="your-database-url"
```

Finally run the app by:
```bash
flask --app rrm run --debug
```

### Usage
The system supports two primary user roles **Student** and **Administrator**.

#### Student Flow
1. Registers using academic details (name, registration number, branch, year).
2. Authenticates using registered credentials.
3. Accesses a personal profile dashboard containing structured student data.
4. Receives a unique, system-generated QR code for identity verification.
5. Select seat preferences visually(Version 3)
6. Logs out securely after session completion.

#### Administrator Flow
1. Authenticate as admin
2. Monitor live occupancy
3. Check students in/out via QR, barcode, or manual entry
4. View and manage seat allocation
5. Access historical usage records

## Future Scope

- Admin-configurable seat rules
- Multi-room support
- Improved mobile responsiveness
- Advanced analytics dashboards

## Contributing
Contributions are welcome!
Fork the repo, create a new branch, and submit a PR

## License
This project is licensed under the MIT License.
See the [LICENSE](LICENSE) for more details

## About the Author
Om Sai,
Engineering Student passionate about building scalable, user-centric web applications and unique engineering projects.

Github: https://github.com/OmSai-HonouredOne

