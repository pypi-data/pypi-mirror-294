from abc import ABC, abstractmethod
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import AnonymizerConfig
import re


class AnonymizationAdapter(ABC):
    @abstractmethod
    def anonymize(self, text: str) -> str:
        pass


class Anonymizer(AnonymizationAdapter):
    def __init__(self, config):
        self.pre_scrub_patterns = config.get("anonymize_patterns", {})
        self.use_presidio = config.get("use_presidio", True)

        if self.use_presidio:
            self.analyzer = AnalyzerEngine()
            self.anonymizer = AnonymizerEngine()

    def pre_scrub(self, text: str) -> str:
        for pattern in self.pre_scrub_patterns.values():
            text = re.sub(pattern, "<anonymized>", text)
        return text

    def anonymize(self, text: str) -> str:
        text = self.pre_scrub(text)  # Always perform pre-scrubbing

        if self.use_presidio:
            # Analyze and anonymize the text using Presidio
            results = self.analyzer.analyze(text=text, entities=["PHONE_NUMBER", "EMAIL_ADDRESS", "PERSON"],
                                            language="en")
            anonymized_text = self.anonymizer.anonymize(text=text, analyzer_results=results,
                                                        anonymizers_config={"DEFAULT": AnonymizerConfig("replace", {
                                                            "new_value": "<anonymized>"})})
            return anonymized_text.text

        return text
