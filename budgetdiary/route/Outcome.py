from datetime import date
from fastapi import APIRouter, Form

from ..controller.Outcome import Outcome as OutcomeController
from ..controller.User import User as UserController
from ..model.response import BaseResponse
from ..utils import Debug

subroute = APIRouter()

@subroute.get("/id/{id}", response_model=BaseResponse)
async def get_by_id(id: int):
    debug_identifier = "Outcome|get_by_id"
    try:
        outcome = await OutcomeController.get_by_id(id)
        if not outcome:
            Debug.msg(debug_identifier, "Outcome not found")
            return BaseResponse(**{"status": "Outcome not found"})
        
        return BaseResponse(**{"status": "Success", "content": outcome})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})

@subroute.get("/all", response_model=BaseResponse)
async def get_all():
    debug_identifier = "Outcome|get_all"
    try:
        outcome = await OutcomeController.get_all()
        if not outcome:
            Debug.msg(debug_identifier, "Data not found")
            return BaseResponse(**{"status": "Data not found"})

        return BaseResponse(**{"status": "Success", "content": outcome})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})
    
@subroute.get("/user_id/{user_id}/all", response_model=BaseResponse)
async def get_all(user_id: int):

    debug_identifier = "Outcome|get_all_by_user_id"
    try:
        outcome = await OutcomeController.get_all_by_user_id(user_id)
        if not outcome:
            Debug.msg(debug_identifier, "Data not found")
            return BaseResponse(**{"status": "Data not found"})

        return BaseResponse(**{"status": "Success", "content": outcome})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})

@subroute.post("/add", response_model=BaseResponse)
async def add(user_id:int = Form(...),description:str = Form(...), amount:float = Form(...),due_date:date=Form(...)):
    debug_identifier = "OutcomeRoute|add"
    try:
        user = await UserController.get_by_id(user_id)
        if not user:
            Debug.msg(debug_identifier, "User not found")
            return BaseResponse(**{"status": "User not found"})
        outcome = await OutcomeController.add(user_id,description,amount,due_date)
        if not outcome:
            Debug.msg(debug_identifier, "Outcome not found")
            return BaseResponse(**{"status": "Outcome not found"})

        return BaseResponse(**{"status": "Success", "content": outcome})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})

@subroute.put("/update/id/{id}", response_model=BaseResponse)
async def update_by_id(id: int, user_id:int = Form(...),description:str = Form(...), amount: str = Form(...), due_date:date = Form(...)):
                      
    debug_identifier = "OutcomeRoute|update_by_id"
    try:
        user = await UserController.get_by_id(user_id)
        if not user:
            Debug.msg(debug_identifier, "User not found")
            return BaseResponse(**{"status": "User not found"})
        
        updated_outcome = await OutcomeController.get_by_id(id)
        if not updated_outcome:
            Debug.msg(debug_identifier, "Outcome does not exist")
            return BaseResponse(**{"status": "Outcome does not exist"})

        updated_outcome.user_id = user_id
        updated_outcome.description = description
        updated_outcome.amount = amount
        updated_outcome.due_date = due_date

        outcome = await OutcomeController.update_by_id(id, updated_outcome)
        if not outcome:
            Debug.msg(debug_identifier, "Outcome not found")
            return BaseResponse(**{"status": "Outcome not found"})

        return BaseResponse(**{"status": "Success", "content": outcome})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})

@subroute.delete("/delete/id/{id}", response_model=BaseResponse)
async def delete_by_id(id: int):
    debug_identifier = "OutcomeRoute|delete_by_id"
    try:
        outcome = await OutcomeController.get_by_id(id)
        if not outcome:
            Debug.msg(debug_identifier, "Outcome does not exist")
            return BaseResponse(**{"status": "Outcome does not exist"})
        
        await OutcomeController.delete_by_id(id)

        return BaseResponse(**{"status": "Success", "content": "Delete action successful"})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})