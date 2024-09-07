# we have directly imported file_1 in ../__init__.py ,
# as if file_1 is a direct model under ..('src')
# but the module 'minus' still has attribute file_1 to be found
# i.e., xplus31.src.file_1 == xplus31.src.minus.file_1