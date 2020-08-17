import os
import json
import module.OF

def String_Flag(flag):
    if flag & module.OF.MESSAGES:
        return "Messages"
    elif flag & module.OF.HIGHLIGHTS:
        return "Highlights"
    elif flag & module.OF.PICTURES:
        return "Images"
    elif flag & module.OF.VIDEOS:
        return "Videos"
    elif flag & module.OF.STORIES:
        return "Stories"
    elif flag & module.OF.ARCHIVED:
        return "Archived"
    elif flag & module.OF.AUDIO:
        return "Audio"

def File_Size_Str(size):
    unit = ["KB", "MB", "GB", "TB"]
    count = -1
    if size < 1024:
        return str(size) + "B"
    else:
        while size >= 1024:
            size /= 1024
            count += 1
    return str('%.2f' % size) + unit[count]

def Link_Size(links):
    size = 0
    for link in links:
        size += link["size"]
    return size

def Write_Through_File(onlyfans):
    file_name = "onlyfans.continue"
    names = onlyfans.return_user_array()
    links = onlyfans.return_links()
    try:
        with open(file_name, "w") as write_through:
            for x in range (0, len(names)):
                write_through.write(names[x]["username"])
                if x != len(names) - 1:
                    write_through.write(",")
            write_through.write("\n")
            for link in links:
                json.dump(link, write_through)
                write_through.write("\n")      
    except IOError:
        pass