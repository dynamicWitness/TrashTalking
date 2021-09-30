import requests
import json
import time
import pyperclip
import ctypes
from ctypes import wintypes
import time
import random

insultFile = open('.../Insults.txt','r')
insults=insultFile.readlines()

compFile = open('.../Compliments.txt','r')
compliments=compFile.readlines()

#insult = insults[random.randint(0,len(insults))]

user32 = ctypes.WinDLL('user32', use_last_error=True)
INPUT_KEYBOARD = 1
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002
KEYEVENTF_UNICODE     = 0x0004
MAPVK_VK_TO_VSC = 0
# msdn.microsoft.com/en-us/library/dd375731
wintypes.ULONG_PTR = wintypes.WPARAM
class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx",          wintypes.LONG),
                ("dy",          wintypes.LONG),
                ("mouseData",   wintypes.DWORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))
class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk",         wintypes.WORD),
                ("wScan",       wintypes.WORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))
    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)
class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg",    wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))
class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type",   wintypes.DWORD),
                ("_input", _INPUT))
LPINPUT = ctypes.POINTER(INPUT)

def PressKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))
def ReleaseKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def Enter():
    PressKey(0x0D)
    time.sleep(0.5)
    ReleaseKey(0x0D)
    # you can change 0x30 to any key you want. For more info look at :
    # msdn.microsoft.com/en-us/library/dd375731


#F12()



def toKeyCode(c):
    keyCode = keyCodeMap[c[0]]
    return int(keyCode, base=16)

keyCodeMap = {
    'shift'             : "0x10",
    ' '                 : '0x20',
    '0'                 : "0x30",
    '1'                 : "0x31",
    '2'                 : "0x32",
    '3'                 : "0x33",
    '4'                 : "0x34",
    '5'                 : "0x35",
    '6'                 : "0x36",
    '7'                 : "0x37",
    '8'                 : "0x38",
    '9'                 : "0x39",
    'a'                 : "0x41",
    'b'                 : "0x42",
    'c'                 : "0x43",
    'd'                 : "0x44",
    'e'                 : "0x45",
    'f'                 : "0x46",
    'g'                 : "0x47",
    'h'                 : "0x48",
    'i'                 : "0x49",
    'j'                 : "0x4A",
    'k'                 : "0x4B",
    'l'                 : "0x4C",
    'm'                 : "0x4D",
    'n'                 : "0x4E",
    'o'                 : "0x4F",
    'p'                 : "0x50",
    'q'                 : "0x51",
    'r'                 : "0x52",
    's'                 : "0x53",
    't'                 : "0x54",
    'u'                 : "0x55",
    'v'                 : "0x56",
    'w'                 : "0x57",
    'x'                 : "0x58",
    'y'                 : "0x59",
    'z'                 : "0x5A",
    'enter'             : "0x0D",
}

#Variables start
championKill = False
InhibKilled = False
multikill1 = False
multikill2 = False
multikill3 = False
multikill4 = False
multikill5 = False
ace = False
towerKill = False
isDead = False
summonerName = str
api_key = str
port = str
sentence='Youll never be half the man your mother is'
previousIsDead = bool
kills = 0
prevKills = 0
gotKill=True
summonerName = 'Your summoners\' name'
api_key = 'Your API key'
port ='2999'
#Variables end

#Main loop 
OldRandInt = 0
OldRandIntC = 0
while(True):
      randint = random.randint(0,len(insults)-1)
      if OldRandInt == randint:
            randint = random.randint(0,len(insults)-1)
            continue
      else:
            OldRandInt = randint
      insult = insults[randint]
      insult = insult.strip()

      randIntC = random.randint(0,len(compliments)-1)

      if OldRandIntC == randIntC:
            randIntC = random.randint(0,len(compliments)-1)
            continue
      else:
            OldRandIntC = randIntC

      compliment=compliments[randIntC]
      compliment=compliment.strip()

      responseAllGameData = requests.get('https://127.0.0.1:'+port+'/liveclientdata/allgamedata', headers={'api_key': api_key},verify=False)
      temp=json.loads(responseAllGameData.text)
      #print(temp)
      parts=temp['allPlayers']
      playerInfo = next((sub for sub in parts if sub['summonerName'] ==summonerName), None)
      #print(parts)
      #print(playerInfo)
      #scores = playerInfo['scores']
      #print(scores)
      #print(parts)
      scores=playerInfo['scores']
      kills = scores['kills']
      if kills != prevKills:
            prevKills = kills
            PressKey(0x10)
            Enter()
            ReleaseKey(0x10)

            for x in insult.lower(): 
                  PressKey(toKeyCode(x))
                  ReleaseKey(toKeyCode(x))
            Enter()
            
                  
      #input('test1')
      if playerInfo != None:
            isDead = playerInfo['isDead']
      else:
            isDead=False
      print(isDead)

      #print(port)
      if previousIsDead != isDead:
            previousIsDead = isDead
            if isDead:
                  PressKey(0x10)
                  Enter()
                  ReleaseKey(0x10)
                  for x in compliment.lower(): 
                        PressKey(toKeyCode(x))
                        ReleaseKey(toKeyCode(x)) 
                  Enter()
            else:
                  print('Not Dead')
      if kills==True:
            print('hello')
      time.sleep(1)