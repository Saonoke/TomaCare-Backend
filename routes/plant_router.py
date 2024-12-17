from fastapi import APIRouter, Depends, Request, File , UploadFile
from sqlmodel import Session
from database.schema import PlantCreate, PlantBase, PlantUpdate, PlantShow, TaskUpdate, TaskCreate, TaskShow
from controllers.plant_controller import PlantController
from database.database import get_session


plant_router = APIRouter(prefix="/plants",tags=["Plants"])



@plant_router.post("/",response_model=PlantShow, status_code=201)
async def create_plant(request: Request, data:PlantCreate, session:Session = Depends(get_session)):
    controller = PlantController(request.state.user, session)
    return controller.create_plant(data)

@plant_router.post('/upload/')
async def upload_image(request: Request,file: UploadFile,session:Session= Depends(get_session)):
    controller = PlantController(request.state.user, session)
    content = await file.read()  # Membaca file gambar ke dalam memori
    result =  controller.machine_learning_process(file=content)
    
    return result


@plant_router.get('/',status_code=200)
async def get_plant_all(request: Request, session:Session = Depends(get_session)):
    controller = PlantController(request.state.user, session)
    return controller.get_all_plan()

@plant_router.get('/{plant_id}',status_code=200)
async def show_plan(request: Request, plant_id:int, session:Session = Depends(get_session)):
    controller = PlantController(request.state.user, session)
    return controller.show_plan_with_task(plant_id)
  
@plant_router.delete('/{plant_id}',response_model=PlantShow)
async def delete_plan(request: Request, plant_id:int, session:Session = Depends(get_session)):
    controller = PlantController(request.state.user, session)
    return controller.delete_plan(plant_id)

@plant_router.put('/{plant_id}',response_model=PlantShow)
async def update_plant(request: Request, plant_id:int,data:PlantUpdate,session:Session= Depends(get_session)):
    controller = PlantController(request.state.user, session)
    return controller.update_plan(plant_id,data)

#  Task
@plant_router.post('/task/',response_model=TaskShow)
async def create_task(data:TaskCreate, session:Session = Depends(get_session)):
    controller = PlantController(session)
    return controller.create_task(data)

@plant_router.put('/task/{task_id}')
async def update_task(request: Request,task_id:int, data:TaskUpdate, session: Session= Depends(get_session)):
    controller = PlantController(request.state.user,session)
    return controller.update_task(task_id, data)

@plant_router.delete('/task/{task_id}')
async def delete_task(task_id:int,session:Session= Depends(get_session)):
    controller = PlantController(session)
    return controller.delete_task(task_id)



