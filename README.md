# DateTime Timezone Converter

A modern, high-performance web application designed to convert date and time between any global timezones with a premium Material Design night-theme user interface.

## 🚀 Tech Stack

### Backend
- **Core**: Python 3.12+
- **Web Framework**: Flask (3.1.3)
- **Timezone Management**: `pytz` (2025.2) — Handles 600+ timezones and Daylight Saving Time (DST).
- **Architecture**: RESTful API with pre-cached timezone computation for O(1) initial load performance.

### Frontend
- **Structure**: Semantic HTML5
- **Styling**: Vanilla CSS3 with Glassmorphism and Material Design principles.
- **Interactions**: Vanilla JavaScript
- **Libraries**:
  - **Flatpickr**: Modern datetime picker with dark theme.
  - **Choices.js**: Lightweight, searchable select inputs for timezone selection.
  - **Google Fonts**: Orbitron (digital clock feel) and Inter (UI clarity).
  - **Material Icons**: Rounded icons for intuitive navigation.

## 🛠️ Requirements & Installation

### Prerequisites
- Python 3.12 or higher
- `pip` (Python package manager)

### Installation
1. Navigate to the project directory:
   ```bash
   cd /Project/datetime_convertor
   ```
2. Install dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```
 
## 🌐 Application Architecture

### Frontend-Backend Connectivity
The frontend communicates with the Flask backend via asynchronous JSON requests:
- **`GET /api/timezones`**: Fetches the pre-cached list of all timezones formatted as `City, Continent (UTC±HH:MM)`.
- **`POST /api/convert`**: Sends the source datetime, source timezone, and target timezone to the server; receives the converted results.

### Ports & Internal Wiring
- **Server Port**: `5000` (Default Flask development port)
- **Host**: `127.0.0.1` (localhost)
- **Endpoint Wiring**: The frontend uses standard `fetch` API calls relative to the root, ensuring portability across different deployment environments.

## 👨‍💻 DevOps & Deployment Info

### Environment Variables
While currently using default configurations, the app is prepared for standard Flask environment variable overrides:
- `FLASK_APP=app.py`
- `FLASK_ENV=development` or `production`

### Performance Optimization
The backend implements a **Pre-loading Timezone Cache** on startup. This computes UTC offsets for all 600+ zones once, preventing 30s+ response delays during per-request computation.

### Process Management

To stop the server:
```bash
fuser -k 5000/tcp
```

### Critical Paths
- **Templates Directory**: `/templates/index.html` (Must be present for route rendering)
- **API Logic**: Contained within `app.py` utilizing the `pytz` library for DST accuracy.

## 🎨 UI Design Features
- **Night Theme**: Deep navy gradients (`#080c14` to `#111927`).
- **Smooth Animations**: CSS transitions, ripple effects on buttons, and shimmer gradients on results.
- **Glassmorphism**: Translucent card layouts for a modern, layered appearance.
