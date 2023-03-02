import os,shutil
import sys
from pathlib import Path
import re

#  File Mask List
IMAGES = ('JPEG', 'PNG', 'JPG', 'SVG') 
DOCUMENTS = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX') 
VIDEOS = ('AVI', 'MP4', 'MOV', 'MKV') 
SOUNDS = ('MP3', 'OGG', 'WAV', 'AMR') 
ARCHIVES = ('ZIP', 'GZ', 'TAR') 

#  Default Folder List
FOLDERS = ('/images', '/videos','/documents','/archives','/sounds', '/others') 

# translation 
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()    


def translate(name):
    return name.translate(TRANS)

# normalise name
def normalise(name):
    rep = re.compile('[^a-zA-Zа-яА-я,\d]')
    name = rep.sub('_', name)
    return name

# Create default folders
def create_def_folder(current):
    for d in FOLDERS:
        def_dir = current + d
        
        isExist = os.path.exists(def_dir) 
        if not isExist:
            # Create a new directory because it does not exist
            os.makedirs(def_dir) 

# Sort function    
def sort_file(file_dir, file_mask, curr_path, dest_path, f_m_c:bool):
    new_fn = []
    
    for file in file_dir:

        dest = ''

        if f_m_c == True:
            
            for ex in file_mask:
                if file.endswith(ex.casefold()):
                    dest = curr_path + dest_path
                    new_fn = str(file).split('.')
                
                    os.rename(curr_path + '\\' + file,curr_path + '\\' + translate(normalise(new_fn[0]))+'.'+ex.lower()) 
                    shutil.move(curr_path + '\\' + translate(normalise(new_fn[0]))+'.'+ex.lower() , dest)
                    break
        else:
            dest = curr_path + dest_path
            if os.path.isfile(curr_path + '\\' + file ):
                shutil.move(curr_path + '\\' + file , dest) 

# main           
def main():
    files = None
    path_f = None
    
    try:
        
        path_f = sys.argv[1]
        if len(path_f) != 0:
            
            AppPath = sys.path[0]
            current = AppPath + path_f
            
            files=os.listdir(current)
            print(files)
            
            print("Create folders...")
            create_def_folder(current)
            print(os.listdir(current))
            
            print("Sorting the files...")
            
            #Images
            sort_file(files, IMAGES, current, FOLDERS[0],True) 
            files_s = os.listdir(current + FOLDERS[0])
            print(FOLDERS[0] + ' -->' , files_s)  
            
            #Videos
            sort_file(files, VIDEOS, current, FOLDERS[1],True)
            files_s = os.listdir(current + FOLDERS[1])
            print(FOLDERS[1] + ' -->' , files_s)    
            
            #doc
            sort_file(files, DOCUMENTS, current, FOLDERS[2],True)
            files_s = os.listdir(current + FOLDERS[2])
            print(FOLDERS[2] + ' -->' , files_s)    
            
            #arhive
            sort_file(files, ARCHIVES, current, FOLDERS[3],True)
            files_s = os.listdir(current + FOLDERS[3])
            print(FOLDERS[3] + ' -->' , files_s)    
            
            #sounds
            sort_file(files, SOUNDS, current, FOLDERS[4],True)
            files_s = os.listdir(current + FOLDERS[4])
            print(FOLDERS[4] + ' -->' , files_s)    
            
            #other
            sort_file(files, () , current, FOLDERS[-1], False)
            files_s = os.listdir(current + FOLDERS[-1])
            print(FOLDERS[-1] + ' -->' , files_s)  
            
            print("Sorting Completed...")
            files=os.listdir(current)
            
    except:
        
        print('Path not found: ', path_f)
        print('example: scrypt.py /some_folder ')
        
    finally:
        
        print('Folders: ',files)
		
if __name__ == "__main__":
    main()