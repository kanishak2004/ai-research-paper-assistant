
import pytest

from rag_pipeline import ResearchPaperAssistant


def test_empty_question_is_rejected():
    assistant = ResearchPaperAssistant.__new__(ResearchPaperAssistant)

    with pytest.raises(ValueError, match="Enter a question"):
        assistant.retrieve("   ")


def test_empty_collection_is_rejected():
    class EmptyCollection:
        def count(self):
            return 0

    assistant = ResearchPaperAssistant.__new__(ResearchPaperAssistant)
    assistant.collection = EmptyCollection()

    with pytest.raises(ValueError, match="Upload and index"):
        assistant.retrieve("What is the main finding?")
