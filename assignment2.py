#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import os, os.path, sys
from mutagen.easyid3 import EasyID3
import shutil 

def find_mp3s(path):
        
    absolute_list = []
    if not os.path.exists(path):
            raise ValueError ('Wrong path entered !!')
    if type(path)is not str:
            raise TypeError ('Path is not a string')
    for dir_, subdir_list, file_list in os.walk(path):
            for file_name in file_list:
                    #only paths ending with .mp3 are needed
                    if (file_name.endswith ('.mp3')):
                            #get the absolute path of the direcotry joined witht he filename
                            absolute_path = os.path.abspath(os.path.join(dir_,file_name))
                            #add all the absolute paths to a list
                            absolute_list.append(absolute_path)
    return absolute_list

def load_id3(path):
        
    if not os.path.exists(path):
            raise ValueError('Wrong path entered')
    if type(path)is not str:
            raise TypeError ('Path is not a string')
    try:
            #ID3 initializer take a path:
            id3 = EasyID3(path)
    except:
            raise ValueError ('ID3 initialization fails')
    return id3

def make_filename(id3,tags):
        
    #check if id3 is an instance of EasyID3
    if not isinstance (id3, EasyID3):
        raise TypeError('Id3 is not instance of EasyID3')
    #check if the artist or title are missing
    try:
        id3['artist']
        id3['title']
    except:
        raise ValueError ('The file is missing required data')
    filename = ''
    #check if id3['album'] is None or empty string and replace it if so
    for tag in tags:
        try:
            id3[tag]
        except:
            id3[tag] = 'Unknown'
        info = str(id3[tag][0])
        filename += info + ' - '
    #return string with extracted id3 and add .mp3 to it
    return filename.rstrip(' - ') + '.mp3'

def rename_mp3(input_mp3_path, output_mp3_path, tags):
    #check if the path exists and ends with .mp3
    if os.path.exists(input_mp3_path):
        if not input_mp3_path.endswith('.mp3'):
            raise ValueError ('Path is not mp3 path')
    else:
        raise ValueError ('Invalid Path')

    if not os.path.exists(output_mp3_path):
        raise ValueError ('Invalid Path')

    try:
        id3_tags = load_id3(input_mp3_path)
        file_name = make_filename(id3_tags, tags)
        joint = os.path.join(output_mp3_path,file_name)
        shutil.copyfile(input_mp3_path, os.path.abspath(joint))
            
    except IOError:
        raise ValueError ('Folder/directory does not exist')

def main():
    #check if the directories are valid
    try:
        x = os.path.isdir(sys.argv[1])
        if x == False:
            raise ValueError ('Invalid Input Path')
    except:    
        raise ValueError ('Invalid Input Path')

    try:
        x = os.path.isdir(sys.argv[2])
        if x == False:
            raise ValueError ('Invalid Output Path')
    except:    
        raise ValueError ('Invalid Output Path')

    try:
        x = os.path.isdir(sys.argv[2])
        if x == False:
            raise ValueError ('Invalid Output Path') 
    except:
        raise ValueError ('Invalid Path')
    #check if 3rd arguement is valid
    try:
        x = sys.argv[3].endswith('.mp3')
        if x == False:
                raise Exception ('String does not end with .mp3')
        arguement3 = sys.argv[3].split('.mp3')
        tags = arguement3[0].split(' - ')
        #check if the elements are valid keys
    #if 3rd arguement doesn't exist replace it with tags = ['artist','album','title']
    except:
        tags = ['artist','album','title']

    valid_keys = EasyID3.valid_keys.keys()
    for tag in tags:
        if(tag not in valid_keys):
            raise ValueError (tag + ' is not a valid ID3 key')
            
    path_mp3_list = find_mp3s(sys.argv[1])
    for path_mp3 in path_mp3_list:
        try:
            rename_mp3(path_mp3,sys.argv[2],tags)
        except Exception as error:
            print path_mp3 , 'cannot be copied because: ' , error

main() 
