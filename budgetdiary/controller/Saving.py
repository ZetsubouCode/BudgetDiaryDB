from typing import List
from datetime import date
from sqlalchemy.sql import func
from sqlalchemy.orm import joinedload
from ..__database import get_session
from ..model.database import Saving as SavingModel
from ..utils import Debug, DebugLevel

class Saving:
    @staticmethod
    async def get_by_id(target_id: int) -> SavingModel:
        """
        Get the first result of Saving by its id
        @param target_id: The id of the Saving data
        @return: Saving object
        """
        with get_session() as session:
            saving = session.query(SavingModel).options(
                joinedload(SavingModel.user)).filter_by(id=target_id).first()

        return saving
    
    @staticmethod
    async def get_all_by_user_id(target_user_id: int) -> SavingModel:
        """
        Get the all result of Saving by its id
        @param target_id: The id of the Saving data
        @return: Saving object
        """
        with get_session() as session:
            saving = session.query(SavingModel).options(
                joinedload(SavingModel.user)).filter_by(id=target_user_id).all()

        return saving

    @staticmethod
    async def get_all() -> List[SavingModel]:
        """
        Get all result of Saving data
        @return: List of Saving object
        """
        with get_session() as session:
            saving = session.query(SavingModel).options(
                joinedload(SavingModel.user)).all()
        return saving

    @staticmethod
    async def add(description: str, amount: float, due_date: date) -> SavingModel:
        """
        Create Saving object and add it to the database
        @param last_layer: Saving last_layer
        @param last_room: Saving last_room
        @return: Saving object
        """
        with get_session() as session:
            saving = SavingModel(description=description,
                                 amount=amount,
                                 due_date=due_date)
            session.add(saving)
            session.commit()
            session.flush()
            session.refresh(saving)

            return saving

    @staticmethod
    async def update_by_id(target_id: int,
                           new_obj: SavingModel) -> SavingModel:
        """
        Update Saving object that have the specific id
        @param taget_id: Saving id
        @param new_obj: Saving Saving new set of data
        @return: Saving object
        """
        with get_session() as sess:
            sess.query(SavingModel).filter_by(id=int(target_id)).update({
                SavingModel.description:new_obj.description,
                SavingModel.amount:new_obj.amount,
                SavingModel.due_date:new_obj.due_date
            })
            sess.commit()
        return new_obj

    @staticmethod
    async def delete_by_id(target_id: int):
        """
        Delete Saving object that have the specific id
        @param taget_id: Saving id
        """
        try:
            with get_session() as sess:

                try:
                    sess.query(SavingModel).filter_by(
                        id=int(target_id)).delete()
                    sess.commit()
                    sess.flush()

                except Exception as e:
                    sess.rollback()
                    Debug.msg("SavingController|delete_by_id",
                              "Failed to Delete {}".format(e),
                              DebugLevel.WARNING)

        except Exception as e:
            Debug.msg("SavingController|delete_by_id",
                      "Exception Raised {}".format(e), DebugLevel.ERROR)
