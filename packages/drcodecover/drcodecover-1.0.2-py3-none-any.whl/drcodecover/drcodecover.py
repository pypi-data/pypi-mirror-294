import sentry_sdk
from sentry_sdk.integrations.threading import ThreadingIntegration
from typing import Dict, Any

def construct_dsn(config: Dict[str, Any]) -> str:
    """
    Constructs the DSN URL for Sentry from the provided configuration.

    Args:
        config (Dict[str, Any]): Configuration dictionary containing DSN components.

    Returns:
        str: The constructed DSN URL.
    """
    return f"https://{config['public_key']}@pulse.drcode.ai:443/{config['project_id']}"

def init_drcode(config: Dict[str, Any]) -> None:
    """
    Initializes Sentry with the provided configuration.

    Args:
        config (Dict[str, Any]): Configuration dictionary containing DSN components and sampling rates.

    Raises:
        ValueError: If required keys are missing in the configuration.
    """
    required_keys = [ 'public_key','project_id']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required config key: {key}")

    dsn = construct_dsn(config)
    
    sentry_sdk.init(
        dsn=dsn,
        integrations=[ThreadingIntegration(propagate_hub=True)],
        traces_sample_rate=config.get('traces_sample_rate', 1.0),
        profiles_sample_rate=config.get('profiles_sample_rate', 1.0),
    )
