from fastapi import APIRouter, Form
from typing import Optional

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
            message = "User not found"
            Debug.msg(debug_identifier, message)
            return BaseResponse(**{"status": message})

        return BaseResponse(**{"status": "Success", "content": user})

    except Exception as e:
        message = "Server error"
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": message})


@subroute.get("/all", response_model=BaseResponse)
async def get_all():
    debug_identifier = "User|get_all"
    try:
        users = await UserController.get_all()
        if not users:
            message = "Data not found"
            Debug.msg(debug_identifier, message)
            return BaseResponse(**{"status": message})

        return BaseResponse(**{"status": "Success", "content": users})

    except Exception as e:
        message = "Server error"
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": message})


@subroute.post("/add", response_model=BaseResponse)
async def add(discord_username:str = Form(...), pin:str = Form(...)):
    debug_identifier = "UserRoute|add"
    try:
        if await UserController.get_by_discord_username(discord_username):
            message = "User already exists"
            Debug.msg(debug_identifier, message)
            return BaseResponse(**{"status": message})
        
        encrypted_pin = await UserController.encrypt_pin(pin)
        user = await UserController.add(discord_username, encrypted_pin)

        if not user:
            message = "User not found"
            Debug.msg(debug_identifier, message)
            return BaseResponse(**{"status": message})

        return BaseResponse(**{"status": "Success", "content": user})

    except Exception as e:
        message = "Server error"
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": message})


@subroute.put("/update/id/{id}", response_model=BaseResponse)
async def update_by_id(id: int, discord_username: Optional[str] = Form(None), 
                       pin: Optional[str] = Form(None), balance: Optional[float] = Form(None)):
    debug_identifier = "UserRoute|update_by_id"
    try:
        updated_user = await UserController.get_by_id(id)
        if not updated_user:
            message = "User does not exist"
            Debug.msg(debug_identifier, message)
            return BaseResponse(**{"status": message})
        
        check_if_exist = await UserController.get_by_discord_username(discord_username)
        if check_if_exist and check_if_exist.discord_username != updated_user.discord_username:
            message = "Username already exists"
            Debug.msg(debug_identifier, message)
            return BaseResponse(**{"status": message})

        if discord_username:
            updated_user.discord_username = discord_username
        if pin:
            updated_user.pin = pin
        if balance:
            updated_user.balance = balance

        user = await UserController.update_by_id(id, updated_user)
        if not user:
            message = "User not found"
            Debug.msg(debug_identifier, message)
            return BaseResponse(**{"status": message})

        return BaseResponse(**{"status": "Success", "content": user})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})


@subroute.patch("/update/discord_username/{discord_username}", response_model=BaseResponse)
async def update_by_username(discord_username: str, new_discord_username:Optional[str] = Form(None), 
                             pin:Optional[str] = Form(None),balance:Optional[float] = Form(None)):

    debug_identifier = "UserRoute|update_by_name"
    try:
        if not (new_discord_username and pin and balance):
            message = "Nothing to update"
            Debug.msg(debug_identifier, message)
            return BaseResponse(**{"status": message})
        updated_user = await UserController.get_by_discord_username(discord_username)
        if not updated_user:
            message = "User does not exist"
            Debug.msg(debug_identifier, message)
            return BaseResponse(**{"status": message})
        if new_discord_username:
            check_if_exist = await UserController.get_by_discord_username(new_discord_username)
            if check_if_exist and check_if_exist.discord_username != updated_user.discord_username:
                message = "User already exist"
                Debug.msg(debug_identifier, message)
                return BaseResponse(**{"status": message})
            updated_user.discord_username = new_discord_username
        if pin:
            updated_user.pin = pin
        if balance:
            updated_user.balance = balance

        user = await UserController.update_by_discord_username(discord_username, updated_user, balance)
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
            message = "User does not exist"
            Debug.msg(debug_identifier, message)
            return BaseResponse(**{"status": message})
        
        await UserController.delete_by_id(id)

        message = "Delete action successful"
        Debug.msg(debug_identifier, message)
        return BaseResponse(**{"status": "Success", "content": message})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})


@subroute.delete("/delete/discord_username/{discord_username}", response_model=BaseResponse)
async def delete_by_username(target_name: str):
    debug_identifier = "UserRoute|delete_by_username"
    try:
        user = await UserController.get_by_discord_username(target_name)
        if not user:
            message = "User does not exist"
            Debug.msg(debug_identifier, message)
            return BaseResponse(**{"status": message})

        deleted = await UserController.delete_by_discord_username(target_name)
        if not deleted:
            message = "Failed to delete user"
            Debug.msg(debug_identifier, message)
            return BaseResponse(**{"status": message})

        message = "Delete action successful"
        Debug.msg(debug_identifier, message)
        return BaseResponse(**{"status": "Success", "content": message})

    except Exception as e:
        Debug.msg(debug_identifier, "Exception Raised: {}".format(e))
        return BaseResponse(**{"status": "Server error"})