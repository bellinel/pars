


from sqlalchemy import select, delete
from database.engine import Database, OlxId, KrishaId
from sqlalchemy.exc import IntegrityError


async def add_site_id_krisha(site_id: int):
        '''Добавляет id с сайта в таблицу '''
    
        db = Database()

        async with db.session_factory() as session:
            id = KrishaId(site_id=site_id)
            session.add(id)
            await session.commit()

            
           
        


async def get_site_id_krisha() -> int:
      db = Database()

      async with db.session_factory() as session:
            query = select(KrishaId.site_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

async def update_site_id_krisha(site_id: int):
        db = Database()

        async with db.session_factory() as session:  # type: AsyncSession
            query = select(KrishaId)
            result = await session.execute(query)
            krisha_entry = result.scalar_one_or_none()

            if krisha_entry:
                if krisha_entry.site_id == site_id:
                    print("ID совпадает — обновление не требуется")
                    return None
                krisha_entry.site_id = site_id
            else:
                session.add(KrishaId(site_id=site_id))

            await session.commit()  


async def update_site_url_olx(site_url: str):
    db = Database()

    async with db.session_factory() as session:  # type: AsyncSession
        # Проверяем, есть ли уже такая ссылка в базе
        query = select(OlxId).where(OlxId.site_url == site_url)
        result = await session.execute(query)
        existing = result.scalar_one_or_none()

        if existing:
            print("URL уже существует — обновление не требуется")
            return None

        # Добавляем новую ссылку
        session.add(OlxId(site_url=site_url))
        await session.commit()
        
        return True

async def update_site_url_olx(site_url: str):
    db = Database()

    async with db.session_factory() as session:
        try:
            query = select(OlxId).where(OlxId.site_url == site_url)
            result = await session.execute(query)
            existing = result.scalar_one_or_none()

            if existing:
                print("URL уже существует — обновление не требуется")
                return None

            session.add(OlxId(site_url=site_url))
            await session.commit()
            return True
        except IntegrityError:
            await session.rollback()
            print("Попытка добавить дубликат URL — откат транзакции")
            return None  


async def get_site_url_olx() -> str | None:
    db = Database()

    async with db.session_factory() as session:
        query = select(OlxId.site_url).order_by(OlxId.id.desc()).limit(1)
        result = await session.execute(query)
        return result.scalar_one_or_none()

async def clear_olx_table():
    db = Database()

    async with db.session_factory() as session:
        await session.execute(delete(OlxId))
        await session.commit()
        print("Таблица OlxId очищена.")
        
