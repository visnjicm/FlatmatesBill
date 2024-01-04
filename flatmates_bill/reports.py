from fpdf import FPDF
import webbrowser
import os
from flatmates_bill.filesharer import FileSharer


class PdfReport:
    """
    Creates a Pdf file that contains data about
    the flatmates such as their names, their due amount
    and the period of the bill.
    """

    def __init__(self, filename):
        self.file_url = None
        self.filename = filename

    def generate(self, flatmate1, flatmate2, bill):
        flatmate1_pay = "$" + str(round(flatmate1.pays(bill, flatmate2), 2))
        flatmate2_pay = "$" + str(round(flatmate2.pays(bill, flatmate1), 2))

        pdf = FPDF(orientation='P', unit='pt', format='A4')
        pdf.add_page()

        # Add icon
        # pdf.image(name="OOP/Project 2/files/house.png", x=10, y=10, w=50, h=50)

        # Insert title
        pdf.set_font(family='Times', size=24, style='BU')
        pdf.cell(w=0, h=80, txt='Flatmates Bill', border=0, align='C', ln=1)

        # Insert Period label and value
        pdf.set_font(family='Times', size=22, style='B')
        pdf.cell(w=100, h=40, txt="Period:", border=0, align='L', ln=0)
        pdf.cell(w=150, h=40, txt=bill.period, border=0, align='L', ln=1)

        # Insert name and due amount of the first flatmate
        pdf.set_font(family='Times', size=20, style='')
        pdf.cell(w=100, h=40, txt=flatmate1.name, border=0, align='L', ln=0)
        pdf.cell(w=150, h=40, txt=flatmate1_pay, border=0, align='L', ln=1)

        # Insert name and due amount of the second flatmate
        pdf.cell(w=100, h=40, txt=flatmate2.name, border=0, align='L', ln=0)
        pdf.cell(w=150, h=40, txt=flatmate2_pay, border=0, align='L', ln=1)

        # Open the PDF
        pdf.output(self.filename)
        # webbrowser.open("file:///home/marko/Python/OOP/Project 2/files/" + self.filename)

        # Fileshare
        file_share = FileSharer(filepath=self.filename)
        self.file_url = file_share.share()
        return self.file_url
