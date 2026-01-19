import json
from google.cloud import pubsub_v1
from app.config import settings

_publisher = None

def _get_publisher():
    global _publisher
    if _publisher is None:
        _publisher = pubsub_v1.PublisherClient()
    return _publisher

def publish_event(event: dict):
    if not settings.events_topic or not settings.gcp_project:
        return  # no-op in MVP

    topic_path = _get_publisher().topic_path(settings.gcp_project, settings.events_topic)
    data = json.dumps(event).encode("utf-8")
    _get_publisher().publish(topic_path, data)
