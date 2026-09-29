from backend.config import Settings
from backend.db.seed import initialize_database


def main() -> None:
    settings = Settings()
    counts = initialize_database(settings.database_path, settings.data_dir)
    for table, count in counts.items():
        print(f"{table}: {count}")
    print("DB 준비 완료. 기존 적재 데이터는 덮어쓰지 않습니다.")


if __name__ == "__main__":
    main()
