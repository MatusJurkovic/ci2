# Usage: 
>1.) git clone https://github.com/MatusJurkovic/ci2.git  
>2.) wsl  
>3.) cd projects/ci2/A06  
>4.) python3 -m venv .venv  
>5.) source .venv/bin/activate  
>6.) pip install -r requirements.txt  
>7.) python graph.py  

# Description: 
After installing the required modules, the script imports numpy, pandas and matplotlib modules. Then it reads the CSV file (commands added to recognise decimals with ',' and columns with ';'). After reading the file, the script creates a plot area (8 by 4 inches). Then the script plots the X-axis and Y-axis. Points are makred by a blue circle. The Y-axis is limited from 1.2 to -1.2, since the values only reach from 1.0 to -1.0. In order to make the graph easier to navigate I included the command to plot a dashed line at Y = 0. The script then names the axis (names defined in CSV) and the graph (Y = cos(X)). FInally, the script adds a light grid, saves the graph as graph.png with 300 DPI and opens a pop-up window with the created graph. 