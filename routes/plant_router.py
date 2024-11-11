from fastapi import APIRouter, Depends
from sqlmodel import Session
from database.schema import PlantCreate, PlantBase, PlantUpdate, PlantShow, TaskUpdate, TaskCreate, TaskShow
from controllers.plant_controller import PlantController
from database.database import get_session

plant_router = APIRouter(prefix="/plants",tags=["Plants"])

@plant_router.post("/",response_model=PlantShow, status_code=201)
async def create_plant(data:PlantCreate, session:Session = Depends(get_session)):
    controller = PlantController(session)
    return controller.create_plant(data)

@plant_router.get('/',status_code=200,response_model=PlantShow)
async def get_plant_all(session:Session = Depends(get_session)):
    controller = PlantController(session)
    plants = controller.get_all_plan()
    return {"data":plants}

@plant_router.get('/{plant_id}',status_code=200)
async def show_plan(plant_id:int,session:Session = Depends(get_session)):
    controller = PlantController(session)
    return controller.show_plan_with_task(plant_id)

@plant_router.delete('/{plant_id}',response_model=PlantShow)
async def delete_plan(plant_id:int, session:Session = Depends(get_session)):
    controller = PlantController(session)
    return controller.delete_plan(plant_id)

@plant_router.patch('/{plant_id}',response_model=PlantShow)
async def update_plant(plant_id:int,data:PlantUpdate,session:Session= Depends(get_session)):
    controller = PlantController(session)
    return controller.update_plan(plant_id,data)

#  Task
@plant_router.post('/task/',response_model=TaskShow)
async def create_task(data:TaskCreate, session:Session = Depends(get_session)):
    controller = PlantController(session)
    return controller.create_task(data)

@plant_router.patch('/task/{task_id}')
async def update_task(task_id:int, data:TaskUpdate, session: Session= Depends(get_session)):
    controller = PlantController(session)
    return controller.update_task(task_id, data)

@plant_router.delete('/task/{task_id}')
async def delete_task(task_id:int,session:Session= Depends(get_session)):
    controller = PlantController(session)
    return controller.delete_task(task_id)









