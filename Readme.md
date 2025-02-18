# Railway Management System API

This is a Django-based API for a railway management system with the following features:
- User registration and login (using Token Authentication).
- Admin-protected endpoint to add a new train (requires header `X-API-KEY`).
- Endpoint to check seat availability between a source and destination.
- Endpoint to book a seat on a train (with transaction locking to avoid race conditions).
- Endpoint to get booking details.

## Tech Stack
- **Backend:** Django, Django REST Framework
- **Database:** SQLite
- **Authentication:** DRF Token Authentication

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd railway_project
