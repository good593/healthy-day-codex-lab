-- 초기 스키마. CREATE IF NOT EXISTS는 기존 테이블의 컬럼을 변경하지 않는다.
-- 스키마 변경 및 PostgreSQL 전환은 후속 강의에서 명시적 마이그레이션으로 구현한다.
CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    manufacturer TEXT NOT NULL,
    category TEXT NOT NULL,
    ingredient_keyword TEXT NOT NULL,
    concern TEXT NOT NULL,
    report_number TEXT NOT NULL,
    registered_on TEXT NOT NULL,
    shelf_life TEXT,
    appearance TEXT,
    intake_method TEXT NOT NULL,
    precautions TEXT,
    functionality TEXT NOT NULL,
    source_url TEXT,
    data_source TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS nutrient_functions (
    source_row INTEGER PRIMARY KEY,
    nutrient TEXT NOT NULL,
    category TEXT NOT NULL,
    functionality TEXT NOT NULL,
    concern TEXT NOT NULL,
    keyword TEXT NOT NULL,
    evidence_level TEXT NOT NULL,
    evidence_description TEXT NOT NULL,
    reliability TEXT NOT NULL,
    source TEXT NOT NULL,
    source_url TEXT
);

CREATE TABLE IF NOT EXISTS intake_references (
    source_row INTEGER PRIMARY KEY,
    nutrient TEXT NOT NULL,
    age_group TEXT NOT NULL,
    sex TEXT NOT NULL,
    pregnancy TEXT NOT NULL,
    lactation TEXT NOT NULL,
    recommended REAL,
    adequate REAL,
    upper_limit REAL,
    upper_limit_raw TEXT,
    unit TEXT NOT NULL,
    source TEXT NOT NULL,
    organization TEXT NOT NULL,
    note TEXT,
    source_url TEXT
);

-- 세 파일을 한 묶음으로 처음 한 번만 적재한다.
CREATE TABLE IF NOT EXISTS seed_history (
    seed_name TEXT PRIMARY KEY,
    imported_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
