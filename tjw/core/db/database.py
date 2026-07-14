import os
import sqlite3
from datetime import datetime
from typing import List, Optional, Dict

from .models import OperationLog, SFZRecord, UserSetting


class Database:
    _instance = None

    def __new__(cls, db_path: str = None):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, db_path: str = None):
        if self._initialized:
            return

        if db_path is None:
            db_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'tjw.db')
        
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._init_tables()
        self._initialized = True

    def _get_connection(self):
        return sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

    def _init_tables(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS operation_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation_type TEXT NOT NULL,
                    module TEXT NOT NULL,
                    details TEXT,
                    ip_address TEXT,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sfz_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_number TEXT NOT NULL,
                    region TEXT,
                    birth_date TEXT,
                    gender TEXT,
                    operation TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_sfz_records_created_at ON sfz_records(created_at)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_operation_logs_created_at ON operation_logs(created_at)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_user_settings_key ON user_settings(key)
            ''')

            conn.commit()

    def add_operation_log(self, operation_type: str, module: str, details: str = None, ip_address: str = None):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO operation_logs (operation_type, module, details, ip_address, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (operation_type, module, details, ip_address, datetime.now()))
            conn.commit()
            return cursor.lastrowid

    def get_operation_logs(self, limit: int = 100, offset: int = 0) -> List[OperationLog]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, operation_type, module, details, ip_address, created_at
                FROM operation_logs
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            ''', (limit, offset))
            rows = cursor.fetchall()
            return [OperationLog(*row) for row in rows]

    def add_sfz_record(self, id_number: str, region: str = None, birth_date: str = None,
                       gender: str = None, operation: str = 'generate'):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sfz_records (id_number, region, birth_date, gender, operation, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (id_number, region, birth_date, gender, operation, datetime.now()))
            conn.commit()
            return cursor.lastrowid

    def get_sfz_records(self, limit: int = 50, offset: int = 0) -> List[SFZRecord]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, id_number, region, birth_date, gender, operation, created_at
                FROM sfz_records
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            ''', (limit, offset))
            rows = cursor.fetchall()
            return [SFZRecord(*row) for row in rows]

    def get_sfz_record_count(self) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM sfz_records')
            return cursor.fetchone()[0]

    def set_setting(self, key: str, value: str, description: str = None):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO user_settings (key, value, description, created_at, updated_at)
                VALUES (?, ?, ?, COALESCE((SELECT created_at FROM user_settings WHERE key = ?), ?), ?)
            ''', (key, value, description, key, datetime.now(), datetime.now()))
            conn.commit()

    def get_setting(self, key: str, default: str = None) -> Optional[str]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT value FROM user_settings WHERE key = ?', (key,))
            row = cursor.fetchone()
            return row[0] if row else default

    def get_all_settings(self) -> Dict[str, UserSetting]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, key, value, description, created_at, updated_at FROM user_settings')
            rows = cursor.fetchall()
            return {row[1]: UserSetting(*row) for row in rows}

    def delete_setting(self, key: str):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM user_settings WHERE key = ?', (key,))
            conn.commit()

    def get_statistics(self) -> Dict[str, int]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM operation_logs')
            log_count = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM sfz_records')
            sfz_count = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM user_settings')
            setting_count = cursor.fetchone()[0]

            return {
                'operation_logs': log_count,
                'sfz_records': sfz_count,
                'user_settings': setting_count
            }

    def clear_old_data(self, days: int = 30):
        cutoff_date = datetime.now() - datetime.timedelta(days=days)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM operation_logs WHERE created_at < ?', (cutoff_date,))
            cursor.execute('DELETE FROM sfz_records WHERE created_at < ?', (cutoff_date,))
            conn.commit()