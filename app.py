from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        rows_a = int(request.form['rows_a'])
        cols_a = int(request.form['cols_a'])
        rows_b = int(request.form['rows_b'])
        cols_b = int(request.form['cols_b'])

        # Check if matrix multiplication is possible
        if cols_a != rows_b:
            error = "Number of columns in Matrix A must equal number of rows in Matrix B."
            return render_template('index.html', error=error)

        return redirect(url_for('input_matrices', rows_a=rows_a, cols_a=cols_a, rows_b=rows_b, cols_b=cols_b))
    return render_template('index.html')

@app.route('/input_matrices', methods=['GET', 'POST'])
def input_matrices():
    rows_a = int(request.args.get('rows_a'))
    cols_a = int(request.args.get('cols_a'))
    rows_b = int(request.args.get('rows_b'))
    cols_b = int(request.args.get('cols_b'))

    if request.method == 'POST':
        # Retrieve Matrix A
        matrix_a = []
        for i in range(rows_a):
            row = []
            for j in range(cols_a):
                value = int(request.form.get(f'a_{i}_{j}', 0))
                row.append(value)
            matrix_a.append(row)

        # Retrieve Matrix B
        matrix_b = []
        for i in range(rows_b):
            row = []
            for j in range(cols_b):
                value = int(request.form.get(f'b_{i}_{j}', 0))
                row.append(value)
            matrix_b.append(row)

        # Perform matrix multiplication
        result = []
        for i in range(rows_a):
            result_row = []
            for j in range(cols_b):
                sum_product = 0
                for k in range(cols_a):
                    sum_product += matrix_a[i][k] * matrix_b[k][j]
                result_row.append(sum_product)
            result.append(result_row)

        return render_template('result.html', result=result)

    return render_template('input_matrices.html', rows_a=rows_a, cols_a=cols_a, rows_b=rows_b, cols_b=cols_b)

if __name__ == '__main__':
    app.run(debug=True)
