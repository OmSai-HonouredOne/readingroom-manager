# Reading Room QR/Bar Code Check-in System

A production-grade web system for managing reading room occupancy, authentication, check-in/check-out, and automatic seat allotment.

## Live Demo
🔗 https://readingroom-ppbn.onrender.com/

## Real-World System Walkthrough
A live demo showcasing real usage across multiple devices, including authentication, seat allocation, and admin workflows.

🔗 https://youtu.be/6nVfKZjPE2o?si=3VF_U95fCDKJiSFq

---

## Problem

The reading room faced multiple operational challenges:
- No real-time seat availability
- Manual and inefficient check-in/check-out
- Seat misuse (laptop vs non-laptop)
- No spatial visibility of occupancy

The system needed to be **secure**, **efficient**, **admin-controlled**, and **scalable**.

---

## Features

### Authentication & Roles
- Secure session-based authentication
- Role-based access (Admin / Student)
- Admin-controlled check-in/check-out to prevent misuse

### Check-In / Check-Out (3 Methods)
- University ID barcode
- User-specific QR code
- Manual registration number entry (fallback)

### Real-Time Occupancy
- Live reading room status
- Active session monitoring for administrators

### Automatic Seat Allotment (Version 2)
- Two seat types: Normal & Laptop
- User-defined laptop preference
- Priority-based assignment:
  - Matching seat type
  - Intelligent fallback if unavailable

### Graphical Seat Layout (Version 3)
- Full reading room rendered using CSS Grid
- Irregular U-shaped layout with transparent walkways
- Color-coded seat states:
  - 🟩 Available
  - 🟥 Occupied
  - 🟦 Assigned (current user)
- Clickable seats with contextual actions
- Admin controls for occupied seats

### In-Memory Vectorized Layout Engine (Version 4)
- Migrated seat state handling from DB to in-memory NumPy arrays
- Multi-dimensional layout with structured seat metadata
- Vectorized operations for state updates
- Layout initialized from DB with fallback recovery
- Much reduction in runtime SQL queries
- Near-instant rendering on Render free tier
- Designed for single-worker stability and future horizontal scaling

#### 🧠 Architecture Philosophy
This system is designed around **data shape and access patterns**, not tool categories.

The reading room is a spatial state problem:
- fixed-size grids
- frequent reads
- localized writes
- deterministic transitions

An in-memory, vectorized model minimizes IO latency, eliminates redundant queries, and treats the layout as a single coherent state object.  
Tools are chosen based on **problem fit**, not convention.

### Seat availability Reminder(Version 5)
- If all seats are occupied, users can set an email reminder for availability.
- When a seat is freed within 20 minutes of checkout, the user is automatically notified via email.
- Implemented using time comparison at checkout with minimal database changes and no background schedulers.

---

### Records & Analytics
- Complete session logs:
  - Student details
  - Check-in / check-out timestamps
  - Assigned seat (box number)
- Date-wise pagination for scalability

### Security & Production Practices
- Environment variables for sensitive data
- No credentials committed
- Flash messaging for user feedback


## Tech Stack

- Backend: Flask & Numpy (Python)
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

### Total Development Time

- Version 1: ~13 hours
- Version 2: ~2 hours
- Version 3: ~4 hours
- Version 4: ~3.5 hours
- Version 5: ~1.5 hours
- Total: ~24 hours
Planned, implemented, tested, and deployed solo.

## Installation and Usage

### Installation

```bash
git clone "https://github.com/OmSai-HonouredOne/readingroom-manager.git"
cd readingroom-manager
pip install -r requirements.txt
```

Create a ```.env``` file in the repo folder and fill the environment variables:
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
- Multi-room support
- Multi worker supporting architecture
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