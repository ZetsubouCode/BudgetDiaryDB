from datetime import date
from fastapi import APIRouter, Form

from ..controller.Budget import Budget as BudgetController
from ..controller.User import User as UserController
from ..model.response import BaseResponse
from ..utils import Debug

subroute = APIRouter()

@subroute.get("/id/{id}", response_model=BaseResponse)
async def get_by_id(id: int):
    debug_identifier = "Budget|get_by_id"
    try:
        budget = await BudgetController.get_by_id(id)
        if not budget:
            Debug.msg(debug_identifier, "Budget not found")
            return BaseResponse(**{"status": "Budget not found"})
        
        return BaseResponse(**{"status": "Success", "content": budget})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})

@subroute.get("/all", response_model=BaseResponse)
async def get_all():
    debug_identifier = "Budget|get_all"
    try:
        budget = await BudgetController.get_all()
        if not budget:
            Debug.msg(debug_identifier, "Data not found")
            return BaseResponse(**{"status": "Data not found"})

        return BaseResponse(**{"status": "Success", "content": budget})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})
    
@subroute.get("/user_id/{user_id}/all", response_model=BaseResponse)
async def get_all(user_id: int):

    debug_identifier = "Budget|get_all_by_user_id"
    try:
        budget = await BudgetController.get_all_by_user_id(user_id)
        if not budget:
            Debug.msg(debug_identifier, "Data not found")
            return BaseResponse(**{"status": "Data not found"})

        return BaseResponse(**{"status": "Success", "content": budget})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})

@subroute.post("/add", response_model=BaseResponse)
async def add(user_id:int = Form(...),description:str = Form(...), amount:float = Form(...),due_date:date=Form(...)):
    debug_identifier = "BudgetRoute|add"
    try:
        user = await UserController.get_by_id(user_id)
        if not user:
            Debug.msg(debug_identifier, "User not found")
            return BaseResponse(**{"status": "User not found"})
        budget = await BudgetController.add(user_id,description,amount,due_date)
        if not budget:
            Debug.msg(debug_identifier, "Budget not found")
            return BaseResponse(**{"status": "Budget not found"})

        return BaseResponse(**{"status": "Success", "content": budget})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})

@subroute.put("/update/id/{id}", response_model=BaseResponse)
async def update_by_id(id: int, user_id:int = Form(...),description:str = Form(...), amount: str = Form(...), due_date:date = Form(...)):
                      
    debug_identifier = "BudgetRoute|update_by_id"
    try:
        user = await UserController.get_by_id(user_id)
        if not user:
            Debug.msg(debug_identifier, "User not found")
            return BaseResponse(**{"status": "User not found"})
        
        updated_budget = await BudgetController.get_by_id(id)
        if not updated_budget:
            Debug.msg(debug_identifier, "Budget does not exist")
            return BaseResponse(**{"status": "Budget does not exist"})

        updated_budget.user_id = user_id
        updated_budget.description = description
        updated_budget.amount = amount
        updated_budget.due_date = due_date

        budget = await BudgetController.update_by_id(id, updated_budget)
        if not budget:
            Debug.msg(debug_identifier, "Budget not found")
            return BaseResponse(**{"status": "Budget not found"})

        return BaseResponse(**{"status": "Success", "content": budget})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})

@subroute.delete("/delete/id/{id}", response_model=BaseResponse)
async def delete_by_id(id: int):
    debug_identifier = "BudgetRoute|delete_by_id"
    try:
        budget = await BudgetController.get_by_id(id)
        if not budget:
            Debug.msg(debug_identifier, "Budget does not exist")
            return BaseResponse(**{"status": "Budget does not exist"})
        
        await BudgetController.delete_by_id(id)

        return BaseResponse(**{"status": "Success", "content": "Delete action successful"})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})