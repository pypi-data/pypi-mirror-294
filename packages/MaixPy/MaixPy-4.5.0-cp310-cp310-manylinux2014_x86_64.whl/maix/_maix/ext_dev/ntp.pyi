"""
maix.ext_dev.ntp module
"""
from __future__ import annotations
__all__ = ['sync_sys_time', 'sync_sys_time_with_config', 'time', 'time_with_config']
def sync_sys_time(host: str, port: int = -1, retry: int = 3, timeout_ms: int = 0) -> list[int]:
    """
    Retrieves time from an NTP server and synchronizes the system time
    This function fetches the current time from the specified NTP server and port,
    then synchronizes the system time with the retrieved time.
    
    Args:
      - host: The hostname or IP address of the NTP server.
      - port: The port number of the NTP server. Use 123 for the default port.
      - retry: The number of retry attempts. Must be at least 1.
      - timeout_ms: The timeout duration in milliseconds. Must be non-negative.
    
    
    Returns: A list of 6 elements: [year, month, day, hour, minute, second]
    """
def sync_sys_time_with_config(path: str) -> list[int]:
    """
    Retrieves time from an NTP server using a configuration file and synchronizes the system time
    This function reads the configuration from a YAML file to fetch the current time
    from a list of specified NTP servers, then synchronizes the system time with the retrieved time.
    
    Args:
      - path: The path to the YAML configuration file, which should include:
    - Config:
    - retry: Number of retry attempts (must be at least 1)
    - total_timeout_ms: Total timeout duration in milliseconds (must be non-negative)
    - NtpServers:
    - host: Hostname or IP address of the NTP server
    - port: Port number of the NTP server (use 123 for default)
    Example YAML configuration:
    Config:
    - retry: 3
    - total_timeout_ms: 10000
    NtpServers:
    - host: "pool.ntp.org"
    port: 123
    - host: "time.nist.gov"
    port: 123
    - host: "time.windows.com"
    port: 123
    
    
    Returns: A vector of integers containing the time details: [year, month, day, hour, minute, second]
    """
def time(host: str, port: int = -1, retry: int = 3, timeout_ms: int = 0) -> list[int]:
    """
    Retrieves time from an NTP server
    This function fetches the current time from the specified NTP server and port,
    returning a tuple containing the time details.
    
    Args:
      - host: The hostname or IP address of the NTP server.
      - port: The port number of the NTP server. Use -1 for the default port 123.
      - retry: The number of retry attempts. Must be at least 1.
      - timeout_ms: The timeout duration in milliseconds. Must be non-negative.
    
    
    Returns: A list of 6 elements: [year, month, day, hour, minute, second]
    """
def time_with_config(path: str) -> list[int]:
    """
    Retrieves time from an NTP server using a configuration file
    This function reads the configuration from a YAML file to fetch the current time
    from a list of specified NTP servers, returning a tuple containing the time details.
    
    Args:
      - path: The path to the YAML configuration file, which should include:
    - Config:
    - retry: Number of retry attempts (must be at least 1)
    - total_timeout_ms: Total timeout duration in milliseconds (must be non-negative)
    - NtpServers:
    - host: Hostname or IP address of the NTP server
    - port: Port number of the NTP server (use 123 for default)
    Example YAML configuration:
    Config:
    - retry: 3
    - total_timeout_ms: 10000
    NtpServers:
    - host: "pool.ntp.org"
    port: 123
    - host: "time.nist.gov"
    port: 123
    - host: "time.windows.com"
    port: 123
    
    
    Returns: A list of 6 elements: [year, month, day, hour, minute, second]
    """
