"""
author: Hanbing Guo
data: 2020/3/12
"""

import kNN
import zipfile

zf = zipfile.ZipFile("./digits.zip")
zf.extractall(path='./')
zf.close()

kNN.handwritingClassTest()

