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

def get_combined_blocks(full_data, cmd_name, channel_id_str):
    """
    Merges specific command blocks with global '*' command blocks.
    Precedence: Specific Command Blocks > Global '*' Blocks.
    """
    if not isinstance(full_data, dict):
        return []

    # 1. Extract Specific Command config
    specific_cfg = full_data.get(cmd_name, {})

    # 2. Extract Global Defaults if they exist
    global_cfg = full_data.get("*", {})

    def get_blocks(cfg):
        if not isinstance(cfg, dict): return []
        # Return lists from Channel ID, '*', and 'all'
        return cfg.get(channel_id_str, []) + cfg.get("*", []) + cfg.get("all", [])

    # Order is critical: Specific blocks appear FIRST in the list.
    # The loop in bot.py breaks at the first match, ensuring specific overrides global.
    return get_blocks(specific_cfg) + get_blocks(global_cfg)
