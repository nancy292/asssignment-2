from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models import TaskBoard  # Import your model 
from uuid import uuid4 
from google.cloud import firestore


app = FastAPI()
firestore_db = firestore.Client()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Root route
@app.get("/", response_class=HTMLResponse)
def get_login(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

@app.get("/addtaskboard", response_class=HTMLResponse)
def get_addtaskboard(request: Request):
    return templates.TemplateResponse("addTaskBoard.html", {"request": request})

@app.post("/addtaskboard/create")
async def create_taskboard(taskboard: TaskBoard):
    print("taskboard in create",taskboard)
    taskboard_dict = taskboard.dict()
    board_id = str(uuid4()) 
    firestore_db.collection("taskboards").document(board_id).set(taskboard_dict)
    return {"message": "TaskBoard created", "id": board_id}


@app.get("/viewtaskboard", response_class=HTMLResponse)
def view_taskboard(request: Request):
    return templates.TemplateResponse("viewtaskboard.html", {"request": request})

@app.get("/taskboards/{useremail}")
async def get_taskboard(useremail: str):
    user_tasks = []

    # Query Firestore for all taskboards
    taskboards_ref = firestore_db.collection("taskboards")  # Replace "taskboards" with your collection name

    # Get taskboards documents
    taskboards = taskboards_ref.stream()
    for taskboard in taskboards:
        taskboard_data = taskboard.to_dict()
        print("all taskboards ",taskboard_data)

        # Loop through each task in the taskboard and check if the user is assigned to it
        if(useremail == taskboard_data["createdBy"]):
            user_tasks.append(taskboard_data)

    return {"user_tasks": user_tasks}
