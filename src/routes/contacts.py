from fastapi_limiter.depends import RateLimiter
from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from src.database.db import get_db
from src.entity.models import User
from src.repository import contacts as repository_contacts
from src.schemas.contact import ContactResponse, ContactSchema
from src.services.auth import auth_service
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get('/', response_model=list[ContactResponse], tags=['contacts'],
            dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def get_contacts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                       db: AsyncSession = Depends(get_db),
                       user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts(limit, offset, db, user)
    return contacts


@router.get('/{contact_id}', response_model=ContactResponse, tags=['contacts'],
            dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def get_contact(contact_id: int, db: AsyncSession = Depends(get_db),
                      user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact(contact_id, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact


@router.get('/birthday/{birthday_days}', response_model=list[ContactResponse], tags=['contacts'],
            dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def get_birthday_contacts(birthday_days: int, db: AsyncSession = Depends(get_db),
                      user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_birthday_contacts(birthday_days, db, user)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found...')
    return contacts


@router.post('/', response_model=ContactResponse, tags=['contacts'], status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(get_db),
                      user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.create_contact(body, db, user)
    return contact


@router.put('/{contact_id}', response_model=ContactResponse, tags=['contacts'])
async def update_contact(body: ContactSchema, contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                      user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(contact_id, body, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact


@router.delete('/{contact_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                      user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.delete_contact(contact_id, db, user)
    return contact.scalars().all()


@router.get('/by_params/', response_model=list[ContactResponse], tags=['contacts'])
async def get_contacts_by_params(name: str | None = None, surname: str | None = None, email: str | None = None,
                                 db: AsyncSession = Depends(get_db),
                                 user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts_by_params(name, surname, email, db, user)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found...')
    return contacts
