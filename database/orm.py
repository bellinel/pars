


from sqlalchemy import select
from database.engine import Database, OlxId, KrishaId


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


async def add_site_id_olx(site_id: int) -> OlxId:
      db = Database()

      async with db.session_factory() as session:
            id = OlxId(site_id=site_id)
            session.add(id)
            await session.commit()  


async def update_site_id_olx(site_id: int):
    db = Database()

    async with db.session_factory() as session:  # type: AsyncSession
        query = select(OlxId)
        result = await session.execute(query)
        olx_entry = result.scalar_one_or_none()

        if olx_entry:
            if olx_entry.site_id == site_id:
                print("ID совпадает — обновление не требуется")
                return None
            olx_entry.site_id = site_id
        else:
            session.add(OlxId(site_id=site_id))

        await session.commit()


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


async def get_site_id_olx() -> int:
      db = Database()

      async with db.session_factory() as session:
            query = select(OlxId.site_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

        