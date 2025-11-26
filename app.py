from flask import Flask, render_template
import pandas as pd
import os
import requests
import tempfile
import logging

# ロギング設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

EXCEL_URL = os.environ.get("EXCEL_URL")
EXCEL_PATH = os.environ.get("EXCEL_PATH")

app = Flask(__name__)

@app.route("/")
def index():
    try:
        # EXCEL_URLが設定されている場合は、URLからダウンロード
        if EXCEL_URL:
            logger.info(f"Downloading Excel from URL: {EXCEL_URL}")
            response = requests.get(EXCEL_URL, timeout=30)
            response.raise_for_status()
            
            # 一時ファイルに保存
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                tmp_file.write(response.content)
                tmp_path = tmp_file.name
            
            try:
                df = pd.read_excel(tmp_path)
                excel_path_display = EXCEL_URL
            finally:
                # 一時ファイルを削除
                os.unlink(tmp_path)
        elif EXCEL_PATH:
            # EXCEL_PATHが設定されている場合は、ローカルファイルから読み込み
            logger.info(f"Loading Excel from path: {EXCEL_PATH}")
            df = pd.read_excel(EXCEL_PATH)
            excel_path_display = EXCEL_PATH
        else:
            return "Error: EXCEL_URL or EXCEL_PATH environment variable must be set", 500
        
        table_html = df.to_html(
            classes="table table-striped",
            index=False,
            border=0
        )
        return render_template(
            "index.html",
            table_html=table_html,
            excel_path=excel_path_display,
        )
    except Exception as e:
        logger.error(f"Error loading Excel: {e}", exc_info=True)
        return f"Error loading Excel: {e}", 500

if __name__ == "__main__":
    # ローカルテスト用
    app.run(host="0.0.0.0", port=8000)

