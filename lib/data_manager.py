import os
import json
from lib.logger import log_warn, log_error

def load_data(file_path):
    """Reads the JSON commands file and optionally warns if duplicate keys are detected."""
    if not os.path.exists(file_path):
        log_warn(f"Configuration file NOT FOUND at {file_path}")
        return {}

    # Check environment variable to see if detection is enabled (Default: True)
    detect_enabled = os.getenv('DETECT_DUPLICATES', 'True').lower() == 'true'

    def detect_duplicates(pairs):
        """
        Hook to detect duplicate keys during JSON parsing recursively.
        Only prints warnings if DETECT_DUPLICATES is enabled.
        Uses the logging library to maintain a consistent paper-trail.
        """
        result = {}
        for key, value in pairs:
            if key in result and detect_enabled:
                log_warn(f"Duplicate key '{key}' detected in {file_path}! Overwriting previous value.")
            result[key] = value
        return result

    with open(file_path, 'r') as f:
        try:
            # Apply duplicate detection hook if enabled
            if detect_enabled:
                return json.load(f, object_pairs_hook=detect_duplicates)
            else:
                return json.load(f)
        except json.JSONDecodeError as e:
            log_error(f"ERROR: {file_path} contains invalid JSON syntax: {e}")
            return {}

def get_combined_blocks(data, channel_id_str):
    """Combines channel-specific blocks with global wildcard blocks."""
    # Ensure data is a dictionary before calling .get to prevent crashes on malformed groups
    if not isinstance(data, dict):
        return []

    specific = data.get(channel_id_str, [])
    global_star = data.get("*", [])
    global_all = data.get("all", [])

    return specific + global_star + global_all
