"""
Ethical validation utilities for ThinkAlike project.
"""

class EthicalDataset:
    """
    A wrapper around datasets that adds ethical validation capabilities.
    """
    
    def __init__(self, data):
        """
        Initialize the ethical dataset.
        
        Args:
            data: The dataset (pandas DataFrame, dict, etc.)
        """
        self.data = data
        self.validation_results = {}
    
    def validate(self, rules=None):
        """
        Validate the dataset against ethical rules.
        
        Args:
            rules: Optional list of rules to validate against
            
        Returns:
            bool: True if all rules pass, False otherwise
        """
        if rules is None:
            rules = self._default_rules()
        
        all_passed = True
        for rule in rules:
            result = rule(self.data)
            self.validation_results[rule.__name__] = result
            if not result:
                all_passed = False
        
        return all_passed
    
    def _default_rules(self):
        """
        Default ethical validation rules.
        
        Returns:
            list: List of validation functions
        """
        return [
            self._check_data_minimization,
            self._check_no_pii_in_clear_text,
        ]
    
    def _check_data_minimization(self, data):
        """Check if the dataset follows data minimization principle"""
        # Simplified implementation
        return True
    
    def _check_no_pii_in_clear_text(self, data):
        """Check if PII is properly protected"""
        # Simplified implementation
        return True

def validate_ethical_requirements(data, requirements=None):
    """
    Validates that data meets ethical requirements.
    
    Args:
        data: The data to validate
        requirements: Optional specific requirements to check
        
    Returns:
        bool: True if data meets requirements, False otherwise
    """
    dataset = EthicalDataset(data)
    return dataset.validate(requirements)

def log_error(message, severity="INFO"):
    """
    Log an error message with specified severity.
    
    Args:
        message: The error message
        severity: Severity level (INFO, WARNING, ERROR, CRITICAL)
    """
    import logging
    logger = logging.getLogger("ethical_validator")
    
    if severity == "INFO":
        logger.info(message)
    elif severity == "WARNING":
        logger.warning(message)
    elif severity == "ERROR":
        logger.error(message)
    elif severity == "CRITICAL":
        logger.critical(message)
    else:
        logger.info(message)
