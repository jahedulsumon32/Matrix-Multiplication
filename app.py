from flask import Flask, request, redirect, url_for, session, render_template_string

app = Flask(__name__)
app.secret_key = 'jahedulsumon64'  # Replace with a secure key in production

# Step 1: Enter dimensions of matrices A and B
@app.route('/', methods=['GET', 'POST'])
def step1():
    if request.method == 'POST':
        try:
            rows_a = int(request.form.get('rows_a'))
            cols_a = int(request.form.get('cols_a'))
            rows_b = int(request.form.get('rows_b'))
            cols_b = int(request.form.get('cols_b'))
            if cols_a != rows_b:
                error = "Number of columns in Matrix A must equal number of rows in Matrix B."
                return render_template_string(STEP1_TEMPLATE, error=error)
            session['rows_a'] = rows_a
            session['cols_a'] = cols_a
            session['rows_b'] = rows_b
            session['cols_b'] = cols_b
            return redirect(url_for('step2'))
        except ValueError:
            error = "Please enter valid integer dimensions."
            return render_template_string(STEP1_TEMPLATE, error=error)
    return render_template_string(STEP1_TEMPLATE)

# Step 2: Enter elements of matrices A and B
@app.route('/step2', methods=['GET', 'POST'])
def step2():
    rows_a = session.get('rows_a')
    cols_a = session.get('cols_a')
    rows_b = session.get('rows_b')
    cols_b = session.get('cols_b')
    if not all([rows_a, cols_a, rows_b, cols_b]):
        return redirect(url_for('step1'))
    if request.method == 'POST':
        try:
            matrix_a = []
            for i in range(rows_a):
                row = []
                for j in range(cols_a):
                    val = request.form.get(f'a_{i}_{j}')
                    row.append(float(val))
                matrix_a.append(row)
            matrix_b = []
            for i in range(rows_b):
                row = []
                for j in range(cols_b):
                    val = request.form.get(f'b_{i}_{j}')
                    row.append(float(val))
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
            return render_template_string(RESULT_TEMPLATE, result=result)
        except (ValueError, TypeError):
            error = "Please enter valid numbers for all matrix elements."
            return render_template_string(STEP2_TEMPLATE, rows_a=rows_a, cols_a=cols_a, rows_b=rows_b, cols_b=cols_b, error=error)
    return render_template_string(STEP2_TEMPLATE, rows_a=rows_a, cols_a=cols_a, rows_b=rows_b, cols_b=cols_b)

# HTML Templates
STEP1_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>Step 1: Enter Matrix Dimensions</title></head>
<body>
    <h2>Step 1: Enter Dimensions of Matrices A and B</h2>
    {% if error %}<p style="color:red;">{{ error }}</p>{% endif %}
    <form method="POST">
        <h3>Matrix A:</h3>
        Rows: <input type="number" name="rows_a" min="1" required><br>
        Columns: <input type="number" name="cols_a" min="1" required><br>
        <h3>Matrix B:</h3>
        Rows: <input type="number" name="rows_b" min="1" required><br>
        Columns: <input type="number" name="cols_b" min="1" required><br><br>
        <input type="submit" value="Next">
    </form>
</body>
</html>
'''

STEP2_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>Step 2: Enter Matrix Elements</title></head>
<body>
    <h2>Step 2: Enter Elements of Matrices A and B</h2>
    {% if error %}<p style="color:red;">{{ error }}</p>{% endif %}
    <form method="POST">
        <h3>Matrix A:</h3>
        {% for i in range(rows_a) %}
            {% for j in range(cols_a) %}
                <input type="number" step="any" name="a_{{ i }}_{{ j }}" required>
            {% endfor %}
            <br>
        {% endfor %}
        <h3>Matrix B:</h3>
        {% for i in range(rows_b) %}
            {% for j in range(cols_b) %}
                <input type="number" step="any" name="b_{{ i }}_{{ j }}" required>
            {% endfor %}
            <br>
        {% endfor %}
        <br>
        <input type="submit" value="Multiply">
    </form>
</body>
</html>
'''

RESULT_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>Result</title></head>
<body>
    <h2>Result: Matrix A x Matrix B</h2>
    <table border="1" cellpadding="5" cellspacing="0">
        {% for row in result %}
            <tr>
                {% for val in row %}
                    <td>{{ val }}</td>
                {% endfor %}
            </tr>
        {% endfor %}
    </table>
    <br>
    <a href="{{ url_for('step1') }}">Start Over</a>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)
