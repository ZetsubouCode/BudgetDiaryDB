from fastapi import APIRouter, Form

from ..controller.User import User as UserController
from ..model.response import BaseResponse
from ..utils import Debug

subroute = APIRouter()

@subroute.post("/login", response_model=BaseResponse)
async def login(discord_username:str = Form(...), password:str = Form(...)):
    debug_identifier = "User|login"
    try:
        user = await UserController.authenticate(discord_username, password)
        if not user:
            Debug.msg(debug_identifier, "Username or password is incorrect")
            return BaseResponse(**{"status": "Username or password is incorrect"})

        return BaseResponse(**{"status": "Success", "content": user})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})

@subroute.get("/id/{id}", response_model=BaseResponse)
async def get_by_id(id: int):
    debug_identifier = "User|get_by_id"
    try:
        user = await UserController.get_by_id(id)
        if not user:
            Debug.msg(debug_identifier, "User not found")
            return BaseResponse(**{"status": "User not found"})
        
        return BaseResponse(**{"status": "Success", "content": user})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})

@subroute.get("/all", response_model=BaseResponse)
async def get_all():
    debug_identifier = "User|get_all"
    try:
        user = await UserController.get_all()
        if not user:
            Debug.msg(debug_identifier, "Data not found")
            return BaseResponse(**{"status": "Data not found"})

        return BaseResponse(**{"status": "Success", "content": user})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})

@subroute.post("/add", response_model=BaseResponse)
async def add(discord_username:str = Form(...), pin:str = Form(...)):
    debug_identifier = "UserRoute|add"
    try:
        if await UserController.get_by_username(discord_username):
            Debug.msg(debug_identifier, "User already exist")
            return BaseResponse(**{"status": "User already exist"})

        user = await UserController.add(discord_username,pin)

        if not user:
            Debug.msg(debug_identifier, "User not found")
            return BaseResponse(**{"status": "User not found"})

        return BaseResponse(**{"status": "Success", "content": user})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})

@subroute.put("/update/id/{id}", response_model=BaseResponse)
async def update_by_id(id: int, discord_username:str = Form(...), pin: str = Form(...), balance:float = Form(...),):
                      
    debug_identifier = "UserRoute|update_by_id"
    try:
        updated_user = await UserController.get_by_id(id)
        if not updated_user:
            Debug.msg(debug_identifier, "User does not exist")
            return BaseResponse(**{"status": "User does not exist"})

        check_if_exist = await UserController.get_by_id(id)
        if check_if_exist and check_if_exist.discord_username != updated_user.discord_username:
            return BaseResponse(**{"status": "Username already exist"})

        updated_user.discord_username = discord_username
        updated_user.pin = pin

        user = await UserController.update_by_id(id, updated_user)
        if not user:
            Debug.msg(debug_identifier, "User not found")
            return BaseResponse(**{"status": "User not found"})

        return BaseResponse(**{"status": "Success", "content": user})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})


@subroute.put("/update/discord_username/{discord_username}", response_model=BaseResponse)
async def update_by_username(discord_username: str, pin:str = Form(...),balance:float = Form(...)):

    debug_identifier = "UserRoute|update_by_name"
    try:
        updated_user = await UserController.get_by_username(discord_username)
        if not updated_user:
            Debug.msg(debug_identifier, "User does not exist")
            return BaseResponse(**{"status": "User does not exist"})

        check_if_exist = await UserController.get_by_username(discord_username)
        if check_if_exist and check_if_exist.discord_username != updated_user.discord_username:
            return BaseResponse(**{"status": "User already exist"})

        updated_user.discord_username = discord_username
        updated_user.pin = pin
        updated_user.balance = balance

        user = await UserController.update_by_username(discord_username, updated_user, balance)
        if not user:
            Debug.msg(debug_identifier, "User not found")
            return BaseResponse(**{"status": "User not found"})

        return BaseResponse(**{"status": "Success", "content": user})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})


@subroute.delete("/delete/id/{id}", response_model=BaseResponse)
async def delete_by_id(id: int):
    debug_identifier = "UserRoute|delete_by_id"
    try:
        user = await UserController.get_by_id(id)
        if not user:
            Debug.msg(debug_identifier, "User does not exist")
            return BaseResponse(**{"status": "User does not exist"})
        
        await UserController.delete_by_id(id)

        return BaseResponse(**{"status": "Success", "content": "Delete action successful"})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})


@subroute.delete("/delete/discord_username/{discord_username}", response_model=BaseResponse)
async def delete_by_username(target_name: str):
    debug_identifier = "UserRoute|delete_by_username"
    try:
        user = await UserController.get_by_username(target_name)
        if not user:
            Debug.msg(debug_identifier, "User does not exist")
            return BaseResponse(**{"status": "User does not exist"})

        await UserController.delete_by_username(target_name)
        if not user:
            Debug.msg(debug_identifier, "User not found")
            return BaseResponse(**{"status": "User not found"})

        return BaseResponse(**{"status": "Success", "content": "Delete action successful"})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})