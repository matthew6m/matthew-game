
credits = """
The story engine behind this game was created by SkilStak (skilstak.io)

           [0;31m        __   .__.__            __          __
           [0;31m  _____|  | _|__|  |   _______/  |______  |  | __
           [0;31m /  ___/  |/ /  |  |  /  ___/\   __\__  \ |  |/ /
           [0;31m \___ \|    <|  |  |__\___ \  |  |  / __ \|    <
           [0;31m/____  >__|_ \__|____/____  > |__| (____  /__|_ \[1;37m_______[0m
           [0;31m     \/     \/            \/            \/     \/[1;37m______/[0m
                                        [1;37mCoding Arts[0m
"""

license = copyright = """
Copyright (c) 2017 SkilStak, Inc.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation and/or
   other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

#------------------------------------------------------------------------------

import platform
import os.path as p
import glob
import importlib
from pathlib import Path
import sys
import re
import textwrap
import shutil
import json

class Parts: pass
parts = Parts()
current = ''
part = {}
prevpart = {}
previous = ''

data_init = {
    'parts': {},
    'stuff': {},
    'current': '',
    'previous': '',
    'name': 'friend'
}
data = data_init

isWindows = platform.system() == 'Windows'
isMac = platform.system() == 'Darwin' 
isLinux = platform.system() == 'Linux'
isBsd = platform.system() == 'FreeBSD'

#------------------------------------------------------------------------------

class Cache:

    def __init__(self):
        self.name = '.' + Path(__file__).stem
        self.path = Path.home() / self.name
        self.modpath = Path('.').absolute()
        self.id = self.modpath.name
        self.data = Path(str(self.path / self.id) + '.json')
        self.partspath = self.modpath / 'parts'
        self.actionspath = self.modpath / 'actions'
        self.make()

    def make(self):
        if not self.path.exists():
            self.path.mkdir()

    def save(self):
        global data
        text = json.dumps(data, indent=2)
        self.data.write_text(text)   

    def load(self):
        global data,current,previous
        if not self.data.exists(): return
        text = self.data.read_text()
        if text:
            data = json.loads(text)
            current = data.get('previous')
            go(current)
    
    def remove(self):
        self.data.unlink()

cache = Cache() # singleton
def save(): cache.save()
def load(): cache.load()

#------------------------------------------------------------------------------

class Colors: pass
c = colors = Colors()
c.base03 = c.b03 = c.Base03 = c.B03 = '\x1b[1;30m'
c.base02 = c.b02 = c.Base02 = c.B02 = '\x1b[0;30m'
c.base01 = c.b01 = c.Base01 = c.B01 = '\x1b[1;32m'
c.base00 = c.b00 = c.Base00 = c.B00 = '\x1b[1;33m'
c.base0 = c.b0 = c.Base0 = c.B0 = '\x1b[1;34m'
c.base1 = c.b1 = c.Base1 = c.B1 = '\x1b[1;36m'
c.base2 = c.b2 = c.Base2 = c.B2 = '\x1b[0;37m'
c.base3 = c.b3 = c.Base3 = c.B3 = '\x1b[1;37m'
c.yellow = c.y = c.Yellow = c.Y = '\x1b[0;33m'
c.orange = c.o = c.Orange = c.O = '\x1b[1;31m'
c.red = c.r = c.Red = c.R = '\x1b[0;31m'
c.magenta = c.m = c.Magenta = c.M = '\x1b[0;35m'
c.violet = c.v = c.Violet = c.V = '\x1b[1;35m'
c.blue = c.b = c.Blue = c.B = '\x1b[0;34m'
c.cyan = c.c = c.Cyan = c.C = '\x1b[0;36m'
c.green = c.g = c.Green = c.G = '\x1b[0;32m'
c.reset = c.x = c.Reset = c.X = '\x1b[0m'
c.line = c.l = c.Line = c.L = '\x1b[2K\x1b[G'

# at least attempt clear on non-Posix (even though the colors won't work)
if isWindows:
    c.screen = c.clear = c.Screen = c.Clear = c.s = c.S  = '\x1B[2J\x1B[0f'
else:
    c.screen = c.clear = c.Screen = c.Clear = c.s = c.S  = '\x1b[2J\x1b[H'

#------------------------------------------------------------------------------

# TODO add @color.setter to mod c.p and c.t as sideeffects
class ThemePrompt:

    def __init__(self):
        self.text = '--> '
        self.color = c.base3

class ThemeInput:

    def __init__(self):
        self.color = c.yellow

class ThemeTell:

    def __init__(self):
        self.color = c.base0

class ThemeMessages:

    def __init__(self):
        self.nopart = ''
        self.bye = ''
        self.nostart = ''
        self.restart = ''

class Theme:

    def __init__(self):
        self.prompt = ThemePrompt()
        self.input = ThemeInput()
        self.tell = ThemeTell()
        self.msgs = ThemeMessages()

theme = Theme() # singleton
theme.msgs.nopart = lambda : f"{c.r}I'm sorry. The author has not written the next part yet.{c.t}"
theme.msgs.bye = lambda : f"Sorry to see you go. See you soon, {data.name}."
theme.msgs.nostart = lambda : f"It appears the author has not added the required {c.r}Start{c.t} part."
theme.msgs.restart = lambda : f"Do you really want to delete your data and restart?"

c.p = c.prompt = theme.prompt.color
c.i = c.input = theme.input.color
c.t = c.tell = theme.tell.color

#------------------------------------------------------------------------------


class Synonyms: pass
syn = Synonyms()
syn.yes = ['yes','y','yep','yeppers','yeah','uhun','yess','affirmative',
'of course','obviously']
syn.no = ['no','nope','n','no way','obviously not', 'of course not','nien','nyet']
syn.bye = ['bye','exit','quit','so long','adios','goodbye','make it stop']
syn.restart = ['start over','start over again','respawn','restart']
syn.back = ['back','prev','previous']
syn.copyright = ['copyright','legal','copying','copyleft','(c)']
syn.credits = ['author','authors','creator','creators',
    'attribution','developer','developers','team','credit','credits']

#------------------------------------------------------------------------------

def _onenter():
    tell(theme.msgs.nostart)
    sys.exit(1)

parts.Start = {
    'onenter': _onenter
}

def _oninput(e):
    if e.yes:
        cache.remove()
        sys.exit(0)

parts.Restart = {
    'onenter': theme.msgs.restart,
    'oninput': _oninput
}

#------------------------------------------------------------------------------

class Event:
    pass

class InputEvent(Event):

    def __init__(self,text):
        super()
        self.line = text.strip()
        self.lower = self.line.lower()
        self.yes = self.lower in syn.yes
        self.no = self.lower in syn.no

#------------------------------------------------------------------------------

class Actions:

    def __init__(self):
        self.synonyms = {}

    def detect(self,line):
        line = line.replace(' ','')
        for name in self.__dict__:
            if name[0].isupper():
                if line.lower().startswith(name.lower()):
                    return self.__dict__.get(name)
        for syn in self.synonyms:
            if line.lower().startswith(syn):
                return self.__dict__.get(self.synonyms[syn])

    def addSynonyms(self,name,synonyms):
        for syn in synonyms:
            self.synonyms[syn.lower().replace(' ','')] = name

actions = Actions() # singleton
actions.Clear = lambda e : clear()
actions.Data = lambda e : show(data)
actions.Bye = lambda e : quit()
actions.addSynonyms('Bye', syn.bye)
actions.Restart = lambda e : go('Restart')
actions.addSynonyms('Restart', syn.restart)
actions.Back = lambda e : go(previous)
actions.addSynonyms('Back', syn.back)
actions.License = lambda e : tell(license)
actions.addSynonyms('License', syn.copyright)
actions.Credits = lambda e : tell(credits)
actions.addSynonyms('Credits', syn.credits)

def _action(e):
    tell("You look hard, {name}.")
    onlook = part.get('onlook')
    if onlook:
        if callable(onlook):
            onlook()
        else:
            tell(onlook)

actions.Look = _action

#------------------------------------------------------------------------------

def handleinput(text):
    e = InputEvent(text)
    if e.line:
        action = actions.detect(e.line)
        if action:
            action(e)
            return
    oninput = part.get('oninput')
    if oninput:
        if callable(oninput):
            oninput(e)
        else:
            go(oninput)

def run():
    try:
        while True:
            text = input(f'{theme.prompt.color}{theme.prompt.text}{theme.input.color}')
            handleinput(text)
    except KeyboardInterrupt:
        tell('\b\n(Keyboard Interrupt Caught)')
        quit()

def go(name):
    global data, previous, current, prevpart, part
    if not parts.__dict__.get(name):
        tell(theme.msgs.nopart)
        return
    clear()
    onleave = part.get('onleave')
    if onleave:
        if callable(onleave):
            onleave()
        else:
            tell(onleave)
    previous = current
    current = name
    data['current'] = current
    data['previous'] = previous
    save()
    part = parts.__dict__.get(current)
    prevpart = parts.__dict__.get(previous)
    if current != previous:
        onenter = part.get('onenter')
        if onenter:
            if callable(onenter):
                onenter()
            else:
                tell(onenter)

#------------------------------------------------------------------------------

def clear():
    print(c.clear)

def tell(what):
    if type(what) is str:
        what = what.format(**data,c=c)
        what = textwrap.dedent(what)
        what = c.t + what.strip() + c.x + '\n'
    print(what)

def show(what):
    print(what)

def quit():
    tell(theme.msgs.bye)
    sys.exit(0)

#------------------------------------------------------------------------------

# autodetect new actions and parts and import them

if cache.actionspath.exists():
    for f in cache.actionspath.iterdir():
        if f.is_file() and f.name.endswith('.py') and not f.name.startswith('_') and not f.name.startswith('.'):
            module = 'actions.' + f.stem 
            importlib.import_module(module)

for f in cache.partspath.iterdir():
    if f.is_file() and f.name.endswith('.py') and not f.name.startswith('_') and not f.name.startswith('.'):
        module = 'parts.' + f.stem 
        importlib.import_module(module)

#------------------------------------------------------------------------------

load()
if not current:
    go('Start')
run()
