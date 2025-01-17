from PyQt5 import QtGui  # (the example applies equally well to PySide)
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
import pandas as pd
import csv
import numpy as np
import serial
import time
import os,sys # to add the picture

'''
#Serial takes two parameters: serial device and baudrate
ser = serial.Serial('/dev/ttyACM0', 9600) #ttyACM0 is the port name it might change based on the device
ser.flushInput() #flush input buffer
'''
##read data from file
##method #1
#f=open("data.csv", "r")
#if f.mode == 'r':
#	contents = f.read()
#	print(contents[1:5])
#
##method 2
# The following code was used to draw data from a saved file
#Data=pd.read_csv('data.csv',usecols=['value'])# read a single  data from file 
#unit=pd.read_csv('data.csv',usecols=['data'])
#Conv_data = Data.rename_axis('value').values # change the data into numpy so we can process it later
#T_data=Conv_data.transpose() # transpose the array to align it for the grap
#T_data=T_data[0,0:5] # we take 5 elements for the example
#Conv_2=unit.rename_axis('data').values
#T_Conv_2=Conv_2.transpose()
#T_Conv_2=T_Conv_2[0,0:5]
# for debugging purposes
#print(T_Conv_2)
#print(T_data)
#print(Conv_data)
#print(Data)
#print(unit)


## Always start by initializing Qt (only once per application)
app = QtGui.QApplication([])

## Define a top-level widget to hold everything
#w = QtGui.QWidget()
win = pg.GraphicsWindow(title="Read data")


## Create some widgets to be placed inside
btn = QtGui.QPushButton('star')
qbtn = QtGui.QPushButton('Quit')
qbtn.clicked.connect(app.instance().quit)
qbtn.resize(qbtn.sizeHint())
qbtn.move(0, 0)  
text = QtGui.QLineEdit('enter text')
listW = QtGui.QListWidget()
Plot = pg.PlotWidget()
pic = QtGui.QLabel()
pic.setGeometry(0,0,200,100)
pic.setPixmap(QtGui.QPixmap("/home/motaz/Pictures/images.png"))

##list items
#newItem = QListWidgetItem()
#newItem.setText(T_Conv_2)
#listw.insertItem(row, newItem)


##data part
#here it's a pre-defined values for testing
hour = [1,2,3,4,5,6,7,8,9,10]
temperature = [30,32,34,32,33,31,29,32,35,45]

######
#Resize width and height
listW.resize(300,120)

listW.addItem("Item 1"); 
listW.addItem("Item 2");
listW.addItem("Item 3");
listW.addItem("Item 4");

listW.setWindowTitle('PyQT QListwidget Demo')

## Create a grid layout to manage the widgets size and position
layout = QtGui.QGridLayout()
win.setLayout(layout)
#win.setStyleSheet("background-image: url(/home/motaz/drawing.svg.png)")

## Add widgets to the layout in their proper positions
layout.addWidget(btn, 0, 0)   # button goes in upper-left
layout.addWidget(qbtn, 1, 0)   # button goes in upper-left
layout.addWidget(text, 2,0)   # text edit goes in middle-left
layout.addWidget(listW, 0, 1)  # list widget goes in bottom-left
layout.addWidget(Plot, 1, 1,2,1)  # plot goes on right side, spanning 3 rows
#layout.addWidget(pic)
layout.addWidget(pic,2,0)

'''
plot_window = 50
y_var = np.array(np.zeros([plot_window]))
x_var = np.array(np.zeros([plot_window]))
itt = 1
t0 = time.time()
# read data from serial port
while itt<plot_window :
	if ser.inWaiting()>0 :
		#data = ser.read()
		data_serial = ser.readline()	
		#if (data != NULL )
		print (itt)
		print(time.time())	
		print(data_serial)
		y_var[itt] = data_serial # save the data in array to be read later
		x_var[itt] = time.time()-t0 # offset all the time values with t0
		itt = itt + 1	
#debugging
print(x_var,y_var)
'''
## plot the data on the PlotWidget
Plot.plot(hour,temperature) #x_var, y_var)
	
## Display the widget as a new window
win.show()
#btn.show()

## Start the Qt event loop
app.exec_()


