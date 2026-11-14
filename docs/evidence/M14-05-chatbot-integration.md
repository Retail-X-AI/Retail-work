# M14-05: Historical Chatbot Interface Integration

## Original scope

The original M14-05 implementation connected the chatbot to an application through an HTTP API and browser-based interface.

The implementation included an application-facing service, HTTP endpoints, a browser interface and API integration tests.

## Current project scope

The HTTP API and browser interface are no longer part of the active project requirements. The current project retains the Python chatbot and its AI functionality.

The following components remain relevant:

- `python-ai/chatbot/assistant.py`: chatbot message processing and intent handling.
- `python-ai/chatbot/supplier_handler.py`: supplier-related chatbot functionality.
- `python-ai/chatbot/training_data.csv`: chatbot intent training data.
- `python-ai/chatbot/train_chatbot.py`: intent classifier training.
- `python-ai/chatbot/models/intent_classifier.joblib`: trained intent classification model.

## Scope clarification

The previous HTTP API and browser interface should not be interpreted as current deliverables. The current chatbot operates through its Python implementation and available project data.

The chatbot is not connected to live point-of-sale systems, physical store inventory or live supplier systems.

## Evidence status

This document records the change in scope from the original M14-05 interface integration to the current Python-based chatbot implementation. The old API tests and browser interface are not included in current test coverage.