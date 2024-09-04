from io import TextIOWrapper
from typing import Optional, Union

File = tuple[Optional[str], Union[bytes, str, TextIOWrapper]]
UploadFile = dict[str, File]
