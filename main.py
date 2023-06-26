import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
import csv


app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def home():
    try:
        with open('to-do-list.csv', 'r', newline='', encoding="utf8") as csv_file:
            csv_data = csv.reader(csv_file)
            list_of_rows = []

            for row in csv_data:
                list_of_rows.append(row[0])
    except FileNotFoundError:
        with open('to-do-list.csv', 'w') as csv_file:
            csv_file.write("To_Do_List\n")
        return render_template('index.html', to_dos=False)

    if request.method == 'POST':
        add = request.form.get('to_do')
        if add:
            with open('to-do-list.csv', 'a', encoding="utf8") as csv_file:
                csv_file.write(f"{request.form.get('to_do')}\n")
            return redirect(url_for('home'))

        for item in list_of_rows:
            value = request.form.get(str(list_of_rows.index(item)))

            if value:
                df = pd.read_csv('to-do-list.csv')
                print(df)
                df = df.loc[df['To_Do_List'] != list_of_rows[list_of_rows.index(item)]]

                df.to_csv('to-do-list.csv', index=False)

        return redirect(url_for('home'))
    return render_template('index.html', to_dos=list_of_rows)





if __name__ == "__main__":
    app.run(debug=True)