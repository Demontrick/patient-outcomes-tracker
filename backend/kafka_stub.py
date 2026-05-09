import json
import logging

logger = logging.getLogger(__name__)

def publish_outcome_event(patient_id: int, score: float):
    """
    Mock Kafka event publisher.
    In a real scenario, this would use a KafkaProducer to send a message
    to the 'outcome.submitted' topic.
    """
    event = {
        "topic": "outcome.submitted",
        "payload": {
            "patient_id": patient_id,
            "score": score,
            "timestamp": str(logging.root.manager.datetime.utcnow() if hasattr(logging.root.manager, 'datetime') else "now")
        }
    }
    # Simulation: Log the event
    logger.info(f"MOCK KAFKA EVENT: {json.dumps(event)}")
    print(f"Published to Kafka topic 'outcome.submitted': {event}")

# Note: To use real Kafka, you would:
# 1. Install kafka-python
# 2. producer = KafkaProducer(bootstrap_servers='localhost:9092')
# 3. producer.send('outcome.submitted', json.dumps(payload).encode('utf-8'))
