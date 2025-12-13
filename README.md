# Reading Room QR/Bar Code Check-in System

A Production-grade web system to manage reading room occupancy, authentication, check-in/check-out, and automatic seat allotment. Built to solve a real institutional problem. Designed for efficiency, not demos.

## Live Demo
🔗 https://readingroom-ppbn.onrender.com/



## Problem

The reading room had:
- No real-time occupancy tracking(walking long distances just to see if the reading room is empty or not)
- Manual and inefficient check-in/check-out
- No way to prevent misuse of seats (laptop vs non-laptop)
- No record of who used the room and when

The system needed to be:
- Secure
- Efficient usage of seats
- Admin-controlled
- Scalable for real-world usage


## Features

### Authentication & Roles
- Secure authentication system
- Role-based access (Admin / User)
- Admin-only check-in and check-out to prevent misuse

### Check-In / Check-Out (3 Methods)
- University ID card barcode
- Unique QR code assigned to each user
- Manual registration number entry

### Real-Time Reading Room Status
- View whether the reading room is occupied or empty
- Live tracking of active sessions

### Automatic Seat (Box) Allotment
- Two seat types: Normal & Laptop (with plug points)
- Users specify laptop status in profile
- System assigns seats automatically using priority logic:
  - First preference: matching seat type
  - Second preference: fallback if preferred seats are unavailable
- Maximizes resource efficiency and prevents misuse

### Entry Records & Analytics
- Complete log of:
  - Session ID
  - Student details
  - Check-in time
  - Check-out time
  - Box number, which the student occupied
- Date-wise pagination for organized review

### Security & Production Practices
- Environment variables used for sensitive data
- No credentials exposed in repository
- Flash messaging for user feedback

## Tech Stack

- Backend: Flask (Python)
- Database: Supabase (PostgreSQL)
- Frontend: HTML, CSS, Bootstrap, JS
- Authentication: Session-based auth on users' devices
- Deployment: Render

## System Design Highlights

- Authentication implemented first to ensure security from day one
- Admin-mediated check-in/check-out to avoid misuse
- Algorithmic seat allotment with priority handling
- Date-based pagination for better scalability and readability

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
5. Logs out securely after session completion.

#### Administrator Flow
1. Authenticates using administrator credentials.
2. Accesses the administrative dashboard.
3. Views and manages registered student records.
4. Verifies student identities using QR/Bar code references and checkins/outs them.
5. Oversees system-level operations and data consistency.


## Development Timeline

- Total development time: ~15 hours
- Built solo
- Planned, implemented, and deployed the first version within 2 days
- Version 2 added automatic seat allotment and optimization logic

## Future Scope

- Admin-configurable seat rules
- Multi-room support
- More user-friendly UI(focus especially on making it more responsive)
- More Dashboard

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

