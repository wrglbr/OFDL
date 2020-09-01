from __future__ import print_function, unicode_literals
import os
import json
import time
import threading
import module.OF
import module.BC
import module.Utilities
from module.OF import Onlyfans
from module.BC import BoolClass
from module.Utilities import *
from PyInquirer import prompt

class MainCommand:
    def __init__(self):
        self.onlyfans = {}
        self.Sub_List = {}
        self.Chosen_List = {}
        self.RedownloadBool = BoolClass()
        self.RedownloadBool.set(False)
        self.sort = False

    def PromptConfig(self):
        questions = [
            {
                'type': 'input',
                'name': 'cookie',
                'message': 'Input Cookie: ',
            },
            {
                'type': 'input',
                'name': 'user-agent',
                'message': 'Input User Agent: ',
            }
        ]

        print("No config was loaded. Please generate a new config file.")

        answers = prompt(questions)

        data = {}
        data["app-token"] = "33d57ade8c02dbc5a333db99ff9ae26a"
        cookie = answers["cookie"]
        user_agent = answers["user-agent"]
        if cookie is not None:
            data["cookie"] = cookie
        if user_agent is not None:
            data["user-agent"] = user_agent
        try:
            f = open("config.json", "w")
            json.dump(data, f)
            f.close()
        except IOError:
            pass

    def SubDown(self, subname):
        print("Please choose media types for " + subname)
        if subname in self.Chosen_List:
            subdownschosen = self.Chosen_List[subname]
        else:
            subdownschosen = ""

        choices = []

        if "M" in subdownschosen:
            choices.append({'name': 'Messages', 'checked': True})
        else:
            choices.append({'name': 'Messages'})

        if "P" in subdownschosen:
            choices.append({'name': 'Pictures', 'checked': True})
        else:
            choices.append({'name': 'Pictures'})

        if "V" in subdownschosen:
            choices.append({'name': 'Videos', 'checked': True})
        else:
            choices.append({'name': 'Videos'})

        if "H" in subdownschosen:
            choices.append({'name': 'Highlights', 'checked': True})
        else:
            choices.append({'name': 'Highlights'})

        if "Ar" in subdownschosen:
            choices.append({'name': 'Archived', 'checked': True})
        else:
            choices.append({'name': 'Archived'})

        if "Au" in subdownschosen:
            choices.append({'name': 'Audio', 'checked': True})
        else:
            choices.append({'name': 'Audio'})

        questions = [
            {
                'type': 'checkbox',
                'message': 'Select media types',
                'name': 'mtypes',
                'choices': choices
            }
        ]

        answers = prompt(questions)

        if len(answers["mtypes"]) == 0:
            self.Chosen_List.pop(subname, None)
        else:
            self.Chosen_List[subname] = ""
            if 'Messages' in answers["mtypes"]:
                self.Chosen_List[subname] += "M"
            if 'Pictures' in answers["mtypes"]:
                self.Chosen_List[subname] += "P"
            if 'Videos' in answers["mtypes"]:
                self.Chosen_List[subname] += "V"
            if 'Highlights' in answers["mtypes"]:
                self.Chosen_List[subname] += "H"
            if 'Archived' in answers["mtypes"]:
                self.Chosen_List[subname] += "Ar"
            if 'Audio' in answers["mtypes"]:
                self.Chosen_List[subname] += "Au"

        print('\n')

        self.Main()

    def Main(self):
        choices = sorted(self.Sub_List)
        message = "Select a subscription"
        
        if len(self.Chosen_List) > 0:
            choices.append('Retrieve Links')
            message += ", 'Retrieve Links'"

        if len(self.onlyfans.links) > 0:
            choices.append('Download Links')
            message += ", 'Download Links'"

        if self.RedownloadBool.get():
            choices.append('Toggle Re-Download Off (Is On)')
        else:
            choices.append('Toggle Re-Download On (Is Off)')
        choices.append('Quit')
        message += ", choose if you want to re-download files or 'Quit'"

        questions = [
            {
                'type': 'list',
                'name': 'sub',
                'message': message,
                'choices': choices
            }
        ]

        ChosenString = "Chosen downloads: "

        if len(self.Chosen_List) == 0:
            ChosenString += "None"
        else:
            for key, value in self.Chosen_List.items():
                if str(value) == "MPVHArAu":
                    ChosenString += str(key) + ": All, "
                else:
                    ChosenString += str(key) + ": " + str(value) + ", "
            ChosenString = ChosenString[:-2]

        print(ChosenString)
        answers = prompt(questions)

        print('\n')

        if answers["sub"] == "Retrieve Links":
            self.Get_Links_T()
        elif answers["sub"] == "Download Links":
            self.Download_Files_T()
        elif answers["sub"] == "Toggle Re-Download Off (Is On)" or answers["sub"] == "Toggle Re-Download On (Is Off)":
            self.RedownloadBool.set(not self.RedownloadBool.get())
            self.Main()
        elif answers["sub"] == "Quit":
            print("Goodbye!")
        else:
            self.SubDown(answers["sub"])
    

    #Main Method
    def StartCli(self):
        """starts OFDL via cli"""
        print("Loading... Please wait.")
        self.onlyfans = Onlyfans()
        self.onlyfans.load_config()

        if len(self.onlyfans.config) == 0:
            self.PromptConfig()
            self.onlyfans.load_config()

        self.onlyfans.get_subscriptions()
        self.Sub_List = self.onlyfans.return_active_subs()

        print("Loading finished.")

        print('\n')

        self.Main()


    #Methods
    def Get_Links_T(self):
        print("Retrieving Links... Please wait.")
        threading.Thread(target=self.Get_Links).start()

    def Download_Files_T(self):
        threading.Thread(target=self.Download_Files).start()

    def Get_Links(self):
        users = []
        index = 0

        print('Status: Collecting Links ...', end='\r')

        self.onlyfans.reset_download_size()
        self.onlyfans.clear_links()
        self.onlyfans.clear_array()

        for key, value in self.Chosen_List.items():
            flag = 0
            if "M" in value:
                flag |= module.OF.MESSAGES

            if "P" in value:
                flag |= module.OF.PICTURES
                
            if "V" in value:
                flag |= module.OF.VIDEOS
                
            if "H" in value:
                flag |= module.OF.HIGHLIGHTS
                
            if "Ar" in value:
                flag |= module.OF.ARCHIVED
                
            if "Au" in value:
                flag |= module.OF.AUDIO

            tmp = {key : flag}
            users.append(tmp)
                
        for u in users:
            for key, value in u.items():
                dict_return = self.onlyfans.get_user_info(key)
                if dict_return is None:
                    continue
                self.onlyfans.get_links(self, dict_return, value, index)
                index += 1
                
        links = self.onlyfans.return_links()
        if len(links) > 0:
            print('\nStatus: Done.')
            print('\n')
            self.Display_Info(links)
        else:
            print('\nStatus: Done. No downloadable links were found.')
            print('\n')

        self.Main()

    def Display_Info(self, links):
        total_size = 0
        user_size = 0
        file_count = 0
        type_file = {"Messages" : 0, "Highlights" : 0, "Images" : 0, "Videos" : 0, "Stories" : 0, "Archived" : 0, "Audio" : 0}
        infotext = ""
        
        current_user = links[0]["index"]
        flag = 0
        for file in links:
            if file["index"] == current_user:
                total_size += file["size"]
                user_size += file["size"]
                file_count += 1
                flag = file["flag"]
                type_file[String_Flag(flag)] += 1
            else:
                user_name = self.onlyfans.subscript_array(current_user) + ": \n"
                infotext += user_name
                for key, value in type_file.items():
                    infotext += "   " + key + ": " + str(value) + "\n"
                    type_file[key] = 0
                infotext += "   Total size: " + File_Size_Str(user_size) + "\n"
                
                user_size = 0
                file_count = 1
                current_user = file["index"]
                user_size += file["size"]
                total_size += file["size"]
                flag = file["flag"]
                type_file[String_Flag(flag)] += 1

        user_name = self.onlyfans.subscript_array(current_user) + ": \n"
        infotext += user_name

        for key, value in type_file.items():
            infotext += "   " + key + ": " + str(value) + "\n"
            type_file[key] = 0

        infotext += "   Total size: " + File_Size_Str(user_size) + "\n"
        infotext += "\n\n"
        infotext += "Files to be downloaded: " + str(len(links)) + "\n"
        infotext += "Download Size: " + File_Size_Str(total_size) + "\n"

        print(infotext)

    def Download_Files(self):
        questions = [ { 'type': 'confirm', 'message': 'Do you want to continue?', 'name': 'continue', 'default': True } ]
        names = []
        files = []
        if len(self.onlyfans.return_links()) > 0:
            answer = prompt(questions)
            print('\n')
            if answer["continue"] != False:
                names = self.onlyfans.return_user_array().copy()
                if self.sort == True:
                    files = self.onlyfans.filter_list.copy()
                    self.onlyfans.all_files_size = self.Link_Size(files)
                else:
                    files = self.onlyfans.return_links().copy()
                file_len = len(files)
                print("Status: Downloading Files...")
                
                current_user = files[0]["index"]
                user_folder = self.onlyfans.subscript_array(current_user)
                self.onlyfans.create_dir(user_folder)
                
                for file in files:
                    print("Files left to download: " + str(file_len) + "     ", end='\r')
                    if file["index"] == current_user:
                        self.onlyfans.download(self, user_folder, file)
                    else:
                        current_user = file["index"]
                        user_folder = self.onlyfans.subscript_array(current_user)
                        self.onlyfans.create_dir(user_folder)
                        self.onlyfans.download(self, user_folder, file)
                    file_len -= 1
                    self.onlyfans.insert_database(names[current_user], file)
                    #self.write_through_file()
                print("Files left to download: " + str(file_len) + "     ")
                print('\nStatus: Done.')
        else:
            print('\nStatus: Done.')
        
        print('\n')
        #os.remove("onlyfans.continue")
        self.onlyfans.clear_links()
        self.onlyfans.clear_array()
        self.onlyfans.clear_filter()
        self.Chosen_List = {}

        self.Main()