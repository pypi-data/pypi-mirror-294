from pydantic import BaseModel
from typing import Dict, Optional, List, Callable

class LoggerConfig(BaseModel):
    service:str
    request_id:str
    
class LogHttp(BaseModel):
    url: str
    useragent: str
    method: str
    host: str

class LogMask(BaseModel):
    path: str
    maskFunction: Optional[Callable[[str], str]] = None

class MaskList(BaseModel):
    masks: Optional[List[LogMask]] = None
        
class LogUser(BaseModel):
    id:str
    status:str
    phone:str
    client:str
    contact:str
    email:str
    groups:str
    scope:str
    type:str