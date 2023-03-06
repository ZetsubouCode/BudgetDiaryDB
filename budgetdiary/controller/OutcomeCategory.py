from typing import List
from __database import get_session
from model.database import OutcomeCategory as OutcomeCategoryModel
from utils import Debug, DebugLevel

class OutcomeCategory:
    @staticmethod
    async def get_by_id(target_id: int) -> OutcomeCategoryModel:
        """
        Get the first result of OutcomeCategory by its id
        @param target_id: The id of the OutcomeCategory data
        @return: OutcomeCategory object
        """
        with get_session() as session:
            OutcomeCategory = session.query(OutcomeCategoryModel).filter_by(id=target_id).first()

        return OutcomeCategory
    
    @staticmethod
    def get_all() -> List[OutcomeCategoryModel]:
        """
        Get all result of OutcomeCategory data
        @return: List of OutcomeCategory object
        """
        with get_session() as session:
            OutcomeCategory = session.query(OutcomeCategoryModel).all()
        return OutcomeCategory

    @staticmethod
    async def add(name:str,emoticon:str)-> OutcomeCategoryModel:
        """
        Create OutcomeCategory object and add it to the database
        @param name: The name of the OutcomeCategory
        @param emoticon: The emoticon of the OutcomeCategory
        @return: OutcomeCategory object
        """
        with get_session() as session:
            OutcomeCategory = OutcomeCategoryModel(name=name,emoticon=emoticon)
            session.add(OutcomeCategory)
            session.commit()
            session.flush()
            session.refresh(OutcomeCategory)

            return OutcomeCategory
    
    @staticmethod
    async def update_by_id(target_id: int, new_obj:OutcomeCategoryModel) -> OutcomeCategoryModel:
        """
        Update OutcomeCategory object that have the specific id
        @param taget_id: OutcomeCategory id
        @param new_obj: OutcomeCategory OutcomeCategory new set of data
        @return: OutcomeCategory object
        """
        with get_session() as sess:
            sess.query(OutcomeCategoryModel).filter_by(id=int(target_id)).update(
                    {
                        OutcomeCategoryModel.name: new_obj.name,
                        OutcomeCategoryModel.emoticon: new_obj.emoticon
                        
                    }
                )
            sess.commit()
        return new_obj
   
    @staticmethod
    async def delete_by_id(target_id: int):
        """
        Delete OutcomeCategory object that have the specific id
        @param taget_id: OutcomeCategory id
        """
        try:
            with get_session() as sess:
            
                try:
                    sess.query(OutcomeCategoryModel).filter_by(id=int(target_id)).delete()
                    sess.commit()
                    sess.flush()
                    
                except Exception as e:
                    sess.rollback()
                    Debug.msg("OutcomeCategoryController|delete_by_id", "Failed to Delete {}".format(e), DebugLevel.WARNING)
                    
        except Exception as e:
            Debug.msg("OutcomeCategoryController|delete_by_id", "Exception Raised {}".format(e), DebugLevel.ERROR)
