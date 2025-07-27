import asyncio
from sqlalchemy import text

from core.models import db_helper


async def init_default_data():
    # SQL-скрипт для вставки разрешений
    insert_permissions = """
    INSERT INTO permission (permission_id, name, description)
    SELECT * FROM (VALUES 
        (1,'admin', 'Administrator privileges'),
        (2, 'moderator', 'Content moderation'),
        (3, 'create', 'Create content'),
        (4, 'edit', 'Edit content'),
        (5, 'delete', 'Delete content')
    ) AS tmp(permission_id, name, description)
    WHERE NOT EXISTS (SELECT 1 FROM permission WHERE name = tmp.name)
    """
    
    async with db_helper.session_factory().begin() as conn:
        # Выполняем SQL-скрипт
        await conn.execute(text(insert_permissions))
        print("✅ Default permissions added")

asyncio.run(init_default_data())