# -*- coding: utf-8 -*-
# # ONS Deaths registered weekly in England and Wales, provisional 

# +
import glob

py_files = [i for i in glob.glob('*.{}'.format('py'))]

for i in py_files:
    file = "'" + i + "'"
    if file.startswith("'main") == True:
        continue
    %run $file
