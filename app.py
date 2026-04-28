from flask import Flask, render_template, request, send_file
import os

# Optional imports (safe handling)
try:
    from watermark import apply_watermark, detect_watermark
except:
    apply_watermark = None
    detect_watermark = None

try:
    from drive_upload import upload_to_drive
except:
    upload_to_drive = None

try:
    from gemini import get_hashtags
except:
    get_hashtags = None


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)


# 🔹 Home
@app.route('/')
def home():
    return render_template("login.html")


# 🔹 Login → Select page
@app.route('/login', methods=['POST'])
def login():
    return render_template("select.html")


# 🔹 Pages
@app.route('/upload_page')
def upload_page():
    return render_template("upload.html")


@app.route('/detect_page')
def detect_page():
    return render_template("detect.html")


@app.route('/monitor_page')
def monitor_page():
    return render_template("monitor.html")


# 🔹 Upload video
@app.route('/upload', methods=['POST'])
def upload_video():
    file = request.files.get('video')

    if not file:
        return "No file uploaded"

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(PROCESSED_FOLDER, "secured_" + file.filename)

    file.save(input_path)

    # watermark (safe check)
    if apply_watermark:
        apply_watermark(input_path, output_path)
    else:
        output_path = input_path

    # drive upload (safe check)
    drive_id = "Not available"
    if upload_to_drive:
        try:
            drive_id = upload_to_drive(output_path)
        except:
            drive_id = "Drive upload failed"

    return render_template(
        "result.html",
        filename="secured_" + file.filename,
        drive_id=drive_id
    )


# 🔹 Download
@app.route('/download/<filename>')
def download_file(filename):
    path = os.path.join(PROCESSED_FOLDER, filename)
    return send_file(path, as_attachment=True)


# 🔹 Detect
@app.route('/detect', methods=['POST'])
def detect():
    file = request.files.get('video')

    if not file:
        return "No file uploaded"

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    result = "Detection not available"
    if detect_watermark:
        try:
            result = detect_watermark(path)
        except:
            result = "Error in detection"

    return render_template("detect_result.html", result=result)


# 🔹 Monitor + AI
@app.route('/monitor', methods=['POST'])
def monitor():
    keyword = request.form.get('keyword', '').lower()

    video_db = {
        "football": ["sample1.mp4", "sample2.mp4"],
        "ronaldo": ["sample2.mp4", "sample3.mp4"],
        "goal": ["sample1.mp4"]
    }

    videos = video_db.get(keyword, [])

    hashtags = "Not available"
    if get_hashtags:
        try:
            hashtags = get_hashtags(keyword)
        except:
            hashtags = "AI error"

    return render_template(
        "monitor_results.html",
        videos=videos,
        keyword=keyword,
        hashtags=hashtags
    )


# 🔹 Check ownership
@app.route('/check_video', methods=['POST'])
def check_video():
    video = request.form.get('video')

    if not video:
        return "No video selected"

    path = os.path.join(UPLOAD_FOLDER, video)

    result = False
    if detect_watermark:
        try:
            result = detect_watermark(path)
        except:
            result = False

    if result:
        return "<h2 style='color:green;text-align:center;'>✅ Ownership Verified</h2>"
    else:
        return "<h2 style='color:red;text-align:center;'>❌ Not Your Video</h2>"


# 🚀 Run (IMPORTANT for Render)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
