from win32api import GetSystemMetrics
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import sys
import numpy as np

try:
    import Tkinter as tk				# used for puthon 2 ( i think )
except:
	import tkinter as tk				# used for python 3


from PIL import Image, ImageTk		# requires pillow package
import serial
from serial.tools import list_ports

# https://matplotlib.org/2.1.2/gallery/user_interfaces/embedding_in_tk_sgskip.html
import matplotlib
matplotlib.use("TkAgg")

monitor_width = GetSystemMetrics(0) 						# requires pypiwin32 package
monitor_height = GetSystemMetrics(1)
window_scaling = 0.6										# needs to be between 0 and 1

# for serial reading
#buffArray = []
baudrate = 9600
arrLen = 128
packCount = 0

# INITIALIZING SERIAL.
# this is now imported from SerialRead.py to make it more readable
# change 'COM4' to 'dev..' whatever for linux
# ser = SerialRead('COM4', baudrate, arrLen) # this needs to be global ( i know this is bad practice, but i didnt know of any other way to do this)


class SerialRead:
    #self.port_names = list_ports.comports()
    # checks if portName is available on the PC
    def comport_not_available(self):
        ports = list_ports.comports()
        for i in range(len(ports)):
            if self.port_name == ports[i].device:
                return False
        return True

    def __init__(self, port="Undefined", baudrate=9600, pack_len=0):
        # check if acceptable baud rate is set
        self.ser = serial.Serial()
        self.port_name = port
        self.baudrate_list = [300, 600, 1200, 2400, 4800,
                              9600, 14400, 19200, 28800, 38400, 57600, 115200]
        if(baudrate in self.baudrate_list):
            self.ser.baudrate = baudrate
        else:
            print("Baud rate not accepted")
            error = True

        # check if USB port is found / accepted name
        if(self.comport_not_available() and port == 'Undefined'):
            print("Port not availible/not located, or undefined")
            self.error = True
        else:
            self.ser.port = port

        self.error = False				# set true if something is wrong
        self.com_open = False			# set true if reading COM ports
        self.pack_count = 0
        self.pack_len = pack_len

    def init_serial_read(self):
        if not self.error:
            try:
                self.ser.open()
                self.ser.flush()
                self.com_open = True

                print("Serial reading initialized.")
                # need to dump first reading! "why?" you may ask. ¯\_(ツ)_/¯ it just works ¯\_(ツ)_/¯
                dumpReading = self.ser.read()
            # this error occurs if one serial parametere is wrong
            except(serial.serialutil.SerialException):
                print("Serial port error. Have you chosen a valid COM-port?")

    def end_serial_read(self):
        self.ser.close()
        self.com_open = False

    def read_serial_to_array(self, ser, arr, len_of_arr, pack_count):
        if len(arr) < len_of_arr:
            arr.append(str(self.ser.read())[2])

        if len(arr) == len_of_arr:
            self.pack_count += 1
            print(arr, " - ", self.pack_count, ' - ', len(arr))
            self.ser.flush()
            arr = []


class MenuBar:
    def __init__(self, master):
        self.master = master
        self.menubar = tk.Menu(self.master)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New", command=self.donothing)
        self.filemenu.add_command(label="Open", command=self.donothing)
        self.filemenu.add_command(label="Save", command=self.donothing)
        self.filemenu.add_command(label="Save as...", command=self.donothing)
        self.filemenu.add_command(label="Close", command=self.donothing)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.master.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.serialmenu = tk.Menu(self.menubar, tearoff=0)
        self.serialmenu.add_command(
            label='Choose serial port', command=self.choose_serial_com)
        self.serialmenu.add_command(
            label='Start serial', command=self.start_serial_com)
        self.serialmenu.add_command(
            label='End serial', command=self.end_serial_com)
        self.menubar.add_cascade(label="Serial", menu=self.serialmenu)
        # needed to actually show the menubar
        self.master.config(menu=self.menubar)

        self.comport_chosen = False

    def donothing(self):
        print("donothing")

    def set_serial_port(self):
        # this returns a tuple with the index of the comport
        self.index = self.port_box.curselection()
        # set com port to selected port in listbox.
        ser.port = self.com_ls[self.index[0]]
        self.com_win.destroy()
        self.comport_chosen = True
        # print(self.com_ls[self.index[0]])
        # print(type(self.index))
        # print('Serial port set to: ' )

    def choose_serial_com(self):
        self.com_win = tk.Toplevel(self.master, bg='gray12')
        self.com_win.geometry('200x100')

        self.ports = list_ports.comports() 				# get a list of com-ports
        self.port_box = tk.Listbox(
            self.com_win, width=50, height=120, selectmode=tk.SINGLE)

        self.com_ls = []
        if(len(self.ports) > 0):
            for i in range(len(self.ports)):
                # com_ls holds strings with names of com ports. needed for setting the serial port,
                self.com_ls.append(self.ports[i].device)
                # as port_box is a listbox item (hard to index and only returns indexes)
                self.port_box.insert(i, self.ports[i].device)
        else:
            self.port_box.insert(0, "no ports found")

        self.select_but = tk.Button(
            self.com_win, text='Select', command=self.set_serial_port)
        self.select_but.pack(side=tk.BOTTOM)

        self.port_box.pack()

        # ser.init_serial_read()

    def start_serial_com(self):
        if self.comport_chosen:
            ser.init_serial_read()
            print("Started serial read")
        else:
            print("Serial port not chosen!")

    def end_serial_com(self):
        self.comport_chosen = False
        ser.end_serial_read()
        print("Ended serial read")


