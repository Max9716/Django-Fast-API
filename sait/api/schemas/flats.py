from pydantic import BaseModel
from typing import Optional

class FlatsRequest(BaseModel):
    id_complex: Optional[str] = 20
