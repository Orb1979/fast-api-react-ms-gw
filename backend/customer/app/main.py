from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Customer
from .schemas import CustomerCreateUpdate, CustomerRead

app = FastAPI(title="customer-service")


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/api/customer/customers", response_model=list[CustomerRead])
def find_all(db: Session = Depends(get_db)) -> list[Customer]:
    return list(db.scalars(select(Customer)).all())


@app.get("/api/customer/customers/{id}", response_model=CustomerRead)
def find_one(id: int, db: Session = Depends(get_db)) -> Customer:
    customer = db.get(Customer, id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return customer


@app.post(
    "/api/customer/customers",
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


@app.put("/api/customer/customers/{id}", response_model=CustomerRead)
def update(
    id: int, payload: CustomerCreateUpdate, db: Session = Depends(get_db)
) -> Customer:
    customer = db.get(Customer, id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    customer.name = payload.name
    customer.email = payload.email
    customer.phone_number = payload.phone_number
    db.commit()
    db.refresh(customer)
    return customer


@app.delete("/api/customer/customers/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)) -> Response:
    customer = db.get(Customer, id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(customer)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Frontend compatibility for current delete URL composition:
# /api/customer/customers{id} (missing slash).
@app.delete("/api/customer/customers{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_no_slash(id: int, db: Session = Depends(get_db)) -> Response:
    return delete(id=id, db=db)
