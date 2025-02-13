import structlog
from datetime import datetime
import pytz

# Configure timezone (you can change this to your preferred timezone)
timezone = pytz.timezone('Asia/Shanghai')

def add_timezone(_, __, event_dict):
    """Add timezone information to the timestamp"""
    if 'timestamp' in event_dict:
        # Convert the timestamp string back to datetime
        dt = datetime.strptime(event_dict['timestamp'], '%Y-%m-%d %H:%M:%S')
        # Localize the datetime to the configured timezone
        dt = timezone.localize(dt)
        # Update the timestamp with timezone info
        event_dict['timestamp'] = dt.strftime('%Y-%m-%d %H:%M:%S %z')
    return event_dict

structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
        add_timezone,  # Add our custom timezone processor
        structlog.processors.dict_tracebacks,
        structlog.processors.JSONRenderer(indent=2)  # Added indent for better readability
    ],
)

logger = structlog.get_logger()