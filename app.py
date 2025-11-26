from flask import Flask, render_template
import pandas as pd
import os

EXCEL_PATH = os.environ.get("EXCEL_PATH", "/data/data.xlsx")

app = Flask(__name__)

@app.route("/")
def index():
    try:
        df = pd.read_excel(EXCEL_PATH)
        table_html = df.to_html(
            classes="table table-striped",
            index=False,
            border=0
        )
        return render_template(
            "index.html",
            table_html=table_html,
            excel_path=EXCEL_PATH,
        )
    except Exception as e:
        return f"Error loading {EXCEL_PATH}: {e}", 500

if __name__ == "__main__":
    # ローカルテスト用
    app.run(host="0.0.0.0", port=8000)

