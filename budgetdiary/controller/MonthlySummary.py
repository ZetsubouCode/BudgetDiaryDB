from typing import List
from datetime import date
from sqlalchemy.sql import func
from sqlalchemy.orm import joinedload
from ..__database import get_session
from ..model.database import MonthlySummary as MonthlySummaryModel
from ..utils import Debug, DebugLevel

class MonthlySummary:
    @staticmethod
    async def get_by_id(target_id: int) -> MonthlySummaryModel:
        """
        Get the first result of MonthlySummary by its id
        @param target_id: The id of the MonthlySummary data
        @return: MonthlySummary object
        """
        with get_session() as session:
            monthly_summary = session.query(MonthlySummaryModel).options(
                joinedload(MonthlySummaryModel.user)).filter_by(id=target_id).first()

        return monthly_summary
    
    @staticmethod
    async def get_all_by_user_id(target_user_id: int) -> MonthlySummaryModel:
        """
        Get the all result of MonthlySummary by its id
        @param target_id: The id of the MonthlySummary data
        @return: MonthlySummary object
        """
        with get_session() as session:
            monthly_summary = session.query(MonthlySummaryModel).options(
                joinedload(MonthlySummaryModel.user)).filter_by(id=target_user_id).all()

        return monthly_summary

    @staticmethod
    async def get_all() -> List[MonthlySummaryModel]:
        """
        Get all result of MonthlySummary data
        @return: List of MonthlySummary object
        """
        with get_session() as session:
            monthly_summary = session.query(MonthlySummaryModel).options(
                joinedload(MonthlySummaryModel.user)).all()
        return monthly_summary

    @staticmethod
    async def add(description: str, amount: float, due_date: date) -> MonthlySummaryModel:
        """
        Create MonthlySummary object and add it to the database
        @param last_layer: MonthlySummary last_layer
        @param last_room: MonthlySummary last_room
        @return: MonthlySummary object
        """
        with get_session() as session:
            monthly_summary = MonthlySummaryModel(description=description,
                                 amount=amount,
                                 due_date=due_date)
            session.add(monthly_summary)
            session.commit()
            session.flush()
            session.refresh(monthly_summary)

            return monthly_summary

    @staticmethod
    async def update_by_id(target_id: int,
                           new_obj: MonthlySummaryModel) -> MonthlySummaryModel:
        """
        Update MonthlySummary object that have the specific id
        @param taget_id: MonthlySummary id
        @param new_obj: MonthlySummary MonthlySummary new set of data
        @return: MonthlySummary object
        """
        with get_session() as sess:
            sess.query(MonthlySummaryModel).filter_by(id=int(target_id)).update({
                MonthlySummaryModel.description:new_obj.description,
                MonthlySummaryModel.amount:new_obj.amount,
                MonthlySummaryModel.due_date:new_obj.due_date
            })
            sess.commit()
        return new_obj

    @staticmethod
    async def delete_by_id(target_id: int):
        """
        Delete MonthlySummary object that have the specific id
        @param taget_id: MonthlySummary id
        """
        try:
            with get_session() as sess:

                try:
                    sess.query(MonthlySummaryModel).filter_by(
                        id=int(target_id)).delete()
                    sess.commit()
                    sess.flush()

                except Exception as e:
                    sess.rollback()
                    Debug.msg("MonthlySummaryController|delete_by_id",
                              "Failed to Delete {}".format(e),
                              DebugLevel.WARNING)

        except Exception as e:
            Debug.msg("MonthlySummaryController|delete_by_id",
                      "Exception Raised {}".format(e), DebugLevel.ERROR)
