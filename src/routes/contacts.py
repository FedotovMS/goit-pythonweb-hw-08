from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas.contacts import ContactCreate, ContactResponse
from src.services.contacts import ContactService

router = APIRouter()


#  Створюємо контакт
@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(contact: ContactCreate, db: AsyncSession = Depends(get_db)):
    service = ContactService(db)
    return await service.create_contact(contact)


#  Отимуємо всі контакти
@router.get("/", response_model=list[ContactResponse])
async def get_contacts(db: AsyncSession = Depends(get_db)):
    service = ContactService(db)
    return await service.get_contacts()


#  Шукаємо контакт за email
@router.get("/search", response_model=list[ContactResponse])
async def search_contacts(
    query: str = Query(..., description="Search by name or email"),
    db: AsyncSession = Depends(get_db),
):
    service = ContactService(db)
    return await service.search_contacts(query)


#  Отримуємо контакт за ID
@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    service = ContactService(db)
    contact = await service.get_contact(contact_id)

    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    return contact


#  Оновлюємо існуючий контакт
@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int, updated_data: ContactCreate, db: AsyncSession = Depends(get_db)
):
    service = ContactService(db)
    contact = await service.update_contact(contact_id, updated_data)

    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    return contact


#  Видаляємо контакт
@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    service = ContactService(db)
    contact = await service.delete_contact(contact_id)

    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    return None


#  Отримуємо контакти з найближчими ДН
@router.get("/birthdays", response_model=list[ContactResponse])
async def get_upcoming_birthdays(db: AsyncSession = Depends(get_db)):
    service = ContactService(db)
    return await service.get_upcoming_birthdays()