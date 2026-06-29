import hashlib
import sqlite3
import sys
sys.path.insert(0, '.')
from models.user import User
from models.db_manager import DBManager

stored = '$f47ac10b-58cc-4372-a567-0e02b2c3d479$8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'
parts = stored.split('$')
print('parts count:', len(parts))
print('sha256(admin):', hashlib.sha256(b'admin').hexdigest())
print('stored hash:', parts[2] if len(parts) > 2 else 'n/a')

db = DBManager('database/kaban.db')
db.connect()
user = User.get_by_username('admin', db)
if user:
    print('db password:', user.password)
    print('check_password(admin):', user.check_password('admin'))
else:
    print('admin user not found')
