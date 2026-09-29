"""후속 상담 실습의 연결 지점. 검색이나 RAG 기능은 아직 구현하지 않는다."""

from typing import Protocol

from groq import Groq, GroqError

from backend.config import Settings


class GenerationError(Exception):
    """외부 API 오류의 세부 정보나 키를 사용자 화면에 전달하지 않는다."""


class TextGenerator(Protocol):
    def generate(self, prompt: str) -> str: ...


class StubGenerator:
    def generate(self, prompt: str) -> str:
        return "연결 테스트용 고정 응답입니다. 실제 AI 상담 답변이 아닙니다."


class GroqGenerator:
    def __init__(self, api_key: str, model: str):
        if not api_key.strip() or not model.strip():
            raise ValueError("GROQ_API_KEY와 GROQ_MODEL을 .env에 설정하세요.")
        self.api_key = api_key
        self.model = model

    def generate(self, prompt: str) -> str:
        try:
            with Groq(api_key=self.api_key, timeout=20.0, max_retries=0) as client:
                result = client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_completion_tokens=512,
                )
        except GroqError as exc:
            raise GenerationError(
                "Groq 호출에 실패했습니다. 연결·계정·모델 설정을 확인하세요."
            ) from exc
        text = result.choices[0].message.content if result.choices else None
        if not text or not text.strip():
            raise GenerationError("Groq가 비어 있는 답변을 반환했습니다.")
        return text


def create_generator(settings: Settings) -> TextGenerator:
    if settings.llm_provider == "stub":
        return StubGenerator()
    return GroqGenerator(settings.groq_api_key.get_secret_value(), settings.groq_model)
