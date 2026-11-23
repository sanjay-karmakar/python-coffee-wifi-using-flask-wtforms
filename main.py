from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from flask_bootstrap import Bootstrap5
import csv

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.secret_key = 'dfnjnrepsmncdvgt'


# Home page
@app.route("/")
def index():
	return render_template("index.html")


# Coffee page
@app.route("/cafes")
def cafes():
	with open("cafe-data.csv", newline='', encoding='utf-8') as csv_file:
		csv_data = csv.reader(csv_file, delimiter=',')
		list_of_rows = []
		for row in csv_data:
			list_of_rows.append(row)

	return render_template("cafes.html", cafes=list_of_rows)


# Add cafe
class CafeForm(FlaskForm):
	cafe = StringField(label='Cafe Name', validators=[DataRequired()])
	location = StringField(label='Cafe Location on Google Maps (URL)', validators=[DataRequired()])
	open = StringField(label='Opening Time e.g. 8AM', validators=[DataRequired()])
	close = StringField(label='Closing Time e.g. 5:30PM', validators=[DataRequired()])
	coffee = SelectField(label='Coffee Rating', choices=["☕️", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"], validators=[DataRequired()])
	wifi = SelectField(label='Wifi Strength Rating', choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"], validators=[DataRequired()])
	power = SelectField(label='Power Socket Availability', choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"], validators=[DataRequired()])
	submit = SubmitField(label='Submit')


@app.route("/add", methods=['GET', 'POST'])
def add():
	add_form = CafeForm()
	if add_form.validate_on_submit():
		# print(add_form.cafe.data)
		with open("cafe-data.csv", mode="a", encoding='utf-8') as csv_file:
			csv_file.write(f"\n{add_form.cafe.data},"
						   f"{add_form.location.data},"
						   f"{add_form.open.data},"
						   f"{add_form.close.data},"
						   f"{add_form.coffee.data},"
						   f"{add_form.wifi.data},"
						   f"{add_form.power.data}")
			return redirect(url_for("cafes"))

	return render_template("add.html", form=add_form)


if __name__ == '__main__':
	app.run(debug=True)