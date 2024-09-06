from abc import ABC, abstractmethod
import re
from pii_extract.api import PiiProcessor

class AnonymizationAdapter(ABC):
    @abstractmethod
    def anonymize(self, text: str) -> str:
        pass

class Anonymizer(AnonymizationAdapter):
    def __init__(self, config):
        self.pre_scrub_patterns = config.get("anonymize_patterns", {})
        self.use_pii_extract = config.get("use_pii_extract", True)
        if self.use_pii_extract:
            # Initialize PiiProcessor with a specific language, e.g., English
            self.pii_processor = PiiProcessor(lang="en")

    def pre_scrub(self, text: str) -> str:
        for pattern in self.pre_scrub_patterns.values():
            text = re.sub(pattern, "<anonymized>", text)
        return text

    def anonymize(self, text: str) -> str:
        text = self.pre_scrub(text)  # Always perform pre-scrubbing
        if self.use_pii_extract:
            # Extract and anonymize PII entities
            anonymized_text = self.pii_processor.process(text)
            return anonymized_text
        return text
