from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_

from src.entity.models import Contact
from src.repository.contacts import ContactRepository
from src.schemas.contacts import ContactCreate


class ContactService:
    def __init__(self, db: AsyncSession):
        self.repository = ContactRepository(db)

    #  Шукаємо контакт
    async def search_contacts(self, query: str):
        return await self.repository.search_contacts(query)

    #  Створюємо новий контакт
    async def create_contact(self, contact_data: ContactCreate):
        new_contact = Contact(**contact_data.model_dump())
        return await self.repository.create(new_contact)

    #  Отримуємо всі контакти
    async def get_contacts(self):
        return await self.repository.get_all()

    #  Отримуємо контакт за ID
    async def get_contact(self, contact_id: int):
        return await self.repository.get_by_id(contact_id)

    #  Оновлюємо контакт
    async def update_contact(self, contact_id: int, updated_data: ContactCreate):
        return await self.repository.update(contact_id, updated_data)

    #  Видаляємо контакт
    async def delete_contact(self, contact_id: int):
        return await self.repository.delete(contact_id)

    #  Отримуємо контакти з найближчими ДН
    async def get_upcoming_birthdays(self):
        return await self.repository.get_upcoming_birthdays()