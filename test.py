import py7zr
import os 

archive = py7zr.SevenZipFile('artifacts\\similarity.7z', mode='r')
archive.extractall(path=os.getcwd())
archive.close()