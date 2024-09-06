from abc import ABC, abstractmethod
import re
from pii_extract import PiiCollectionBuilder

class AnonymizationAdapter(ABC):
    @abstractmethod
    def anonymize(self, text: str) -> str:
        pass

class Anonymizer(AnonymizationAdapter):
    def __init__(self, config):
        self.pre_scrub_patterns = config.get("anonymize_patterns", {})
        self.use_pii_extract = config.get("use_pii_extract", True)
        if self.use_pii_extract:
            # Initialize PiiCollectionBuilder with English as the language
            self.pii_collection_builder = PiiCollectionBuilder(lang="en")
            self.pii_collection_builder.build_tasks(["email", "phone", "ssn"])

    def pre_scrub(self, text: str) -> str:
        for pattern in self.pre_scrub_patterns.values():
            text = re.sub(pattern, "<anonymized>", text)
        return text

    def anonymize(self, text: str) -> str:
        text = self.pre_scrub(text)  # Always perform pre-scrubbing
        if self.use_pii_extract:
            # Extract PII entities using PiiCollectionBuilder and replace them
            piis = self.pii_collection_builder(text)
            for pii in piis:
                text = text.replace(pii["value"], "<anonymized>")
        return text
