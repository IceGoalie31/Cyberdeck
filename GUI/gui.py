import sys
import custom_modules
from PyQt5.QtWidgets import * #QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, QTime, Qt, QProcess, QIODevice, QUrl
from qtpy.QtWebEngineWidgets import QWebEngineView
import psutil
from socket import AddressFamily

#def on_scan_clicked():
#    print("scan clicked!")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Touchscreen GUI")
        self.setGeometry(100, 100, 800, 600)

        # Create a central widget to hold the tab widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        central_widget.setStyleSheet("background-color: darkgray;")

        # Create tab widget
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabBar::tab {
                height: 100px; /* Set tab height */
                width: 100px; /* Set tab width */
                border: none; /* Remove border */
                background-color: gray;
                
            }
            QTabBar::tab:selected {
                background-color: lightgray; /* Set selected tab background color */
            }
        """)

        # Create and add tabs to the tab widget
        tabs = [
            ("IO", "Placeholder for IO"),
            ("Map", "Placeholder for Xastir map"),
            ("Sat", "Placeholder for satellite image downloading"),
            ("Wifi", "Placeholder for WiFi pentesting"),
            ("Mar", "Placeholder for Wifi marauder connection (esp32 to be included in the case)"),
            ("Pwn", "Placeholder for pwnagotchi web interface, (pwnagotchi to be included in case)"),
            ("Etc", "Placeholder for other tools")
        ]

        for tab_name, tab_content in tabs:
            tab = QWidget()
            tab_layout = QVBoxLayout(tab)
            tab.setLayout(tab_layout)

            # Add a label to show placeholder content
            tab_layout.addWidget(QLabel(tab_content))

            # Add a button only to the "Wifi" tab
            if tab_name == "Wifi":
                #self.tab_layout = QVBoxLayout(self)
                #self.log_display = QProcess()
                self.log_display = QTextEdit()
                tab_layout.addWidget(self.log_display)

                # Add buttons to control log display
                button_scan = QPushButton("Scan")
                button_Deauth = QPushButton("Deauth")
                button_Scan_AP = QPushButton("Scan AP")
                button_clear = QPushButton("Clear")



                button_layout = QVBoxLayout()
                button_layout.addWidget(button_scan)
                button_layout.addWidget(button_Scan_AP)
                button_layout.addWidget(button_Deauth)
                button_layout.addWidget(button_clear)


                #tab_layout.addLayout(button_layout)

                combined_layout = QHBoxLayout()
                combined_layout.addLayout(button_layout)
                combined_layout.addWidget(self.log_display)


                tab_layout.addLayout(combined_layout)

                # Connect button signals to respective slots
                button_Deauth.clicked.connect(self.start_Deauth)
                button_Scan_AP.clicked.connect(self.scan_AP)
                button_clear.clicked.connect(self.log_display.clear)
                # Connect the button's clicked signal to the on_button_clicked function
                button_scan.clicked.connect(self.scan)

            tab_widget.addTab(tab, tab_name)

            if tab_name == "IO":
                #TODO: use grid box style - ref sdr cyberdeck

                # creating font object
                font = QFont('Arial', 50, QFont.Bold)
                # creating a label object
                self.label = QLabel()

                # setting center alignment to the label
                self.label.setAlignment(Qt.AlignCenter)

                # setting font to the label
                self.label.setFont(font)

                # adding label to the layout of the "IO" tab
                tab_layout.addWidget(self.label)

                # creating a timer object
                timer = QTimer(self)

                # adding action to timer
                timer.timeout.connect(self.showTime)

                # update the timer every second
                timer.start(1000)

                # Creating a group box to contain the clock label
                clock_group_box = QGroupBox("Clock")
                clock_layout = QVBoxLayout()
                clock_group_box.setLayout(clock_layout)

                # Adjusting the alignment of the clock group box to the top right
                tab_layout.addWidget(clock_group_box, alignment=Qt.AlignTop | Qt.AlignRight)
                clock_layout.addWidget(self.label)

                # Create group box for CPU information
                cpu_group_box = QGroupBox("CPU Information")
                cpu_layout = QVBoxLayout()
                cpu_group_box.setLayout(cpu_layout)
                cpu_group_box.setFixedWidth(250)

                # Create labels to display CPU usage and temperature
                self.cpu_usage_label = QLabel("CPU usage: --")
                self.cpu_temp_label = QLabel("CPU Temperature: -- brk on win")
                #self.mem_usage_label = QLabel("Memory usage: --")
                #DONETODO: move memory to own display box
                self.cpu_timer = QTimer(self)
                self.cpu_timer.timeout.connect(self.update_cpu_stats)
                self.cpu_timer.start(2000)  # Update every 2 seconds

                # Add labels to CPU layout
                cpu_layout.addWidget(self.cpu_usage_label)
                cpu_layout.addWidget(self.cpu_temp_label)
                #cpu_layout.addWidget(self.mem_usage_label)
                # Add CPU group box to the main layout
                #tab_layout.addWidget(cpu_group_box)

                # Add CPU group box to the layout of the "IO" tab
                tab_layout.addWidget(cpu_group_box)


                mem_group_box = QGroupBox("Memory Information")
                mem_layout = QVBoxLayout()
                mem_group_box.setLayout(mem_layout)
                mem_group_box.setFixedWidth(250)
                self.mem_usage_label = QLabel("Memory usage: --")
                #self.cpu_timer.timeout.connect(self.update_mem_stats)

                self.mem_timer = QTimer(self)
                self.mem_timer.timeout.connect(self.update_mem_stats)
                self.mem_timer.start(2000)

                mem_layout.addWidget(self.mem_usage_label)

                tab_layout.addWidget(mem_group_box)


                net_group_box = QGroupBox("Network Information")
                net_layout = QVBoxLayout()
                net_group_box.setLayout(net_layout)
                net_group_box.setFixedWidth(250)

                self.net_ip_address_label = QLabel("Ip address: --")
                self.net_bytes_sent_label = QLabel("Bytes sent: --")
                self.net_bytes_received_label = QLabel("Bytes received: --")
                self.net_packets_sent_label = QLabel("Packets sent: --")
                self.net_packets_received_label = QLabel("Packets received: --")
                self.net_error_receive_label = QLabel("Receive errors: --")
                self.net_error_sent_label = QLabel("Sent errors: --")

                net_layout.addWidget(self.net_ip_address_label)
                net_layout.addWidget(self.net_bytes_sent_label)
                net_layout.addWidget(self.net_bytes_received_label)
                net_layout.addWidget(self.net_packets_sent_label)
                net_layout.addWidget(self.net_packets_received_label)
                net_layout.addWidget(self.net_error_sent_label)
                net_layout.addWidget(self.net_error_receive_label)

                self.net_timer = QTimer(self)
                self.net_timer.timeout.connect(self.update_net_stats)
                self.net_timer.start(5000)

                self.update_net_ip_addr()

                self.ip_timer = QTimer(self)
                self.ip_timer.timeout.connect(self.update_net_ip_addr)
                self.ip_timer.start(120000)

                #net_layout.addWidget(self.net_bytes_sent_label)

                tab_layout.addWidget(net_group_box)

            if tab_name == "Sat":
                self.webview = QWebEngineView()
                tab_layout.addWidget(self.webview)
                self.webview.load(QUrl('http://google.com/'))

            if tab_name == "Pwn":
                self.webview = QWebEngineView()
                tab_layout.addWidget(self.webview)
                self.webview.load(QUrl('http://google.com/'))


        # Add tab widget to the main layout
        layout.addWidget(tab_widget)

    def start_Deauth(self):
        self.log_display.append(custom_modules.deauth())
    def scan_AP(self):
        self.log_display.append(custom_modules.scanAP())

    def clear_log(self):
        self.log_display.clear()

    def scan(self):
        self.log_display.append(custom_modules.scan())
    def showTime(self):

        # getting current time
        current_time = QTime.currentTime()

        # converting QTime object to string
        label_time = current_time.toString('hh:mm:ss')
        self.label.setFont(QFont('Arial', 20, QFont.Bold))

        # showing it to the label
        self.label.setText(label_time)

    def update_cpu_stats(self):
        #get cpu% from psUtil
        cpuPercentFloat = psutil.cpu_percent()
        cpuUsage = "CPU usage: " + str(cpuPercentFloat) + "%"
        self.cpu_usage_label.setText(cpuUsage)
        #WILL WORK ON LINUX
        #cpuTempFloat = psutil.sensors_temperatures()
        #cpuTemp = "GPU Usage: " + str(cpuTempFloat) + "°f"
        #self.cpu_temperature_label.setText(cpuUsage)

    def update_mem_stats(self):
        memUsage = "Mem usage: " + str(psutil.virtual_memory().percent) + "%"
        self.mem_usage_label.setText(memUsage)

    def update_net_stats(self):
        netBytesSent = "Bytes sent: " + str(psutil.net_io_counters(pernic=False, nowrap=False).bytes_sent)
        self.net_bytes_sent_label.setText(netBytesSent)

        netBytesReceived = "Bytes received: " + str(psutil.net_io_counters(pernic=False, nowrap=False).bytes_recv)
        self.net_bytes_received_label.setText(netBytesReceived)

        netPacketsRecieved = "Packets received: " + str(psutil.net_io_counters(pernic=False, nowrap=False).packets_recv)
        self.net_packets_received_label.setText(netPacketsRecieved)

        netPacketsSent = "Packets sent: " + str(psutil.net_io_counters(pernic=False, nowrap=False).packets_sent)
        self.net_packets_sent_label.setText(netPacketsSent)

        netErrorSent = "Sent errors: " + str(psutil.net_io_counters(pernic=False, nowrap=False).errout)
        self.net_error_sent_label.setText(netErrorSent)

        netErrorReceived = "Receive errors: " + str(psutil.net_io_counters(pernic=False, nowrap=False).errin)
        self.net_error_receive_label.setText(netErrorReceived)

    def update_net_ip_addr(self):
        interface_info = psutil.net_if_addrs()
        for addr in interface_info['Wi-Fi']: #TODO CHANGE ON LINUX
            if addr.family == AddressFamily.AF_INET:  # Check if it's an IPv4 address
                wifi_address = addr.address
                break
        netIpAddr = "Ip address: " + str(wifi_address)
        self.net_ip_address_label.setText(netIpAddr)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

