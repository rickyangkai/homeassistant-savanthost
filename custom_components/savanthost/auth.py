import hashlib
import uuid
import logging

_LOGGER = logging.getLogger(__name__)

def get_device_id() -> str:
    """Get device ID based on MAC address (similar to Node.js os.networkInterfaces logic)."""
    try:
        # getnode() returns the MAC address as a 48-bit integer
        mac_int = uuid.getnode()
        # Convert to hex string and format
        mac_hex = "{:012X}".format(mac_int)
        return mac_hex
    except Exception as e:
        _LOGGER.error(f"Failed to get device ID: {e}")
        # Fallback to a hash of hostname if MAC fails (though getnode usually works)
        import socket
        hostname = socket.gethostname()
        return hashlib.md5(hostname.encode()).hexdigest().upper()[:16]

def generate_address_code(device_id: str) -> str:
    """Generate address code (machine code) from device ID."""
    # Logic from auth.ts: sha256(deviceId + 'SavantHost').digest('hex').substring(0, 16).toUpperCase()
    data = f"{device_id}SavantHost"
    hash_obj = hashlib.sha256(data.encode())
    return hash_obj.hexdigest()[:16].upper()

def validate_auth_code(address_code: str, auth_code: str) -> bool:
    """Validate the authorization code."""
    # Logic from auth.ts:
    # expected = sha256(addressCode.reversed() + 'SavantHostAuth').digest('hex').substring(0, 16).toUpperCase()
    
    if not auth_code:
        return False
        
    reversed_address = address_code[::-1]
    data = f"{reversed_address}SavantHostAuth"
    hash_obj = hashlib.sha256(data.encode())
    expected_code = hash_obj.hexdigest()[:16].upper()
    
    # Clean input code (remove spaces, upper case)
    clean_auth_code = auth_code.strip().upper()
    
    is_valid = clean_auth_code == expected_code
    
    if not is_valid:
        _LOGGER.debug(f"Auth failed. Address: {address_code}, Expected: {expected_code}, Got: {clean_auth_code}")
        
    return is_valid
