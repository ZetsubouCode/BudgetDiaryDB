from typing import List
from sqlalchemy.sql import func
from datetime import date
from sqlalchemy.orm import joinedload
from ..__database import get_session
from ..model.database import BudgetList as BudgetListModel
from ..utils import Debug, DebugLevel

class BudgetList:

    @staticmethod
    async def get_budget_list_total() -> BudgetListModel:
        """
        Get the first result of BudgetList by its id
        @param target_id: The id of the BudgetList data
        @return: BudgetList object
        """
        with get_session() as session:
            budget_list = session.query(func.sum(BudgetListModel.amount).label("amount")).all()

        return budget_list
    
    @staticmethod
    async def get_monthly_budget_list(first_date: date, last_date: date) -> BudgetListModel:
        """
        Get the first result of BudgetList by its id
        @param target_id: The id of the BudgetList data
        @return: BudgetList object
        """
        with get_session() as session:
            budget_list = session.query(BudgetListModel).options(joinedload(BudgetListModel.category)
            ).filter(BudgetListModel.date_buy>=first_date,BudgetListModel.date_buy<=last_date).all()

        return budget_list

    @staticmethod
    async def get_monthly_total(first_date: date, last_date: date) -> BudgetListModel:
        """
        Get the first result of BudgetList by its id
        @param target_id: The id of the BudgetList data
        @return: BudgetList object
        """
        with get_session() as session:
            budget_list = session.query(func.sum(BudgetListModel.amount).label("amount")).filter(
                BudgetListModel.date_buy>=first_date,BudgetListModel.date_buy<=last_date).all()

        return budget_list
    
    @staticmethod
    async def get_all() -> List[BudgetListModel]:
        """
        Get all result of BudgetList data
        @return: List of BudgetList object
        """
        with get_session() as session:
            budget_list = session.query(BudgetListModel).all()
        return budget_list

    @staticmethod
    async def add(category_id: int, date_buy: date, detail:str, amount:int) -> BudgetListModel:
        """
        Create BudgetList object and add it to the database
        @param last_layer: BudgetList last_layer
        @param last_room: BudgetList last_room
        @return: BudgetList object
        """
        with get_session() as session:
            budget_list = BudgetListModel(category_id=category_id, date_buy=date_buy, detail=detail, amount=amount)
            session.add(budget_list)
            session.commit()
            session.flush()
            session.refresh(budget_list)

            return budget_list
    
    @staticmethod
    async def update_by_id(target_id: int, new_obj:BudgetListModel) -> BudgetListModel:
        """
        Update BudgetList object that have the specific id
        @param taget_id: BudgetList id
        @param new_obj: BudgetList BudgetList new set of data
        @return: BudgetList object
        """
        with get_session() as sess:
            sess.query(BudgetListModel).filter_by(id=int(target_id)).update(
                    {
                        BudgetListModel.category_id : new_obj.category_id,
                        BudgetListModel.detail : new_obj.detail,
                        BudgetListModel.amount : new_obj.amount,
                    }
                )
            sess.commit()
        return new_obj
   
    @staticmethod
    async def delete_by_id(target_id: int):
        """
        Delete BudgetList object that have the specific id
        @param taget_id: BudgetList id
        """
        try:
            with get_session() as sess:
            
                try:
                    sess.query(BudgetListModel).filter_by(id=int(target_id)).delete()
                    sess.commit()
                    sess.flush()
                    
                except Exception as e:
                    sess.rollback()
                    Debug.msg("BudgetListController|delete_by_id", "Failed to Delete {}".format(e), DebugLevel.WARNING)
                    
        except Exception as e:
            Debug.msg("BudgetListController|delete_by_id", "Exception Raised {}".format(e), DebugLevel.ERROR)