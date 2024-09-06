from abc import ABC, abstractmethod
import re
from pii_extract.api import PiiExtractor

class AnonymizationAdapter(ABC):
    @abstractmethod
    def anonymize(self, text: str) -> str:
        pass

class Anonymizer(AnonymizationAdapter):
    def __init__(self, config):
        self.pre_scrub_patterns = config.get("anonymize_patterns", {})
        self.use_pii_extract = config.get("use_pii_extract", True)
        if self.use_pii_extract:
            # Initialize PiiExtractor with relevant PII tasks
            self.pii_extractor = PiiExtractor(lang="en")  # Specify language as needed

    def pre_scrub(self, text: str) -> str:
        for pattern in self.pre_scrub_patterns.values():
            text = re.sub(pattern, "<anonymized>", text)
        return text

    def anonymize(self, text: str) -> str:
        text = self.pre_scrub(text)  # Always perform pre-scrubbing
        if self.use_pii_extract:
            # Apply PiiExtractor for anonymization
            piis = self.pii_extractor.extract(text)
            for pii in piis:
                text = text.replace(pii['match'], "<anonymized>")
        return text
