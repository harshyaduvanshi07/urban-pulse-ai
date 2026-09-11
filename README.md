# Urban Pulse AI

AI-powered mobile urban sensing platform using public transport buses as mobile sensing units.

## Problem Statement

Prototype for SIH 2026 PS26124: transform public transport buses into intelligent mobile sensing units that detect road defects, traffic conditions, pedestrian risks and incidents, then aggregate structured events on a centralized GIS dashboard.

## Current Prototype

The prototype uses cloud infrastructure to simulate onboard edge inference:

```text
Recorded road video
        ↓
YOLO object detection
        ↓
BoT-SORT tracking
        ↓
Vehicle count / traffic density
        ↓
Synthetic GPS + timestamp
        ↓
Supabase events
        ↓
Live GIS dashboard
```

Production architecture can export the same models to ONNX/TensorRT and deploy them on a Jetson-class edge computer on each bus.

## Repository Structure

```text
urban-pulse-ai/
├── dashboard/
│   └── live_dash.html
├── ai/
│   └── traffic_detection.py
├── simulator/
│   └── fleet_simulator.py
├── sql/
│   └── supabase_setup.sql
├── docs/
│   └── architecture.md
├── requirements.txt
└── .gitignore
```

## 1. Supabase Setup

Create the required tables/view and event constraint using:

`sql/supabase_setup.sql`

The browser dashboard must use a **Publishable/anon key only**. Never commit a Secret/service-role key.

## 2. Dashboard

Open `dashboard/live_dash.html` from a local web server.

Example:

```bash
cd dashboard
python -m http.server 8000
```

Then open:

`http://localhost:8000/live_dash.html`

Before running, replace:

```js
const SUPABASE_KEY = "PASTE_YOUR_PUBLISHABLE_KEY_HERE";
```

with your Supabase Publishable key.

## 3. AI Environment

```bash
pip install -r requirements.txt
```

The AI script expects a road video and uses YOLO26 + BoT-SORT for object detection/tracking.

## 4. Security

- Publishable/anon key: browser-safe when RLS/policies are configured correctly.
- Secret key: backend/Colab only.
- Do not commit `.env`, tokens, service-role keys, or secret API keys.
- If a secret is accidentally exposed, rotate it.

## 5. Prototype Scope

Implemented:
- Fleet simulation
- GPS-tagged events
- Road/traffic event schema
- GIS map
- Event feed
- Traffic heatmap
- Realtime Supabase updates
- YOLO vehicle detection
- BoT-SORT tracking
- Vehicle counting / traffic density

Future production modules:
- Pothole/road-defect custom model
- ANPR
- Pedestrian-risk classification
- Rash-driving and hit-and-run reasoning
- Route delay and OD analytics
- Edge deployment with ONNX/TensorRT
