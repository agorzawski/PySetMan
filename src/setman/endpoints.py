"""
Collection of endpoints for setman service
"""

# /realms
EP_REALMS = "/realms"

# /parameters
EP_PARAMETERS = "/parameters"

# /contexts
EP_CONTEXTS = "/contexts"
EP_RESIDENCY = "/contexts/resident"
EP_RESIDENCY_HISTORY = "/contexts/resident/history"

# /rules
EP_RULES = "/rules"

# /settings
EP_SETTINGS = "/settings/context"
EP_RESIDENT_SETTINGS = "/settings/resident"

# /trims
EP_TRIM = "/trims"
EP_RESIDENT_TRIM = "/trims/resident"
EP_TRIM_HISTORY = "/trims/history"
EP_TRIM_HISTORY_ONE = EP_TRIM_HISTORY + "/{}"

# /devices
EP_DEVICES = "/devices"
EP_DRIVE_ALL = "/devices/drive"