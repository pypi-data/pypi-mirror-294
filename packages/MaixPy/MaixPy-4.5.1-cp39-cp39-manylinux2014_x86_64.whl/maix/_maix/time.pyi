"""
maix.time module
"""
from __future__ import annotations
from maix.__maix_time__ import sleep_ms
from maix.__maix_time__ import sleep_us
from time import sleep
__all__ = ['DateTime', 'FPS', 'fps', 'fps_set_buff_len', 'fps_start', 'gmtime', 'list_timezones', 'localtime', 'now', 'sleep', 'sleep_ms', 'sleep_us', 'strptime', 'ticks_diff', 'ticks_ms', 'ticks_s', 'ticks_us', 'time', 'time_diff', 'time_ms', 'time_s', 'time_us', 'timezone']
class DateTime:
    day: int
    hour: int
    microsecond: int
    minute: int
    month: int
    second: int
    weekday: int
    year: int
    yearday: int
    zone: float
    zone_name: str
    def __init__(self, year: int = 0, month: int = 0, day: int = 0, hour: int = 0, minute: int = 0, second: int = 0, microsecond: int = 0, yearday: int = 0, weekday: int = 0, zone: int = 0) -> None:
        ...
    def strftime(self, format: str) -> str:
        """
        Convert to string
        
        Returns: date time string
        """
    def timestamp(self) -> float:
        """
        Convert to float timestamp
        
        Returns: float timestamp
        """
class FPS:
    def __init__(self, buff_len: int = 20) -> None:
        ...
    def fps(self) -> float:
        """
        The same as end function.
        
        Returns: float type, current fps since last call this method
        """
    def set_buff_len(self, len: int) -> None:
        """
        Set fps method buffer length, by default the buffer length is 10.
        
        Args:
          - len: Buffer length to store recent fps value.
        """
    def start(self) -> None:
        """
        Manually set fps calculation start point, then you can call fps() function to calculate fps between start() and fps().
        """
def fps() -> float:
    """
    Calculate FPS since last call this method.
    Attention, this method is not multi thread safe, only call this method in one threads.
    If you want to use in multi threads, please use time.FPS class.
    FPS is average value of recent n(buff_len) times, and you can call fps_set_buff_len(10) to change buffer length, default is 20.
    Multiple invoke this function will calculate fps between two invoke, and you can also call fps_start() fisrt to manually assign fps calulate start point.
    
    Returns: float type, current fps since last call this method
    """
def fps_set_buff_len(len: int) -> None:
    """
    Set fps method buffer length, by default the buffer length is 10.
    
    Args:
      - len: Buffer length to store recent fps value.
    """
def fps_start() -> None:
    """
    Manually set fps calculation start point, then you can call fps() function to calculate fps between fps_start() and fps().
    """
def gmtime(timestamp: float) -> DateTime:
    """
    timestamp to DateTime(time zone is UTC (value 0))
    
    Args:
      - timestamp: double timestamp
    
    
    Returns: DateTime
    """
def list_timezones() -> dict[str, list[str]]:
    """
    List all timezone info
    
    Returns: A dict with key are regions, and value are region's cities.
    """
def localtime() -> DateTime:
    """
    Get local time
    
    Returns: local time, DateTime type
    """
def now() -> DateTime:
    """
    Get current UTC date and time
    
    Returns: current date and time, DateTime type
    """
def strptime(str: str, format: str) -> DateTime:
    """
    DateTime from string
    
    Args:
      - str: date time string
      - format: date time format
    
    
    Returns: DateTime
    """
def ticks_diff(last: float, now: float = -1) -> float:
    """
    Calculate time difference in s.
    
    Args:
      - last: last time
      - now: current time, can be -1 if use current time
    
    
    Returns: time difference
    """
def ticks_ms() -> int:
    """
    Get current time in ms since bootup
    
    Returns: current time in ms, uint64_t type
    """
def ticks_s() -> float:
    """
    Get current time in s since bootup
    
    Returns: current time in s, double type
    """
def ticks_us() -> int:
    """
    Get current time in us since bootup
    
    Returns: current time in us, uint64_t type
    """
def time() -> float:
    """
    Get current time in s
    
    Returns: current time in s, double type
    """
def time_diff(last: float, now: float = -1) -> float:
    """
    Calculate time difference in s.
    
    Args:
      - last: last time
      - now: current time, can be -1 if use current time
    
    
    Returns: time difference
    """
def time_ms() -> int:
    """
    Get current time in ms
    
    Returns: current time in ms, uint64_t type
    """
def time_s() -> int:
    """
    Get current time in s
    
    Returns: current time in s, uint64_t type
    """
def time_us() -> int:
    """
    Get current time in us
    
    Returns: current time in us, uint64_t type
    """
def timezone(timezone: str = '') -> str:
    """
    Set or get timezone
    
    Args:
      - timezone: string type, can be empty and default to empty, if empty, only return crrent timezone, a "region/city" string, e.g. Asia/Shanghai, Etc/UTC, you can get all by list_timezones function.
    
    
    Returns: string type, return current timezone setting.
    """
