from cmd_sequences.ad_port_read import seq as run_ad_port_read_sequence
from cmd_sequences.firmware_identification import seq as run_firmware_identification_sequence
from serial import Serial
from report_generator.report import Report

from utils.singleton import Singleton

from device.handler import DeviceHandler

sg = Singleton()
sg.baud_rate = 115200 #initial baud rate

def main():

    ser = Serial('COM9', sg.baud_rate, timeout=1)

    report = Report("out/report.xlsx")

    i8_board = DeviceHandler("I8", ser)
    run_ad_port_read_sequence(i8_board, report)
    report.add_bold_separator()
    run_firmware_identification_sequence(i8_board, report)


    report.export()

    ser.close()





if __name__ == "__main__":
    main()
