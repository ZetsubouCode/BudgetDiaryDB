from typing import List
from sqlalchemy.sql import func
from datetime import date
from sqlalchemy.orm import joinedload
from ..__database import get_session
from ..model.database import Budget as BudgetModel
from ..utils import Debug, DebugLevel

class Budget:

    @staticmethod
    async def get_budget_total() -> BudgetModel:
        """
        Get the first result of Budget by its id
        @param target_id: The id of the Budget data
        @return: Budget object
        """
        with get_session() as session:
            budget = session.query(func.sum(BudgetModel.amount).label("amount")).all()

        return budget
    
    @staticmethod
    async def get_monthly_budget(first_date: date, last_date: date) -> BudgetModel:
        """
        Get the first result of Budget by its id
        @param target_id: The id of the Budget data
        @return: Budget object
        """
        with get_session() as session:
            budget = session.query(BudgetModel).options(joinedload(BudgetModel.category)
            ).filter(BudgetModel.date_buy>=first_date,BudgetModel.date_buy<=last_date).all()

        return budget

    @staticmethod
    async def get_monthly_total(first_date: date, last_date: date) -> BudgetModel:
        """
        Get the first result of Budget by its id
        @param target_id: The id of the Budget data
        @return: Budget object
        """
        with get_session() as session:
            budget = session.query(func.sum(BudgetModel.amount).label("amount")).filter(
                BudgetModel.date_buy>=first_date,BudgetModel.date_buy<=last_date).all()

        return budget
    
    @staticmethod
    async def get_all() -> List[BudgetModel]:
        """
        Get all result of Budget data
        @return: List of Budget object
        """
        with get_session() as session:
            budget = session.query(BudgetModel).all()
        return budget

    @staticmethod
    async def add(category_id: int, date_buy: date, detail:str, amount:int) -> BudgetModel:
        """
        Create Budget object and add it to the database
        @param last_layer: Budget last_layer
        @param last_room: Budget last_room
        @return: Budget object
        """
        with get_session() as session:
            budget = BudgetModel(category_id=category_id, date_buy=date_buy, detail=detail, amount=amount)
            session.add(budget)
            session.commit()
            session.flush()
            session.refresh(budget)

            return budget
    
    @staticmethod
    async def update_by_id(target_id: int, new_obj:BudgetModel) -> BudgetModel:
        """
        Update Budget object that have the specific id
        @param taget_id: Budget id
        @param new_obj: Budget Budget new set of data
        @return: Budget object
        """
        with get_session() as sess:
            sess.query(BudgetModel).filter_by(id=int(target_id)).update(
                    {
                        BudgetModel.category_id : new_obj.category_id,
                        BudgetModel.detail : new_obj.detail,
                        BudgetModel.amount : new_obj.amount,
                    }
                )
            sess.commit()
        return new_obj
   
    @staticmethod
    async def delete_by_id(target_id: int):
        """
        Delete Budget object that have the specific id
        @param taget_id: Budget id
        """
        try:
            with get_session() as sess:
            
                try:
                    sess.query(BudgetModel).filter_by(id=int(target_id)).delete()
                    sess.commit()
                    sess.flush()
                    
                except Exception as e:
                    sess.rollback()
                    Debug.msg("BudgetController|delete_by_id", "Failed to Delete {}".format(e), DebugLevel.WARNING)
                    
        except Exception as e:
            Debug.msg("BudgetController|delete_by_id", "Exception Raised {}".format(e), DebugLevel.ERROR)