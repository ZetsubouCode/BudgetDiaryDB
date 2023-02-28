from datetime import date
from fastapi import APIRouter, Form

from ..controller.Saving import Saving as SavingController
from ..controller.User import User as UserController
from ..model.response import BaseResponse
from ..utils import Debug

subroute = APIRouter()

@subroute.get("/id/{id}", response_model=BaseResponse)
async def get_by_id(id: int):
    debug_identifier = "Saving|get_by_id"
    try:
        saving = await SavingController.get_by_id(id)
        if not saving:
            Debug.msg(debug_identifier, "Saving not found")
            return BaseResponse(**{"status": "Saving not found"})
        
        return BaseResponse(**{"status": "Success", "content": saving})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})

@subroute.get("/all", response_model=BaseResponse)
async def get_all():
    debug_identifier = "Saving|get_all"
    try:
        saving = await SavingController.get_all()
        if not saving:
            Debug.msg(debug_identifier, "Data not found")
            return BaseResponse(**{"status": "Data not found"})

        return BaseResponse(**{"status": "Success", "content": saving})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})
    
@subroute.get("/user_id/{user_id}/all", response_model=BaseResponse)
async def get_all(user_id: int):

    debug_identifier = "Saving|get_all_by_user_id"
    try:
        saving = await SavingController.get_all_by_user_id(user_id)
        if not saving:
            Debug.msg(debug_identifier, "Data not found")
            return BaseResponse(**{"status": "Data not found"})

        return BaseResponse(**{"status": "Success", "content": saving})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})

@subroute.post("/add", response_model=BaseResponse)
async def add(user_id:int = Form(...),description:str = Form(...), amount:float = Form(...),due_date:date=Form(...)):
    debug_identifier = "SavingRoute|add"
    try:
        user = await UserController.get_by_id(user_id)
        if not user:
            Debug.msg(debug_identifier, "User not found")
            return BaseResponse(**{"status": "User not found"})
        saving = await SavingController.add(user_id,description,amount,due_date)
        if not saving:
            Debug.msg(debug_identifier, "Saving not found")
            return BaseResponse(**{"status": "Saving not found"})

        return BaseResponse(**{"status": "Success", "content": saving})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})

@subroute.put("/update/id/{id}", response_model=BaseResponse)
async def update_by_id(id: int, user_id:int = Form(...),description:str = Form(...), amount: str = Form(...), due_date:date = Form(...)):
                      
    debug_identifier = "SavingRoute|update_by_id"
    try:
        user = await UserController.get_by_id(user_id)
        if not user:
            Debug.msg(debug_identifier, "User not found")
            return BaseResponse(**{"status": "User not found"})
        
        updated_saving = await SavingController.get_by_id(id)
        if not updated_saving:
            Debug.msg(debug_identifier, "Saving does not exist")
            return BaseResponse(**{"status": "Saving does not exist"})

        updated_saving.user_id = user_id
        updated_saving.description = description
        updated_saving.amount = amount
        updated_saving.due_date = due_date

        saving = await SavingController.update_by_id(id, updated_saving)
        if not saving:
            Debug.msg(debug_identifier, "Saving not found")
            return BaseResponse(**{"status": "Saving not found"})

        return BaseResponse(**{"status": "Success", "content": saving})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})

@subroute.delete("/delete/id/{id}", response_model=BaseResponse)
async def delete_by_id(id: int):
    debug_identifier = "SavingRoute|delete_by_id"
    try:
        saving = await SavingController.get_by_id(id)
        if not saving:
            Debug.msg(debug_identifier, "Saving does not exist")
            return BaseResponse(**{"status": "Saving does not exist"})
        
        await SavingController.delete_by_id(id)

        return BaseResponse(**{"status": "Success", "content": "Delete action successful"})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})