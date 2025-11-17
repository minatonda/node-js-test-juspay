"""
Test result model for tracking test outcomes
"""
from typing import Optional


class TestResult:
    """
    Represents the result of a single test assertion.
    """
    
    def __init__(self, name: str):
        """
        Initialize a test result.
        
        Args:
            name: Test name/description
        """
        self.name = name
        self.ok = True
        self.info: Optional[str] = None
    
    def fail(self, msg: str):
        """
        Mark the test as failed with a message.
        
        Args:
            msg: Failure message
        """
        self.ok = False
        self.info = msg
    
    def success(self, msg: Optional[str] = None):
        """
        Mark the test as successful (optional message).
        
        Args:
            msg: Optional success message
        """
        self.ok = True
        if msg:
            self.info = msg
    
    def __str__(self) -> str:
        """String representation of test result"""
        status = "✓" if self.ok else "✗"
        info = f" - {self.info}" if self.info else ""
        return f"{status} {self.name}{info}"

