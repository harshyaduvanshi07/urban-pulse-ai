-- Urban Pulse AI / SIH 2026
-- Run in Supabase SQL Editor.
-- This script intentionally contains NO secret API key.

-- Event types used by the prototype.
ALTER TABLE public.events
DROP CONSTRAINT IF EXISTS events_event_type_check;

ALTER TABLE public.events
ADD CONSTRAINT events_event_type_check
CHECK (
  event_type IN (
    'pothole',
    'damaged_road',
    'missing_divider',
    'missing_zebra_crossing',
    'damaged_signboard',
    'waterlogging',
    'vehicle_density',
    'traffic_bottleneck',
    'pedestrian_risk',
    'incident_rash_driving',
    'incident_hit_and_run'
  )
);

-- GIS-friendly view for the browser.
CREATE OR REPLACE VIEW public.events_with_coords AS
SELECT
  id,
  event_type,
  bus_id,
  occurred_at,
  confidence,
  thumbnail_url,
  metadata,
  created_at,
  ST_AsText(geom) AS geom_text
FROM public.events;

GRANT SELECT ON public.events_with_coords TO anon;

-- Ensure realtime is enabled for event inserts if your project
-- has not already enabled it through the Supabase dashboard.
-- ALTER PUBLICATION supabase_realtime ADD TABLE public.events;
