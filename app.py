from flask import Flask, render_template, request, send_file
import os
from watermark import apply_watermark, detect_watermark
from drive_upload import upload_to_drive
from gemini import get_hashtags   # 🔥 NEW (AI)

app = Flask(_name_)

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# 🔹 Login Page
@app.route('/')
def home():
    return render_template("login.html")


# 🔹 Select Page
@app.route('/login', methods=['POST'])
def login():
    return render_template("select.html")


# 🔹 Upload Page
@app.route('/upload_page')
def upload_page():
    return render_template("upload.html")


# 🔹 Detect Page
@app.route('/detect_page')
def detect_page():
    return render_template("detect.html")


# 🔹 Monitor Page
@app.route('/monitor_page')
def monitor_page():
    return render_template("monitor.html")


# 🔹 Upload + Watermark + Drive
@app.route('/upload', methods=['POST'])
def upload_video():
    file = request.files['video']

    if file:
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        output_path = os.path.join(PROCESSED_FOLDER, "secured_" + file.filename)

        file.save(input_path)

        # Apply watermark
        apply_watermark(input_path, output_path)

        # Upload to Drive
        drive_id = upload_to_drive(output_path)

        return render_template(
            "result.html",
            filename="secured_" + file.filename,
            drive_id=drive_id
        )

    return "Upload failed"


# 🔹 Download
@app.route('/download/<filename>')
def download_file(filename):
    path = os.path.join(PROCESSED_FOLDER, filename)
    return send_file(path, as_attachment=True)


# 🔹 Detect Watermark
@app.route('/detect', methods=['POST'])
def detect():
    file = request.files['video']

    if file:
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)

        result = detect_watermark(path)

        return render_template("detect_result.html", result=result)

    return "Error"


# 🔹 Monitor + Gemini AI Suggestions 🔥
@app.route('/monitor', methods=['POST'])
def monitor():
    keyword = request.form['keyword'].lower()

    # 🔹 Simulated database
    video_db = {
        "football": ["sample1.mp4", "sample2.mp4"],
        "ronaldo": ["sample2.mp4", "sample3.mp4"],
        "goal": ["sample1.mp4"]
    }

    videos = video_db.get(keyword, [])

    # 🔥 Gemini AI hashtags
    try:
        hashtags = get_hashtags(keyword)
    except:
        hashtags = "AI suggestions not available"

    return render_template(
        "monitor_results.html",
        videos=videos,
        keyword=keyword,
        hashtags=hashtags   # 🔥 send to HTML
    )


# 🔹 Check Ownership
@app.route('/check_video', methods=['POST'])
def check_video():
    video = request.form['video']

    path = os.path.join(UPLOAD_FOLDER, video)

    result = detect_watermark(path)

    if result:
        return "<h2 style='color:green;text-align:center;'>✅ Ownership Verified</h2>"
    else:
        return "<h2 style='color:red;text-align:center;'>❌ Not Your Video</h2>"


# 🚀 Run
if _name_ == '_main_':
    app.run(debug=True)
