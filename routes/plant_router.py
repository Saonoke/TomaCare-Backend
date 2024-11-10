from fastapi import APIRouter, Depends, Request
from sqlmodel import Session
from database.schema import PlantCreate, PlantBase, PlantUpdate, PlantShow
from controllers.plant_controller import PlantController
from database.database import get_session

plant_router = APIRouter(prefix="/plants",tags=["Plants"])



@plant_router.post("/",response_model=PlantCreate, status_code=201)
async def create_plant(request: Request, data:PlantCreate, session:Session = Depends(get_session))-> PlantCreate:
    controller = PlantController(request.state.user, session)
    return controller.create_plant(data)

@plant_router.get('/',status_code=200)
async def get_plant_all(request: Request, session:Session = Depends(get_session)):
    controller = PlantController(request.state.user, session)
    plants = controller.get_all_plan()
    return {"data":plants}

@plant_router.get('/{plant_id}',status_code=200)
async def show_plan(request: Request, plant_id:int, session:Session = Depends(get_session))->PlantBase:
    controller = PlantController(request.state.user, session)
    return controller.show_plan_with_task(plant_id)

@plant_router.delete('/{plant_id}')
async def delete_plan(request: Request, plant_id:int, session:Session = Depends(get_session))->PlantBase:
    controller = PlantController(request.state.user, session)
    return controller.delete_plan(plant_id)

@plant_router.patch('/{plant_id}')
async def update_plant(request: Request, plant_id:int,data:PlantUpdate,session:Session= Depends(get_session)):
    controller = PlantController(request.state.user, session)
    return controller.update_plan(plant_id,data)







