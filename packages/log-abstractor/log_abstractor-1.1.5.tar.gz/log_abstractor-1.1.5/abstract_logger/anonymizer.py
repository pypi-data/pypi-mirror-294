from abc import ABC, abstractmethod
import scrubadub
import re
class AnonymizationAdapter(ABC):
    @abstractmethod
    def anonymize(self, text: str) -> str:
        pass

class Anonymizer(AnonymizationAdapter):
    def __init__(self, config):
        self.pre_scrub_patterns = config.get("anonymize_patterns", {})
        self.use_scrubadub = config.get("use_scrubadub", True)
        if self.use_scrubadub:
            # Register only the detectors you need
            scrubadub.detectors.register_detector(scrubadub.detectors.EmailDetector)
            scrubadub.detectors.register_detector(scrubadub.detectors.PhoneDetector)
            scrubadub.detectors.register_detector(scrubadub.detectors.SSNDetector)

    def pre_scrub(self, text: str) -> str:
        for pattern in self.pre_scrub_patterns.values():
            text = re.sub(pattern, "<anonymized>", text)
        return text

    def anonymize(self, text: str) -> str:
        text = self.pre_scrub(text)  # Always perform pre-scrubbing
        if self.use_scrubadub:
            text = scrubadub.clean(text)  # Only apply Scrubadub if enabled
        return text