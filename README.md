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
Chrome window should be opened and in it open the FOE world for which you would like to create MMR table. Once game is done loading

5. Run python script:
```
python pychrome.py
```
