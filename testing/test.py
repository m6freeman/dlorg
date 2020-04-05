import os
import time
import json
import shutil
import re
import hashlib
from pathlib import Path, PurePath

BUFF_SIZE = 65536

testFolder = Path.home() / "Downloads/test"
files = (x for x in testFolder.iterdir() if x.is_file())
md5 = hashlib.md5()
for file in files:
    with file.open() as f:
        while True:
            data = f.read(BUFF_SIZE)
            if not data:
                break
            md5.update(data)
        f.close()
print(md5.hexdigest())
