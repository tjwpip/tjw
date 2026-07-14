from .database import Database

_db = None


def get_db() -> Database:
    global _db
    if _db is None:
        _db = Database()
    return _db


def log_operation(operation_type: str, module: str, details: str = None, ip_address: str = None):
    db = get_db()
    return db.add_operation_log(operation_type, module, details, ip_address)


def record_sfz_generation(id_number: str, region: str = None, birth_date: str = None, gender: str = None):
    db = get_db()
    return db.add_sfz_record(id_number, region, birth_date, gender, operation='generate')


def record_sfz_verification(id_number: str, region: str = None, birth_date: str = None, gender: str = None):
    db = get_db()
    return db.add_sfz_record(id_number, region, birth_date, gender, operation='verify')


def get_settings():
    db = get_db()
    return db.get_all_settings()


def get_setting(key: str, default: str = None):
    db = get_db()
    return db.get_setting(key, default)


def set_setting(key: str, value: str, description: str = None):
    db = get_db()
    return db.set_setting(key, value, description)


def get_statistics():
    db = get_db()
    return db.get_statistics()