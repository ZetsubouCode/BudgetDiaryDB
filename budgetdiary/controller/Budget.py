from typing import List
from __database import get_session
from model.database import Budget as BudgetModel
from utils import Debug, DebugLevel

class Budget:
    @staticmethod
    async def get_by_id(target_id: int) -> BudgetModel:
        """
        Get the first result of Budget by its id
        @param target_id: The id of the Budget data
        @return: Budget object
        """
        with get_session() as session:
            budget = session.query(BudgetModel).filter_by(id=target_id).first()

        return budget
    
    @staticmethod
    def get_all() -> List[BudgetModel]:
        """
        Get all result of Budget data
        @return: List of Budget object
        """
        with get_session() as session:
            budget = session.query(BudgetModel).all()
        return budget

    @staticmethod
    async def add(description:str)-> BudgetModel:
        """
        Create Budget object and add it to the database
        @param last_layer: Budget last_layer
        @param last_room: Budget last_room
        @return: Budget object
        """
        with get_session() as session:
            budget = BudgetModel(description=description)
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
                        BudgetModel.description: new_obj.description,
                        
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