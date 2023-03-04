import os,shutil
import sys
import re

#  key = Default Folder : List = File Mask 

FILE_MASK = {"/images":('JPEG', 'PNG', 'JPG', 'SVG') , 
             "/documents":('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX') ,
             "/videos":('AVI', 'MP4', 'MOV', 'MKV') , 
             "/sounds":('MP3', 'OGG', 'WAV', 'AMR'), 
             "/archives":('ZIP', 'GZ', 'TAR', 'RAR') , 
             "/others":() }



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


# Sort function    
def sort_file(file_dir, file_mask, curr_path, dest_path):
    
    if len(file_mask) != 0:
        f_m_c = True
    else:
        f_m_c = False
        
    new_fn = []
    
    for file in file_dir:
        dest = ''
        if f_m_c == True:
            
            for ex in file_mask:
                if file.endswith(ex.casefold()):
                    dest = curr_path + dest_path
                    new_fn = str(file).split('.')
                    
                    if not os.path.exists(dest) :
                        os.makedirs(dest) 
                        
                    os.rename(curr_path + '\\' + file,curr_path + '\\' + translate(normalise(new_fn[0]))+'.'+ex.lower()) 
                    shutil.move(curr_path + '\\' + translate(normalise(new_fn[0]))+'.'+ex.lower() , dest)
                    break
        else:
            dest = curr_path + dest_path
            if not os.path.exists(dest) :
                os.makedirs(dest) 
           
            if os.path.isfile(curr_path + '\\' + file ):
                shutil.move(curr_path + '\\' + file , dest) 
                
# main           
def main():
    
    files = ''
    path_f = ''
    
    try:
        
        path_f = sys.argv[1]
        
        if len(path_f) != 0:
            
            AppPath = sys.path[0]
            current = AppPath + path_f
            
            files=os.listdir(current)
            print(files)
            
            print("Sorting the files...")
            
            for k, v in FILE_MASK.items():
                sort_file(files, v, current, k) 
            
            print("Sorting Completed...")
            files=os.listdir(current)
            
    except:
        
        print('Path not found : ', path_f)
        print('example: scrypt.py /some_folder ')
        
    finally:
        if len(path_f) != 0:
            for i in os.listdir(current):
                files_s = os.listdir(current + '/' + i)
                print(i , ' -->', files_s)  
		
if __name__ == "__main__":
    main()