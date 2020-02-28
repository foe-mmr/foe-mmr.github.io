# foe-mmr.github.io
MMR list FOE EN11

### Making your own MMR table for other servers/worlds

File pychrome.py contains Python script that can be used to make your own MMR table for other servers and/or worlds.
Account that can access GvG maps is needed in each world you want to make MMR table.

1. First Clone or download repository or you can simply copy pychrome.py content and create new file.

2. Install (if not already installed) pip for Python 2 with:

```
sudo apt install python-pip
```
3. To install pychrome, simply:

```
pip install pychrome
```

4. Setup Chrome headless mode (chrome version >= 59):

```
google-chrome --headless --disable-gpu --remote-debugging-port=9222
```
No other Chrome windows should be open before. Chrome window should be opened and in it open the FOE world for which you would like to create MMR table. Once game is done loading

5. In another terminal run python script:
```
python pychrome.py
```

If everythings ok then you should see something like this in terminal:
```
---------------------
   MMR Table maker   
---------------------
  GvG MAPS: 0 / 13
  Guilds: 0
---------------------
```

Now you need to do some clicking, click on every GvG map and its leaderbord. After that click on Global rankings guilds section and keep clicking throught pages until you reach desired guild count. You can keep track of your clicking progress in terminal. Once you have clicked on every GvG maps leaderboard and opened at least one page of guild global rankings MMR table will be created and printed to terminal where you can copy it.
