from datetime import date
from fastapi import APIRouter, Form

from ..controller.Income import Income as IncomeController
from ..controller.User import User as UserController
from ..model.response import BaseResponse
from ..utils import Debug

subroute = APIRouter()

@subroute.get("/id/{id}", response_model=BaseResponse)
async def get_by_id(id: int):
    debug_identifier = "Income|get_by_id"
    try:
        income = await IncomeController.get_by_id(id)
        if not income:
            Debug.msg(debug_identifier, "Income not found")
            return BaseResponse(**{"status": "Income not found"})
        
        return BaseResponse(**{"status": "Success", "content": income})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})

@subroute.get("/all", response_model=BaseResponse)
async def get_all():
    debug_identifier = "Income|get_all"
    try:
        income = await IncomeController.get_all()
        if not income:
            Debug.msg(debug_identifier, "Data not found")
            return BaseResponse(**{"status": "Data not found"})

        return BaseResponse(**{"status": "Success", "content": income})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})
    
@subroute.get("/user_id/{user_id}/all", response_model=BaseResponse)
async def get_all(user_id: int):

    debug_identifier = "Income|get_all_by_user_id"
    try:
        income = await IncomeController.get_all_by_user_id(user_id)
        if not income:
            Debug.msg(debug_identifier, "Data not found")
            return BaseResponse(**{"status": "Data not found"})

        return BaseResponse(**{"status": "Success", "content": income})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})

@subroute.post("/add", response_model=BaseResponse)
async def add(user_id:int = Form(...),description:str = Form(...), amount:float = Form(...),due_date:date=Form(...)):
    debug_identifier = "IncomeRoute|add"
    try:
        user = await UserController.get_by_id(user_id)
        if not user:
            Debug.msg(debug_identifier, "User not found")
            return BaseResponse(**{"status": "User not found"})
        income = await IncomeController.add(user_id,description,amount,due_date)
        if not income:
            Debug.msg(debug_identifier, "Income not found")
            return BaseResponse(**{"status": "Income not found"})

        return BaseResponse(**{"status": "Success", "content": income})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})

@subroute.put("/update/id/{id}", response_model=BaseResponse)
async def update_by_id(id: int, user_id:int = Form(...),description:str = Form(...), amount: str = Form(...), due_date:date = Form(...)):
                      
    debug_identifier = "IncomeRoute|update_by_id"
    try:
        user = await UserController.get_by_id(user_id)
        if not user:
            Debug.msg(debug_identifier, "User not found")
            return BaseResponse(**{"status": "User not found"})
        
        updated_income = await IncomeController.get_by_id(id)
        if not updated_income:
            Debug.msg(debug_identifier, "Income does not exist")
            return BaseResponse(**{"status": "Income does not exist"})

        updated_income.user_id = user_id
        updated_income.description = description
        updated_income.amount = amount
        updated_income.due_date = due_date

        income = await IncomeController.update_by_id(id, updated_income)
        if not income:
            Debug.msg(debug_identifier, "Income not found")
            return BaseResponse(**{"status": "Income not found"})

        return BaseResponse(**{"status": "Success", "content": income})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})

@subroute.delete("/delete/id/{id}", response_model=BaseResponse)
async def delete_by_id(id: int):
    debug_identifier = "IncomeRoute|delete_by_id"
    try:
        income = await IncomeController.get_by_id(id)
        if not income:
            Debug.msg(debug_identifier, "Income does not exist")
            return BaseResponse(**{"status": "Income does not exist"})
        
        await IncomeController.delete_by_id(id)

        return BaseResponse(**{"status": "Success", "content": "Delete action successful"})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})