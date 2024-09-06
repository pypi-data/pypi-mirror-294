from abc import ABC, abstractmethod
import re
from pii_extract.api.processor import PiiProcessor
from pii_extract.defs import LANG_ANY

class AnonymizationAdapter(ABC):
    @abstractmethod
    def anonymize(self, text: str) -> str:
        pass

class Anonymizer(AnonymizationAdapter):
    def __init__(self, config):
        self.pre_scrub_patterns = config.get("anonymize_patterns", {})
        self.use_pii_extract = config.get("use_pii_extract", True)
        if self.use_pii_extract:
            # Initialize PiiProcessor and configure it to detect specific PII types
            self.pii_processor = PiiProcessor()
            self.pii_processor.build_tasks([("en", LANG_ANY)])  # Detect PII in English texts

    def pre_scrub(self, text: str) -> str:
        for pattern in self.pre_scrub_patterns.values():
            text = re.sub(pattern, "<anonymized>", text)
        return text

    def anonymize(self, text: str) -> str:
        text = self.pre_scrub(text)  # Always perform pre-scrubbing
        if self.use_pii_extract:
            # Process text and extract PII entities
            processed_text = self.pii_processor.process(text, "en")
            return processed_text
        return text
