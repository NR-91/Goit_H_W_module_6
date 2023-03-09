import shutil
import sys
import re
from pathlib import Path


FILE_MASK = {"images":['*.jpeg', '*.png', '*.jpg', '*.svg'] , 
             "documents":['*.doc', '*.docx', '*.txt', '*.pdf'] ,
             "videos":['*.avi', '*.mp4', '*.mov', '*.mkv'] , 
             "sounds":['*.mp3', '*.ogg', '*.wav', '*.amr'], 
             "archives":['*.zip', '*.gz', '*.tar', '*.rar'] , 
             "others":['*.*'] }

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

def def_folder_list():
    result = []
    for d_f in FILE_MASK.keys():
        result.append(d_f)
    return result


# Sort function    
def sort_file(p):
    for x in p.iterdir():
        if x.is_dir():
            print(x)
            if not x.name in def_folder_list():
                if x.stat().st_size == 0:
                    x.rmdir()
                x.rename(p / normalise(translate(x.name)))
                sort_file(Path.joinpath(p, x.name))
        else:
            
            for k,v in FILE_MASK.items():
                for ex in v:
                    for x in p.glob(ex):
                        
                        files_dir =  p / k
                        if not files_dir.exists():
                            files_dir.mkdir()
                            
                        src_path = Path.joinpath(p, x.name)
                        dst_path = Path.joinpath(files_dir, normalise(translate(x.stem)) + x.suffix)
                        shutil.move(src_path, dst_path) 
                        
                        if k == 'archives':
                            shutil.unpack_archive(dst_path, Path.joinpath(files_dir, normalise(translate(x.stem))))
                          
# main           
def main():
    
    try:
        p = Path('.',sys.argv[1])
        print("Sorting the files...")
        sort_file(p)
        print("Sorting Completed...")   
    except:
        print('Path not found')
        print('example: scrypt.py some_folder ')
        
if __name__ == "__main__":
    main()