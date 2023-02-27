from typing import List
from __database import get_session
from model.database import IncomeCategory as IncomeCategoryModel
from utils import Debug, DebugLevel

class IncomeCategory:
    @staticmethod
    async def get_by_id(target_id: int) -> IncomeCategoryModel:
        """
        Get the first result of IncomeCategory by its id
        @param target_id: The id of the IncomeCategory data
        @return: IncomeCategory object
        """
        with get_session() as session:
            IncomeCategory = session.query(IncomeCategoryModel).filter_by(id=target_id).first()

        return IncomeCategory
    
    @staticmethod
    def get_all() -> List[IncomeCategoryModel]:
        """
        Get all result of IncomeCategory data
        @return: List of IncomeCategory object
        """
        with get_session() as session:
            IncomeCategory = session.query(IncomeCategoryModel).all()
        return IncomeCategory

    @staticmethod
    async def add(name:str,emoticon:str)-> IncomeCategoryModel:
        """
        Create IncomeCategory object and add it to the database
        @param last_layer: IncomeCategory last_layer
        @param last_room: IncomeCategory last_room
        @return: IncomeCategory object
        """
        with get_session() as session:
            IncomeCategory = IncomeCategoryModel(name=name,emoticon=emoticon)
            session.add(IncomeCategory)
            session.commit()
            session.flush()
            session.refresh(IncomeCategory)

            return IncomeCategory
    
    @staticmethod
    async def update_by_id(target_id: int, new_obj:IncomeCategoryModel) -> IncomeCategoryModel:
        """
        Update IncomeCategory object that have the specific id
        @param taget_id: IncomeCategory id
        @param new_obj: IncomeCategory IncomeCategory new set of data
        @return: IncomeCategory object
        """
        with get_session() as sess:
            sess.query(IncomeCategoryModel).filter_by(id=int(target_id)).update(
                    {
                        IncomeCategoryModel.name: new_obj.name,
                    }
                )
            sess.commit()
        return new_obj
   
    @staticmethod
    async def delete_by_id(target_id: int):
        """
        Delete IncomeCategory object that have the specific id
        @param taget_id: IncomeCategory id
        """
        try:
            with get_session() as sess:
            
                try:
                    sess.query(IncomeCategoryModel).filter_by(id=int(target_id)).delete()
                    sess.commit()
                    sess.flush()
                    
                except Exception as e:
                    sess.rollback()
                    Debug.msg("IncomeCategoryController|delete_by_id", "Failed to Delete {}".format(e), DebugLevel.WARNING)
                    
        except Exception as e:
            Debug.msg("IncomeCategoryController|delete_by_id", "Exception Raised {}".format(e), DebugLevel.ERROR)