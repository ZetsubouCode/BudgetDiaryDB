import os
import hashlib
from typing import List
from datetime import date
from sqlalchemy.sql import func
from sqlalchemy.orm import joinedload
from ..__database import get_session
from ..model.database import User as UserModel
from ..utils import Debug, DebugLevel

class User:
    @staticmethod
    async def get_by_id(target_id: int) -> UserModel:
        """
        Get the first result of User by its id
        @param target_id: The id of the User data
        @return: User object
        """
        with get_session() as session:
            user = session.query(UserModel).filter_by(id=target_id).first()

        return user

    @staticmethod
    async def get_by_username(target_username: str) -> UserModel:
        """
        Get the first result of User by its username
        @param target_id: The id of the User data
        @return: User object
        """
        with get_session() as session:
            user = session.query(UserModel).filter_by(discord_username=target_username).first()

        return user

    @staticmethod
    async def get_all() -> List[UserModel]:
        """
        Get all result of User data
        @return: List of User object
        """
        with get_session() as session:
            user = session.query(UserModel).all()
        return user

    @staticmethod
    async def add(discord_username: str, pin: str, balance: float) -> UserModel:
        """
        Create User object and add it to the database
        @param last_layer: User last_layer
        @param last_room: User last_room
        @return: User object
        """
        with get_session() as session:
            user = UserModel(discord_username=discord_username,
                                 pin=pin,
                                 balance=balance)
            session.add(user)
            session.commit()
            session.flush()
            session.refresh(user)

            return user

    @staticmethod
    async def update_by_id(target_id: int,
                           new_obj: UserModel) -> UserModel:
        """
        Update User object that have the specific id
        @param taget_id: User id
        @param new_obj: User User new set of data
        @return: User object
        """
        with get_session() as sess:
            sess.query(UserModel).filter_by(id=int(target_id)).update({
                UserModel.discord_username:new_obj.discord_username,
                UserModel.pin:new_obj.pin,
                UserModel.balance:new_obj.balance
            })
            sess.commit()
        return new_obj

@staticmethod
async def delete_by_id(target_id: int):
    """
    Delete User object that have the specific id
    @param taget_id: User id
    """
    try:
        with get_session() as sess:
            try:
                sess.query(UserModel).filter_by(
                    id=int(target_id)).delete()
                sess.flush()

            except Exception as e:
                sess.rollback()
                Debug.msg("UserController|delete_by_id",
                          "Failed to Delete {}".format(e),
                          DebugLevel.WARNING)
                return False

            try:
                sess.commit()
            except Exception as e:
                sess.rollback()
                Debug.msg("UserController|delete_by_id",
                          "Failed to commit transaction: {}".format(e),
                          DebugLevel.ERROR)
                return False
                
        return True

    except Exception as e:
        Debug.msg("UserController|delete_by_id",
                  "Exception Raised {}".format(e), DebugLevel.ERROR)
        return False
            
    @staticmethod
    async def encrypt_pin(pin:str) -> str:
        encoded = (pin+os.environ.get("SALT")).encode()
        result = hashlib.sha256(encoded)
        
        return result.hexdigest()

    @staticmethod
    async def authenticate(username:str, pin:str) -> bool :
        log_identifier = "UserController|check_pin"

        result = await User.encrypt_pin(pin)
        data = await User.get_by_username(username)
        if not data:
            Debug.msg(log_identifier, "Data not found", DebugLevel.INFO)
            return None
        if result!=data.pin:
            Debug.msg(log_identifier, "Wrong PIN", DebugLevel.INFO)
            return None

        return data
