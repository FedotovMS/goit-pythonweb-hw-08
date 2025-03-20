from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, and_

from src.entity.models import Contact
from src.schemas.contacts import ContactCreate


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    #  Створюємо контакт
    async def create(self, contact: Contact):
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    #  Отримуємо всі контакти
    async def get_all(self):
        result = await self.db.execute(select(Contact))
        return result.scalars().all()

    #  Отримуємо контакт за ID
    async def get_by_id(self, contact_id: int):
        result = await self.db.execute(select(Contact).where(Contact.id == contact_id))
        return result.scalar_one_or_none()

    #  Оновлюємо контакт
    async def update(self, contact_id: int, updated_data: ContactCreate):
        contact = await self.get_by_id(contact_id)
        if not contact:
            return None  

        for key, value in updated_data.dict().items():
            setattr(contact, key, value)

        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    #  Видалялємо контатк
    async def delete(self, contact_id: int):
        contact = await self.get_by_id(contact_id)
        if not contact:
            return None  

        await self.db.delete(contact)
        await self.db.commit()
        return contact

    #  Шукаємо контакт за імʼям або email
    async def search_contacts(self, query: str):
        stmt = select(Contact).where(
            or_(
                Contact.first_name.ilike(f"%{query}%"),
                Contact.last_name.ilike(f"%{query}%"),
                Contact.email.ilike(f"%{query}%"),
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

        # Отримуємо контакти з найближчим ДН

    async def get_upcoming_birthdays(self):
        today = datetime.today().date()
        next_week = today + timedelta(days=7)

        stmt = select(Contact).where(
            and_(Contact.birth_date >= today, Contact.birth_date <= next_week)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()