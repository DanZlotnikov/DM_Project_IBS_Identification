import os
import csv
from flask import Flask, render_template, request
import pandas as pd
import ibs_identification  # your updated module with run_* functions

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('welcome.html')

@app.route('/select', methods=['POST'])
def select():
    selected_file = request.form['options']
    base_dir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, 'files', selected_file)

    # Read first row or columns from CSV/XLS (similar to your existing logic)
    if selected_file.endswith('.csv'):
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            first_row = next(reader)
    elif selected_file.endswith('.xls'):
        df = pd.read_excel(file_path)
        first_row = list(df.columns)
    else:
        first_row = []

    return render_template('columns.html', selected_file=selected_file, columns=first_row)

@app.route('/process_columns', methods=['POST'])
def process_columns():
    selected_columns = request.form.getlist('columns')
    k_value = request.form.get('k_value')
    threshold_value = request.form.get('threshold_value')
    selected_file = request.form.get('selected_file')

    # Decide which function to call based on the file
    if selected_file == "german_credit_data.csv":
        run_folder = ibs_identification.run_gcd(selected_columns, k_value, threshold_value)
    elif selected_file == "default_of_credit_card_clients.xls":
        run_folder = ibs_identification.run_ccc(selected_columns, k_value, threshold_value)
    elif selected_file == "CleanAdult_numerical_cat.csv":
        run_folder = ibs_identification.run_compas(selected_columns, k_value, threshold_value)
    elif selected_file == "SQFD - CY 2017.csv":
        run_folder = ibs_identification.run_sqfd(selected_columns, k_value, threshold_value)
    else:
        run_folder = None

    if run_folder:
        folder_path = os.path.join('code', 'static', run_folder) 
        k_images = sorted(os.listdir(os.path.join(folder_path, "K"))) 
        thres_images = sorted(os.listdir(os.path.join(folder_path, "Threshold"))) 
        gen_images = sorted(os.listdir(folder_path))
           
        gen_images = [img for img in gen_images if img.lower().endswith('.png')]

        # Replace backslashes with forward slashes for URLs.
        folder_path = folder_path.replace("\\", "/")
        run_folder = run_folder.replace("\\", "/")
        
        return render_template('results.html',
                               run_folder = run_folder,
                               k_images=k_images,
                               thres_images=thres_images,
                               gen_images=gen_images)
    else:
        return "Invalid file selected."

if __name__ == '__main__':
    app.run(debug=True)
