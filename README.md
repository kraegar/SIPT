# SIPT
Spirit Island Phase Tracker

This is a phase tracker for the board game Spirit Island.  The intent is to help players track phases and rule changes based on adversary, level, turn, and other statuses that may affect the game. It also has some help such as board setup changes and spirit setup.  All game assets, images, terms and names are property of Greater than Games and Eric Reuss.


To run this, you must install python 3 and kivy.

Follow the guide for installing kivy here: https://kivy.org/doc/stable/gettingstarted/installation.html#installation-canonical

For those on windows wanting the brief version, install python3 from python.org, then run the following.  This will create a virtual environment in the root of your C drive.

python -m pip install --upgrade pip setuptools virtualenv

c:

cd \\

python -m virtualenv sipt_venv

c:\sipt_venv\Scripts\activate

python -m pip install kivy[base] kivy_examples

mkdir c:\sipt_venv\apps

mkdir c:\sipt_venv\apps\sipt\

Finally, download all the files and move them into c:\sipt_venv\apps\sipt\

To run the app:

cd c:\sipt_venv\apps\sipt\

python main.py


If running on a raspberry pi, the app is now enabled for remote "next" clicks with a Bluetooth camera shutter control such as the following: https://www.amazon.com/gp/product/B08Y6K9NCJ/