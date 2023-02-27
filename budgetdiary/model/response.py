from typing import Optional, Any

from pydantic import BaseModel


class BaseResponse(BaseModel):
	status: str
	content: Optional[Any] = None