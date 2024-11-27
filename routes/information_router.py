from fastapi import APIRouter, Depends
from sqlmodel import Session

from controllers.information_controller import InformationController
from database.database import get_session
from database.schema import InformationResponse

information_router = APIRouter(
    prefix="/information",
    tags=["Information"],
)

@information_router.get("", response_model=list[InformationResponse] , status_code=200)
async def get_informations(session:Session = Depends(get_session)):
    controller = InformationController(session)
    return controller.get_all()

@information_router.get("/{_id}", response_model=InformationResponse, status_code=200)
async def get_information(_id: int, session:Session = Depends(get_session)):
    controller = InformationController(session)
    return controller.get_by_id(_id)