class LivePlot:
    # https://matplotlib.org/2.1.2/gallery/user_interfaces/embedding_in_tk_sgskip.html

    def __init__(self, master):
        self.master = master
        # setting figsize aspect ratio to (1,1) makes it abide the ratio set by col and row in root
        self.f = Figure(figsize=(1, 1), dpi=80)
        self.a = self.f.add_subplot(111)
        self.t = np.arange(0.0, 3.0, 0.01)
        self.s = np.sin(2*np.pi*self.t)
        self.a.grid(b=True, which='major', axis='both', alpha=0.5)
        self.a.plot(self.t, self.s)

        self.canvas = FigureCanvasTkAgg(self.f, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

        # extra option
        #self.toolbar = NavigationToolbar2Tk(self.canvas, self.master)
        # self.toolbar.update()
        #self.canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)


class SteeringAngle:
    def __init__(self, master):
        self.master = master


class Table:
    def __init__(self, master):
        self.frame = tk.Frame(master)


class MainApp:
    def __init__(self, master):
        self.master = master
        #self.master_frame = tk.Frame(self.master)
        # self.master_frame.configure(bg='gray12')
        #self.master_frame.grid(sticky=tk.E+tk.N+tk.W+tk.S, row=1, column=1)

        self.fr_plot = tk.Frame(self.master)
        self.fr_plot.grid(sticky=tk.E+tk.N+tk.W+tk.S, row=0, column=1, )
        self.fr_plot.configure(bg='gray12')

        self.fr_table = tk.Frame(self.master)
        self.fr_table.grid(row=0, column=0, sticky=tk.E+tk.N+tk.W+tk.S)
        self.fr_table.configure(bg='gray12')

        self.fr_canmsg = tk.Frame(self.master)
        self.fr_canmsg.grid(row=1, column=1, sticky=tk.E+tk.N+tk.W+tk.S)
        self.fr_canmsg.configure(bg='black')

        self.fr_steering = tk.Frame(self.master)
        self.fr_steering.grid(row=1, column=0, sticky=tk.E+tk.N+tk.W+tk.S)
        self.fr_steering.configure(bg='red')

        self.menubar = MenuBar(self.master)
        self.live_plot = LivePlot(self.fr_plot)


if __name__ == '__main__':
    root = tk.Tk()
    # http://www.science.smith.edu/dftwiki/index.php/File:TkInterColorCharts.png
    # root.configure(background='gray12')							# change this number to a lower one if you want darker background
    # sets the icon for the application
    root.iconbitmap("Resources/logo.ico")
    root.title("DNV GL Fuel Fighters Data Visualization")
    # sets the opening size of the GUI to window_scaling * "your_monitor_resolution". need to slize string to remove ".0" after multiplication
    win_width = int(window_scaling * monitor_width)
    win_height = int(window_scaling * monitor_height)
    # this is now decided with mainApp frame size
    root.geometry(str(win_width) + 'x' + str(win_height))
    # root.maxsize(monitor_width, monitor_height)					# now you cant have a bigger window than your monitor resolution
    root.rowconfigure(0, weight=5)
    root.rowconfigure(1, weight=4)
    root.columnconfigure(0, weight=3)
    root.columnconfigure(1, weight=5)

    MainApp(root)
    root.update()
    root.mainloop()
