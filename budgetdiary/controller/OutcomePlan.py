from typing import List
from sqlalchemy.sql import func
from datetime import date
from sqlalchemy.orm import joinedload
from ..__database import get_session
from ..model.database import OutcomePlan as OutcomePlanModel
from ..model.database import OutcomePlanCategory as OutcomePlanCategoryModel
from ..utils import Debug, DebugLevel

class OutcomePlan:
    @staticmethod
    async def get_by_id(target_id: int) -> OutcomePlanModel:
        """
        Get the first result of OutcomePlan by its id
        @param target_id: The id of the OutcomePlan data
        @return: OutcomePlan object
        """
        with get_session() as session:
            outcome_plan = session.query(OutcomePlanModel).filter_by(id=target_id).first()

        return outcome_plan

    @staticmethod
    async def get_outcome_plan() -> OutcomePlanModel:
        """
        Get the first result of OutcomePlan by its id
        @param target_id: The id of the OutcomePlan data
        @return: OutcomePlan object
        """
        with get_session() as session:
            outcome_plan = session.query(func.sum(OutcomePlanModel.amount).label("amount")).all()

        return outcome_plan

    @staticmethod
    async def get_last_outcome_plan(data_date:date) -> OutcomePlanModel:
        """
        Get the first result of OutcomePlan by its id
        @param target_id: The id of the OutcomePlan data
        @return: OutcomePlan object
        """
        with get_session() as session:
            outcome_plan = session.query(func.sum(OutcomePlanModel.amount).label("amount")
            ).filter(OutcomePlanModel.date_created<data_date).all()

        return outcome_plan

    
    @staticmethod
    async def get_specific_latest_outcome_plan(keyword:str,outcome_plan_category:int) -> OutcomePlanModel:
        """
        Get the first result of OutcomePlan by its outcome_plan_category id and depend on the keyword
        @param target_id: The id of the OutcomePlan data
        @return: OutcomePlan object
        """
        with get_session() as session:
            outcome_plan = session.query(OutcomePlanModel).options(joinedload(OutcomePlanModel.outcome_plan_category), joinedload(OutcomePlanModel.outcome_plan_category)
            ).filter(OutcomePlanModel.outcome_plan_category==outcome_plan_category,func.lower(OutcomePlanModel.description.like(keyword))
                ).order_by(OutcomePlanModel.date_created.desc()).first()

        return outcome_plan
  
    @staticmethod
    async def get_daily_outcome_plan(target_date: date) -> OutcomePlanModel:
        """
        Get the first result of OutcomePlan by its id
        @param target_id: The id of the OutcomePlan data
        @return: OutcomePlan object
        """
        with get_session() as session:
            outcome_plan = session.query(OutcomePlanModel).options(joinedload(OutcomePlanModel.outcome_plan_category), joinedload(OutcomePlanModel.outcome_plan_category)
            ).filter_by(date_created=target_date).all()

        return outcome_plan
    
    @staticmethod
    async def get_monthly_outcome_plan(first_date: date, last_date: date) -> OutcomePlanModel:
        """
        Get the first result of OutcomePlan by its id
        @param target_id: The id of the OutcomePlan data
        @return: OutcomePlan object
        """
        with get_session() as session:
            outcome_plan = session.query(OutcomePlanModel).options(joinedload(OutcomePlanModel.outcome_plan_category), joinedload(OutcomePlanModel.outcome_plan_category)
            ).filter(OutcomePlanModel.date_created>=first_date,OutcomePlanModel.date_created<=last_date).order_by(OutcomePlanModel.date_created).all()

        return outcome_plan

    @staticmethod
    async def get_group_outcome_plan() -> List[OutcomePlanModel]:
        """
        Get all result of OutcomePlan data
        @return: List of OutcomePlan object
        """
        with get_session() as session:
            income = session.query(
                func.sum(OutcomePlanModel.amount).label("amount"),
                OutcomePlanCategoryModel.name.label("name")).join(
                    OutcomePlanCategoryModel).group_by(
                            OutcomePlanCategoryModel.name
            ).order_by(OutcomePlanCategoryModel.name).all()
        return income

    @staticmethod
    async def get_monthly_total(first_date: date, last_date: date) -> OutcomePlanModel:
        """
        Get the first result of OutcomePlan by its id
        @param target_id: The id of the OutcomePlan data
        @return: OutcomePlan object
        """
        with get_session() as session:
            outcome_plan = session.query(func.sum(OutcomePlanModel.amount).label("amount")).filter(
                OutcomePlanModel.date_created>=first_date,OutcomePlanModel.date_created<=last_date).all()

        return outcome_plan
    
    @staticmethod
    async def get_all() -> List[OutcomePlanModel]:
        """
        Get all result of OutcomePlan data
        @return: List of OutcomePlan object
        """
        with get_session() as session:
            outcome_plan = session.query(OutcomePlanModel).all()
        return outcome_plan

    @staticmethod
    async def add(user_id:str, outcome_plan_category_id:int,description:str, amount:int, quantity:int, date_spend:date) -> OutcomePlanModel:
        """
        Create OutcomePlan object and add it to the database
        @param last_layer: OutcomePlan last_layer
        @param last_room: OutcomePlan last_room
        @return: OutcomePlan object
        """
        with get_session() as session:
            outcome_plan = OutcomePlanModel(user_id=user_id,outcome_plan_category_id=outcome_plan_category_id,description=description, amount=amount,quantity=quantity,date_spend=date_spend)
            session.add(outcome_plan)
            session.commit()
            session.flush()
            session.refresh(outcome_plan)

            return outcome_plan
    
    @staticmethod
    async def update_by_id(target_id: int, new_obj:OutcomePlanModel) -> OutcomePlanModel:
        """
        Update OutcomePlan object that have the specific id
        @param taget_id: OutcomePlan id
        @param new_obj: OutcomePlan OutcomePlan new set of data
        @return: OutcomePlan object
        """
        with get_session() as sess:
            sess.query(OutcomePlanModel).filter_by(id=int(target_id)).update(
                    {
                        OutcomePlanModel.outcome_plan_category_id: new_obj.outcome_plan_category_id,
                        OutcomePlanModel.description : new_obj.description,
                        OutcomePlanModel.amount: new_obj.amount,
                        OutcomePlanModel.quantity: new_obj.quantity,
                        OutcomePlanModel.date_spend: new_obj.date_spend
                        
                    }
                )
            sess.commit()
        return new_obj
   
    @staticmethod
    async def delete_by_id(target_id: int):
        """
        Delete OutcomePlan object that have the specific id
        @param taget_id: OutcomePlan id
        """
        try:
            with get_session() as sess:
            
                try:
                    sess.query(OutcomePlanModel).filter_by(id=int(target_id)).delete()
                    sess.commit()
                    sess.flush()
                    
                except Exception as e:
                    sess.rollback()
                    Debug.msg("OutcomePlanController|delete_by_id", "Failed to Delete {}".format(e), DebugLevel.ERROR)
                    
        except Exception as e:
            Debug.msg("OutcomePlanController|delete_by_id", "Exception Raised {}".format(e), DebugLevel.ERROR)
