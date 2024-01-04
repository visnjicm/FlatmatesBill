from flask.views import MethodView
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from flask import Flask, render_template, request
from flatmates_bill.flat import Flatmate, Bill
from flatmates_bill.reports import PdfReport

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a secure secret key

class HomePage(MethodView):

    def get(self):
        return render_template('index.html')


class BillForm(FlaskForm):
    amount = StringField("Bill Amount: ")
    period = StringField("Bill Period: ")

    name1= StringField("Name: ")
    days_in_house1 = StringField("Days in the house: ")

    name2= StringField("Name: ")
    days_in_house2 = StringField("Days in the house: ")

    button = SubmitField("Calculate")

class BillFormPage(MethodView):

    def get(self):
        bill_form = BillForm()
        return render_template('bill_form_page.html',
                               billform=bill_form, )


class ResultsPage(MethodView):
    def post(self):
        billform = BillForm(request.form)

        amount = int(billform.amount.data)
        period = str(billform.period.data)
        bill = Bill(amount=amount, period=period)

        flatmate1_name = str(billform.name1.data)
        flatmate1_days = int(billform.days_in_house1.data)
        flatmate1 = Flatmate(flatmate1_name,flatmate1_days)

        flatmate2_name = str(billform.name2.data)
        flatmate2_days = int(billform.days_in_house2.data)
        flatmate2 = Flatmate(flatmate2_name,flatmate2_days)

        flatmate_report = PdfReport('report.pdf')
        flatmate_report_url = flatmate_report.generate(flatmate1, flatmate2, bill)

        return f"Process done! View the bill here: {flatmate_report_url}"





app.add_url_rule('/', view_func=HomePage.as_view('home_page'))
app.add_url_rule('/bill_form', view_func=BillFormPage.as_view('bill_form_page'))
app.add_url_rule('/results', view_func=ResultsPage.as_view('results_page'))

if __name__ == "__main__":
    app.run(debug=False)
