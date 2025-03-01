import os
import csv
from flask import Flask, render_template, request, jsonify
import pandas as pd
import ibs_identification  # your updated module with run_* functions
import time
import threading

app = Flask(__name__)

run_folder = ''

def _make_run_folder(prefix):
    """
    Create a unique folder in static/runs based on current time.
    Returns the relative path to that folder (e.g. 'runs/gcd_1677699482').
    """
    run_id = int(time.time())  # or use uuid.uuid4() for more uniqueness
    folder_name = f"{prefix}_{run_id}"
    # We'll store runs in 'static/runs/<prefix>_<timestamp>'
    run_folder = os.path.join("code\\static", "runs", folder_name)
    os.makedirs(run_folder, exist_ok=True)
    os.makedirs(os.path.join(run_folder, "K"), exist_ok=True)
    os.makedirs(os.path.join(run_folder, "Threshold"), exist_ok=True)
    # Return the relative path that Flask can use: 'runs/<prefix>_<timestamp>'
    return os.path.join("runs", folder_name)

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

def run_ibs_processing(run_folder, selected_file, selected_columns, k_value, threshold_value):
    # Decide which function to call based on the file
    if selected_file == "german_credit_data.csv":
        ibs_identification.run_gcd(run_folder, selected_columns, k_value, threshold_value)
    elif selected_file == "default_of_credit_card_clients.xls":
        ibs_identification.run_ccc(run_folder, selected_columns, k_value, threshold_value)
    elif selected_file == "CleanAdult_numerical_cat.csv":
        ibs_identification.run_compas(run_folder, selected_columns, k_value, threshold_value)
    elif selected_file == "SQFD - CY 2017.csv":
        ibs_identification.run_sqfd(run_folder, selected_columns, k_value, threshold_value)
    else:
        run_folder = None

@app.route('/process_columns', methods=['POST'])
def process_columns():
    selected_columns = request.form.getlist('columns')
    k_value = request.form.get('k_value')
    threshold_value = request.form.get('threshold_value')
    selected_file = request.form.get('selected_file')
    global run_folder
    
    if selected_file == "german_credit_data.csv":
        run_folder = _make_run_folder("gcd")
    elif selected_file == "default_of_credit_card_clients.xls":
        run_folder = _make_run_folder("ccc")
    elif selected_file == "CleanAdult_numerical_cat.csv":
        run_folder = _make_run_folder("compas")
    elif selected_file == "SQFD - CY 2017.csv":
        run_folder = _make_run_folder("sqfd")
    
    # Start IBS identification in a separate thread
    processing_thread = threading.Thread(target=run_ibs_processing, args=(run_folder, selected_file, selected_columns, k_value, threshold_value))
    processing_thread.start()

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
@app.route('/get_images')
def get_images():
    """Fetch newly generated images dynamically while IBS runs."""
    global run_folder
    folder_path = os.path.join("code", "static", run_folder)
    if not os.path.exists(folder_path):
        return jsonify({"k_images": [], "thres_images": [], "gen_images": []})

    k_folder = os.path.join(folder_path, "K")
    thres_folder = os.path.join(folder_path, "Threshold")

    k_images = sorted([img for img in os.listdir(k_folder) if img.lower().endswith('.png')]) if os.path.exists(k_folder) else []
    thres_images = sorted([img for img in os.listdir(thres_folder) if img.lower().endswith('.png')]) if os.path.exists(thres_folder) else []
    gen_images = sorted([img for img in os.listdir(folder_path) if img.lower().endswith('.png') and img not in k_images and img not in thres_images])

    return jsonify({"k_images": k_images, "thres_images": thres_images, "gen_images": gen_images})

if __name__ == '__main__':
    app.run(debug=True)
