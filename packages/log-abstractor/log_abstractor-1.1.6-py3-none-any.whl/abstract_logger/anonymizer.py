from abc import ABC, abstractmethod
import re
from piidata.piidetector import PiiDetector

class AnonymizationAdapter(ABC):
    @abstractmethod
    def anonymize(self, text: str) -> str:
        pass

class Anonymizer(AnonymizationAdapter):
    def __init__(self, config):
        self.pre_scrub_patterns = config.get("anonymize_patterns", {})
        self.use_pii_data = config.get("use_pii_data", True)
        if self.use_pii_data:
            # Create PiiDetector instance
            self.pii_detector = PiiDetector()

    def pre_scrub(self, text: str) -> str:
        for pattern in self.pre_scrub_patterns.values():
            text = re.sub(pattern, "<anonymized>", text)
        return text

    def anonymize(self, text: str) -> str:
        text = self.pre_scrub(text)  # Always perform pre-scrubbing
        if self.use_pii_data:
            # Apply PiiData to anonymize
            detected_pii = self.pii_detector.detect_pii(text)
            for pii in detected_pii:
                text = text.replace(pii["entity"], "<anonymized>")
        return text
