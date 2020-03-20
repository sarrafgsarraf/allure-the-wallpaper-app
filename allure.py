import ctypes
import time
import os
import requests as requests
import urllib.request as url
from win10toast import ToastNotifier
from infi.systray import SysTrayIcon

toaster = ToastNotifier()


noti = ""
inter = ""
buff = 0
acc = ""
word = ""
directory = 'C:\\Users\\sarra\\Downloads\\wall\\papers\\'
play_list = []
uploaded_by = []
buff_img = 0
interval = 0
keyword = ""
access_key = ""
yes = False
global img_path

def settings():
    global noti
    global inter
    global buff
    global acc
    global word
    global buff_img
    global interval
    global keyword
    global access_key

    noti = input("\n\nDo you want desktop notication for every wallpaper change? y/n?\n    If you dont want to set this hit enter, default is Yes!\n:")
    if noti == "":
        print("Notification set to default of ON!")
        noti = 'y'
    else:
        print("Notification set to ON!") if noti == 'y' else print("Notification set to OFF!")

    inter = input("\n\nAt what interval do you want to change the wallpaper?\n    If in minutes enter: minutes+m eg:5m\n    If in hours enter: hours+h eg:5h\n    If in days enter: days+d eg 2d\n    If you dont want to set this hit enter, default in 60m!\n:")
    if inter == "":
        inter = 60
        print("Change Interval set to default of 1m or 60 seconds!")
    else:
        n = inter
        if n[-1] == 'm':
            inter = int(n[0:-1]) * 60
            print("Change Interval set to " +str(n[0:-1])+ " minutes or " +str(inter)+ " seconds!")
        elif n[-1] == 'h':
            inter = int(n[0:-1]) * 60 * 60
            print("Change Interval set to " +str(n[0:-1])+ " hours or " +str(inter)+ " seconds!")
        elif n[-1] == 'd':
            inter = int(n[0:-1]) * 60 * 60 * 24
            print("Change Interval set to " +str(n[0:-1])+ " days or " +str(inter)+ " seconds!")

    buff = input("\n\nInput your buffer value in digits, remeber it should be 12 or more and less than 30.\n    If you dont want to set this hit enter, default is 12!\n:")
    if buff == "":
        buff = 12
        buff = int(buff)
        print("Buffer set to default of 12 images!")
    else:
        print("Buffer set to default of " +buff+ " images!")
        buff = int(buff)

    acc = input("\n\nEnter your own UnSplash.com Developer Access Key.\n    If you don't want to set this hit enter!\n:")
    if acc == "":
        acc = '6aade448e73df408614baa222e14f9d808eccebd90f20e10f9f1b04a8ced2c9c'
        print("Access Key set to default!")
    else:
        print("Access Key set to " +acc)

    word = input("\n\nEnter the keyword to be used for image searches.\n    If you don't want to set this hit enter!\n:")
    if word == "":
        print("Keyword set to random.")
    else:
        print("Keyword set to " +word)

    buff_img = buff
    interval = inter
    keyword = word
    access_key = acc

    load()


def changeBG(imagePath):
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, imagePath , 0)
    print("changed")
    print(imagePath)
    return

def request():
    req_url = 'https://api.unsplash.com/photos/random?orientation=landscape&query=' + keyword + '&count=' + str(buff_img) + '&client_id=' +access_key
    r = requests.get(req_url)
    data = r.json()
    del play_list[:]
    for img_data in data:
        file_name = str(img_data['id']) + ".jpg"
        img_url = img_data['urls']['raw']
        suffix = '&q=80&fm=jpg&crop=entropy&cs-tinysrgb&w=1920&fit=max'
        img_url = img_url + suffix
        url.urlretrieve(img_url, file_name)
        play_list.append(file_name)
        uploaded_by.append(img_data['user']['name'])

