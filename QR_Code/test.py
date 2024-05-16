import csv
import qrcode
import os
import win32print
import win32api

class QRPrinter:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.qr_data = self.read_csv()
        self.project_folder = os.path.dirname(os.path.abspath(__file__))  # Get the path of the current working directory

    def read_csv(self):
        qr_data = []
        with open(self.csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                qr_data.append(row)
        return qr_data

    def generate_qr_codes(self):
        qr_codes = []
        for row in self.qr_data:
            data = row[0]
            qr = qrcode.make(data, border=4)  # Add border to the QR code
            qr_codes.append((qr, row[0]))  # Append tuple of QR code and caption
        return qr_codes

    def print_qr_codes_directly(self):
        qr_codes = self.generate_qr_codes()

        for qr, caption in qr_codes:
            win32print.SetDefaultPrinter(win32print.GetDefaultPrinter())
            qr.show()

        print("QR codes printed directly")

# Usage
printer = QRPrinter("demo.csv")
printer.print_qr_codes_directly()
