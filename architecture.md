# Architecture

## Prototype

The prototype is cloud-hosted because physical bus hardware is not available during development.

### Edge simulation
- Recorded dashcam/road video
- YOLO26 object detection
- BoT-SORT object tracking
- Vehicle count and traffic density
- Synthetic GPS and timestamps

### Central platform
- Supabase PostgreSQL/PostGIS event store
- Realtime event delivery
- Leaflet GIS dashboard
- Traffic heatmap
- Fleet aggregation and alerts

## Production

```text
Bus cameras
    ↓
Jetson-class edge computer
    ↓
ONNX/TensorRT optimized AI
    ↓
Structured event JSON + selected evidence
    ↓
Secure API
    ↓
Central PostgreSQL/PostGIS
    ↓
GIS dashboard + analytics + alerts
```

Raw video should remain local to the bus where practical. Only event metadata, GPS/time, confidence, and selected evidence should be uploaded to reduce bandwidth.