def load():
    request()
    global imagePath
    while True:
        for i,j in zip(play_list,uploaded_by):
            imagePath = directory + "\\" + i
            changeBG(imagePath)
            if noti == 'y': toaster.show_toast("Allure","by " + j + " via Unsplash.com", icon_path="C:\\Users\\sarra\\Downloads\\wall\\app_artwork\\allure.ico")
            try:
                time.sleep(interval)
            except KeyboardInterrupt:
                continue
                print("Reached")
            os.remove(i)
            if play_list.index(i) == buff_img - 1:
                request()
                print("reload")
                break


def start_sys_ico():
    def next_wall(sysTrayIcon):
        raise KeyboardInterrupt

    def setting(sysTrayIcon):
        settings()

    def get_info(sysTrayIcon):
        print("Info sent")

    menu_options = (('Change Now', "C:\\Users\\sarra\\Downloads\\wall\\app_artwork\\next.ico", next_wall),
                    ('Open Settings', "C:\\Users\\sarra\\Downloads\\wall\\app_artwork\\settings.ico", setting),
                    ('Get Photographer Info', "C:\\Users\\sarra\\Downloads\\wall\\app_artwork\\info.ico", get_info))

    sysTrayIcon = SysTrayIcon("C:\\Users\\sarra\\Downloads\\wall\\app_artwork\\allure.ico", "the wallpaper app", menu_options, default_menu_index=0)
    sysTrayIcon.start()

print("""\
              .                                                                                 
           *////////////((((((((((((((((((((((((((((((((((((((((((((//////////////*             
         /////////////(((((((((((((((((((((((((((((((((((((((((((((((((//////////////           
        /////////      ,(((((((((((((((((((((((((((((((((((((((((((((((((/////////////          
        ///////  ####### (((((((((((((((((((((((((((((((((((((((((((((((((*       ////          
        /////// ########  (((((((((((((((((((((((((((((((((((((((((((((. .*********  /          
        ///////, ######  ((((((((((((((((((((((((((((((((((((((((((((  **************           
        //////((((,   /((((((((((((((((((((((((((((((/(((((((((((((  *****************          
        /////(((((((((((((((((((((((((((((((((   ********  ,(((((/ *******************          
        /////((((((((((((((((((((((((((((((  ***************  ((  ********************          
        ////((((((((((((((((((((((((((((. ,*******************. **********************          
        /////(((((((((((((((((((((((((  *********************. ***********************          
        /////(((((((((((((((((((((((. **********************  ****    .(##(.    ******          
        /////(((((((((((((((((((((( ,********************** ,*,  ((((((((((((((((. .**          
        /////((((((((((((((((((((  **********************, *, (((((((((((((////((((( .          
        //////(((((((((((((((((/ ,**********************  *  ((((((((((((////////((((           
        ///////(((((((((((((((  ***********************  *, ((((((((((((((///////((((/          
        ////////((((((((((((( ,*********************** .**. ((((((((((((/////////(((//          
        *////////((((((((((/ ***********************/ ***** ((((((/((((/////////(((///          
          /////////(((((((  ***********************. ******* ((((((((////////(((((///           
                                                               ((((((((///((((((///             
                                                                  /(((((((((((//                


                                 @@   @@                                                        
                                  @    @                                                        
                        @/   @    @    @    @     @    @ (     @   @                            
                             @    @    @    @     @    @      %/////@                           
                        @    @    @    @    @     @    @      @                                 
                        #@%@ ,@. @@@# @@@#   @@@@ @@  @@@.     ,@@@@                            



""")
print("              Welcome to allure - the wallpaper app              ")
print("allure downloads High Resolution pictures from UnSplash.com and sets them as your Desktop Wallpaper.\n")
print("allure features:")
print("    - use keywords to search wallpapers")
print("    - set  wallpaper change interval from every 5 minutes to once a day")
print("    - change image buffer size to save space (>=12 && <=30)")
print("    - use your own api access key")
print("    - lives in your SystemApp Tray, no installation required")
print("    - make changes to config via cmd and SystemApp Tray icon\n")
start_sys_ico()
settings()