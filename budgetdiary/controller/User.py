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
        Get the User object by its id
        @param target_id: The id of the User data
        @return: User object
        """
        with get_session() as session:
            user = session.query(UserModel).filter_by(id=target_id).first()

        return user

    @staticmethod
    async def get_by_username(target_username: str) -> UserModel:
        """
        Get the User object by its username
        @param target_id: The id of the User data
        @return: User object
        """
        with get_session() as session:
            user = session.query(UserModel).filter_by(discord_username=target_username).first()

        return user

    @staticmethod
    async def get_all() -> List[UserModel]:
        """
        Get all the User objects
        @return: List of User objects
        """
        with get_session() as session:
            user = session.query(UserModel).all()
        return user

    @staticmethod
    async def add(discord_username: str, pin: str, balance: float) -> UserModel:
        """
        Add a new User object to the database
        @param discord_username: Discord username of the user
        @param pin: PIN of the user
        @param balance: balance of the user
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
        Update the User object by its id
        @param target_id: Id of the User object to update
        @param new_obj: New User object data
        @return: Updated User object
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
        Delete the User object by its id
        @param target_id: Id of the User object to delete
        @return: True if User object is deleted, False otherwise
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
        """
        Encrypts the given PIN with SHA256 algorithm and returns the encrypted value.
        @param pin: The plain text PIN to be encrypted.
        @return: The encrypted value of the given PIN.
        """
        encoded = (pin+os.environ.get("SALT")).encode()
        result = hashlib.sha256(encoded)
        
        return result.hexdigest()

    @staticmethod
    async def authenticate(username:str, pin:str) -> bool :
        """
        Authenticates the user with the given username and PIN.
        @param username: The username of the user to be authenticated.
        @param pin: The PIN of the user to be authenticated.
        @return: True if the user is authenticated, False otherwise.
        """
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
