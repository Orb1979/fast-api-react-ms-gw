from fastapi import Depends, FastAPI, HTTPException, Response, status, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import get_db
from .models import Customer
from .schemas import CustomerCreateUpdate, CustomerRead

app = FastAPI(title="customer-service")
router = APIRouter(prefix="/api/customer")


@router.get("/customers", response_model=list[CustomerRead])
def find_all(db: Session = Depends(get_db)) -> list[Customer]:
    return list(db.scalars(select(Customer)).all())


@router.get("/customers/{id}", response_model=CustomerRead)
def find_one(id: int, db: Session = Depends(get_db)) -> Customer:
    customer = db.get(Customer, id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return customer


@router.post(
    "/customers",
    response_model=CustomerRead,
    status_code=status.HTTP_201_CREATED,
)
def create(payload: CustomerCreateUpdate, db: Session = Depends(get_db)) -> Customer:
    customer = Customer(
        name=payload.name,
        email=payload.email,
        phone_number=payload.phone_number,
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@router.put("/customers/{id}", response_model=CustomerRead)
def update(id: int, payload: CustomerCreateUpdate, db: Session = Depends(get_db)) -> Customer:
    customer = db.get(Customer, id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    customer.name = payload.name
    customer.email = payload.email
    customer.phone_number = payload.phone_number
    db.commit()
    db.refresh(customer)
    return customer


@router.delete("/customers/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)) -> Response:
    customer = db.get(Customer, id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(customer)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# mount the router to the app
app.include_router(router)
