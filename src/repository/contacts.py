from datetime import date, timedelta

from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from src.entity.models import Contact, User
from src.schemas.contact import ContactSchema


async def get_contacts(limit: int, offset: int, db: AsyncSession, user: User):
    stmt = select(Contact).filter_by(user=user).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession, user: User):
    stmt = select(Contact).filter_by(id=contact_id, user=user)
    contacts = await db.execute(stmt)
    return contacts.scalar_one_or_none()


async def get_birthday_contacts(days: int, db: AsyncSession, user: User):
    dateFrom = date.today()
    dateTo = date.today() + timedelta(days=days)
    thisYear = dateFrom.year
    nextYear = dateFrom.year + 1
    stmt = select(Contact).filter(or_(func.to_date(func.concat(func.to_char(Contact.birthday, "DDMM"), thisYear),
                                                   "DDMMYYYY").between(dateFrom, dateTo),
                                      func.to_date(func.concat(func.to_char(Contact.birthday, "DDMM"), nextYear),
                                                   "DDMMYYYY").between(dateFrom, dateTo))).filter_by(user=user)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def create_contact(body: ContactSchema, db: AsyncSession, user: User):
    contact = Contact(**body.model_dump(exclude_unset=True), user=user)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactSchema, db: AsyncSession, user: User):
    stmt = select(Contact).filter_by(id=contact_id, user=user)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.description = body.description
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession, user: User):
    stmt = select(Contact).filter_by(id=contact_id, user=user)
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact


async def get_contacts_by_params(name: str | None, surname: str | None, email: str | None, db: AsyncSession, user: User):
    if name is not None:
        stmt = select(Contact.id, Contact.name, Contact.surname, Contact.email, Contact.phone_number, Contact.birthday, Contact.description).filter_by(name=name)
    elif surname is not None:
        stmt = select(Contact.id, Contact.name, Contact.surname, Contact.email, Contact.phone_number, Contact.birthday, Contact.description).filter_by(surname=surname)
    elif email is not None:
        stmt = select(Contact.id, Contact.name, Contact.surname, Contact.email, Contact.phone_number, Contact.birthday, Contact.description).filter_by(email=email)
    else:
        pass
    contacts = await db.execute(stmt)
    return contacts
