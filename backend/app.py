from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)
df = pd.read_csv("data/students.csv")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    name_query = request.args.get('name', '').lower()
    if not name_query:
        return jsonify([])

    results = df[df['Name'].str.lower().str.contains(name_query)].copy()
    output = []
    for _, row in results.iterrows():
        warning = None
        if str(row['Category']).strip() != str(row['Seat Type']).strip():
            warning = "Category and Seat Type mismatch"
        output.append({
            "name": row['Name'],
            "merit_no": int(row['Merit No']),
            "score": float(row['Merit Score']),
            "category": row['Category'],
            "seat": row['Seat Type'],
            "warning": warning
        })
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)
