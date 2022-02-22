import tkinter
import csv
import os
import stat
import time
import configparser
from parse import *

# 파이선을 이용해 CSV파일들의 값을 읽고 Map으로 저장해 정렬한다음 config의 tag.ini에 저장하는 
# 이떄 tag.ini에 존재하는 기존 값들도 읽고 Map에 저장한다. 따라서 csv에서 값을 읽어올때 중복되는 사항을 방지하고 csv에선 제거되었어도 해당하는 태그를 그대로 유지하도록 한다.

# 중복 키를 list로 해결하기 위한 방법
class MultiOrderedDict(dict):
    def __setitem__(self, key, value):
        if isinstance(value, list) and key in self:
            self[key].extend(value)
        else:
            super().__setitem__(key, value)
# 여기가까지 configparser Setting

def GenetateTags():
    text.insert("current" ,"GenetateTags Start!\n")
    #configparser 초기화
    config = configparser.RawConfigParser(dict_type=MultiOrderedDict, strict=False)

    # ini 파일 위치 초기화.
    config_directorypath = './'
    targetini = 'DefaultGameplayTags.ini'
    sectionname = '/Script/GameplayTags.GameplayTagsSettings'
    tagname = '+GameplayTagList'
    redirecttagname = '+GameplayTagRedirects'

    # csv 파일 위치 초기화
    csv_directorypath = "../Content/K2/Table/"
    file_list = os.listdir(csv_directorypath)
    file_list = [file for file in file_list if file.endswith('.csv')]
    text.insert("current" , "Find csv Files : \n")
    text.insert("current" , str(file_list)+"\n")


    # ini 값 읽어오기
    text.insert("current" ,"Read " + targetini + "\n")
    taglist = list()
    redirecttaglist = list()

    config.read(config_directorypath + targetini)

    try:
        parsedarray = config[sectionname][tagname]
        while(1):
            parsedarray = parse("{}Tag=\"{}\"{}", parsedarray)
            if parsedarray:
                taglist.append(parsedarray[1])
                parsedarray = parsedarray[2]
            else:
                break
    except:
        text.insert("current" ,"Warnning : "+tagname + " NotFound.\n")

    try:
        parsedarray = config[sectionname][redirecttagname]
        #splitstrings = parsedarray.split('\n')
        #splitstrings = parsedarray
        #for newstring in splitstrings:
        #    redirecttaglist.append(newstring)
        while(1):
            parsedarray = parse("{}NewTagName=\"{}\"{}", parsedarray)
            if parsedarray:
                print(parsedarray[1])
                taglist.append(parsedarray[1])
                parsedarray = parsedarray[2]
                print(parsedarray)
            else:
                break
    except:
        text.insert("current" ,"Warnning : "+redirecttagname + " NotFound.\n")

    text.insert("current" ,"Done\n")

    ## 기존 ini중에 제외할 태그를 선별한다.
    #text.insert("current" ,"Exclusion list processing.\n")
    #excludlist_str = inputbox.get("1.0",tkinter.END).strip("\n")
    #if excludlist_str:
    #    excludlist = excludlist_str.split(" ")
    #    excludlist.append("\"")
    #    excludlist.append("TagName")
    #    excludlist.append("\(")
    #    excludlist.append("\)")
    #    str_match = list()
    #    #text.insert("current" , str(taglist) + "\n")
    #    for excludtag in excludlist:
    #        str_match = [i for i in range(len(taglist)) if excludtag in taglist[i]]
    #        text.insert("current" , excludtag + "\n")
    #        if str_match:
    #            str_match.reverse()
    #            for index in str_match:
    #                taglist.pop(index)
    #            text.insert("current" , "Removed :" + str(len(str_match)) + "\n")
    #        else:
    #            text.insert("current" , "Not Found.\n")
    #    #text.insert("current" , taglist + "\n")

    # 모든 csv에 태그값 1번째 라인을 읽고 '.'이 있는 항목만 taglist에 저장
    text.insert("current" ,"Read csv Files\n")
    # 색인된 파일들 중 하나
    for csv_file in file_list: 
        fs = open(csv_directorypath + csv_file)
        csvfile = csv.reader(fs)
        # 모든 행중에
        tagcolumn = list()
        for csvrow in csvfile:
            # 첫번째 행일 경우에 tag column을 찾고 저장한다.
            if(csvrow[0].isdigit() == False):
                for i, value in enumerate(csvrow):
                    if value.find("Tag") != -1:
                        tagcolumn.append(i)
            # 이외의 경우엔 tagcolumn 에 해당하는 열의 값을 taglist에 저장한다.
            else:
                if tagcolumn:
                    for targetcolumn in tagcolumn:
                        taglist.append(csvrow[targetcolumn])
                else:
                    text.insert("current" , "Warnning : "+ csv_file +"Tag NotFound!!\n")
        if tagcolumn:
            text.insert("current" , csv_file + " TagFound :"+str(tagcolumn) + "\n")
        fs.close()
    text.insert("current" ,"Done\n")


    # taglist값을 중복 제거 후 정렬.
    text.insert("current" ,"Sort List of Tags\n")
    newset = set(taglist)
    taglist = list(newset)

    taglist.sort()
    text.insert("current" ,"Done\n")

    # 기존 ini중에 제외할 태그를 선별한다.
    text.insert("current" ,"Exclusion list processing.\n")
    excludlist_str = inputbox.get("1.0",tkinter.END).strip("\n")
    excludlist=list()
    if excludlist_str:
        excludlist = excludlist_str.split(" ")
    excludlist.append("\"")
    excludlist.append("TagName")
    excludlist.append("\(")
    excludlist.append("\)")
    str_match = list()
    #text.insert("current" , str(taglist) + "\n")
    for excludtag in excludlist:
        str_match = [i for i in range(len(taglist)) if excludtag in taglist[i]]
        text.insert("current" , excludtag + "\n")
        if str_match:
            str_match.reverse()
            for index in str_match:
                taglist.pop(index)
            text.insert("current" , "Removed :" + str(len(str_match)) + "\n")
        else:
            text.insert("current" , "Not Included.\n")
    #text.insert("current" , taglist + "\n")

    # ini 파일 수정 후 저장.
    text.insert("current" ,"Edit "+targetini+"\n")
    os.chmod( config_directorypath + targetini, stat.S_IWRITE )

    fs = open(config_directorypath + targetini, "w")
    print(fs)
    config.remove_option(sectionname, redirecttagname)
    config.remove_option(sectionname, tagname)
    config.write(fs)

    #for tag in redirecttaglist:
    #    if tag != None:
    #        fs.write(redirecttagname+"="+tag+"\n")

    for tag in taglist:
        if tag != None:
            fs.write(tagname+"=(Tag=\""+tag+"\",DevComment=\"\")\n")
    fs.close()
    text.insert("current" ,"Done\n")
    text.insert("current" ,"GenerateTags Complete!\n\n")
    
# GUI
window = tkinter.Tk()
window.title("tag_generator")
window.geometry("640x400")
window.resizable(False, False)

text=tkinter.Text(window, width=100, height=10, fg="black", relief="solid", yscrollcommand='Any')
text.insert(tkinter.CURRENT, "Content/K2/Table/에 있는 csv 파일들의 Tag들을 모아서 DefaultGameplayTags.ini에 생성하는 프로그램.\n")
text.pack(side="top", fill="both", expand=True)

frame=tkinter.Frame(width=100, height=1, relief="solid", bd=1)
frame.pack(fill="both")

message01=tkinter.Message(frame, text="ex) Damage Character.PlayerCharacter ...", width=500)
message01.pack(side="bottom")

message02=tkinter.Message(frame, text="Exclusion list :", width=100)
message02.pack(side="left")
inputbox=tkinter.Text(frame, width=100, height=1, fg="black", relief="solid", yscrollcommand='Any')
inputbox.pack(side="right")

button = tkinter.Button(window, overrelief="solid", width=15, padx=5, pady=5, command=GenetateTags, highlightthickness=1, text="Generate!", relief="solid", bd=1)
button.pack(side="bottom")

window.mainloop()