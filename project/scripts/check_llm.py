import argparse

from backend.config import Settings
from backend.integrations.llm import GenerationError, create_generator


def main() -> None:
    parser = argparse.ArgumentParser(description="고정 응답 또는 Groq 연결을 확인합니다.")
    parser.add_argument("--live", action="store_true", help="실제 Groq API를 1회 호출합니다.")
    args = parser.parse_args()
    settings = Settings(llm_provider="groq" if args.live else "stub")
    try:
        print(
            create_generator(settings).generate("연결 테스트입니다. 한국어로 짧게 인사해 주세요.")
        )
    except (ValueError, GenerationError) as exc:
        parser.exit(1, f"{exc}\n")


if __name__ == "__main__":
    main()
