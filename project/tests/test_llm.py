import json

import httpx
import pytest
from groq import Groq

from backend.config import Settings
from backend.integrations.llm import GenerationError, GroqGenerator, create_generator


def test_stub_needs_no_key_or_network():
    settings = Settings(_env_file=None, llm_provider="stub", groq_api_key="", groq_model="")
    assert "고정 응답" in create_generator(settings).generate("테스트")


def test_live_provider_requires_explicit_configuration():
    settings = Settings(_env_file=None, llm_provider="groq", groq_api_key="", groq_model="")
    with pytest.raises(ValueError, match="GROQ_API_KEY"):
        create_generator(settings)


def mock_sdk(monkeypatch, handler):
    def factory(**kwargs):
        return Groq(**kwargs, http_client=httpx.Client(transport=httpx.MockTransport(handler)))

    monkeypatch.setattr("backend.integrations.llm.Groq", factory)


def test_groq_request_and_response_without_external_call(monkeypatch):
    def handler(request):
        body = json.loads(request.content)
        assert body["model"] == "test-model"
        assert body["messages"] == [{"role": "user", "content": "연결 테스트"}]
        return httpx.Response(
            200,
            json={
                "id": "test",
                "object": "chat.completion",
                "created": 0,
                "model": "test-model",
                "choices": [
                    {
                        "index": 0,
                        "finish_reason": "stop",
                        "message": {"role": "assistant", "content": "연결 성공"},
                    }
                ],
            },
        )

    mock_sdk(monkeypatch, handler)
    assert GroqGenerator("test-key", "test-model").generate("연결 테스트") == "연결 성공"


def test_groq_error_is_not_returned_as_a_successful_answer(monkeypatch):
    mock_sdk(
        monkeypatch,
        lambda request: httpx.Response(
            401,
            json={"error": {"message": "private service details", "type": "authentication_error"}},
        ),
    )
    with pytest.raises(GenerationError) as error:
        GroqGenerator("test-key", "test-model").generate("연결 테스트")
    assert "private service details" not in str(error.value)


def test_empty_groq_response_is_rejected(monkeypatch):
    mock_sdk(
        monkeypatch,
        lambda request: httpx.Response(
            200,
            json={
                "id": "test",
                "object": "chat.completion",
                "created": 0,
                "model": "test-model",
                "choices": [],
            },
        ),
    )
    with pytest.raises(GenerationError, match="비어 있는"):
        GroqGenerator("test-key", "test-model").generate("연결 테스트")
