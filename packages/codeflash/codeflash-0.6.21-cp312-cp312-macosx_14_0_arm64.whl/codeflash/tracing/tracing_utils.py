from typing import Optional

from pydantic import dataclasses


@dataclasses.dataclass
class FunctionModules:
    function_name: str
    file_name: str
    module_name: str
    class_name: Optional[str] = None
    line_no: Optional[int] = None
