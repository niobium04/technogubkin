import pandas as pd
import io

from flask import Flask, render_template, request

from functions import f, create_figure

app = Flask(__name__)
plot_url = None


@app.route('/', methods=['GET', 'POST'])
def calculate():
    if request.method == 'POST':
        form = request.form

        your_choice = form['pipeline-input']
        your_choice_year = int(form['data-input'])
        df = pd.read_excel(form['file-input-1'], index_col=0)
        df1 = pd.read_excel(form['file-input-2'], index_col=0)
        df2 = pd.read_excel('ингибируемые.xlsx', index_col=0)

        result = f(your_choice, your_choice_year, df, df1)

        fig = create_figure(your_choice_year)

        output = io.BytesIO()
        fig.savefig(output, format='png')
        output.seek(0)

        with open('static/plot.png', 'wb') as file:
            file.write(output.read())

        plot_url = '/static/plot.png'
        return render_template('index.html', result=result, plot_url=plot_url)
    return render_template('index.html', result=' ', plot_url='')


if __name__ == '__main__':
    app.run(debug=False)
