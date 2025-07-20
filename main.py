import os
import random
import shlex
import subprocess
import sys

# ── Configuration ─────────────────────────────────────────
SCRIPT_DIR    = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

QUOTES_FILE   = "quotes.txt"
IMAGES_FOLDER = "images"
MUSIC_FOLDER  = "music"
OUTPUT_FOLDER = "videos"
FONT_FILE     = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DURATION      = 10           # seconds
VIDEO_SIZE    = "1080x1920"  # width x height
FONTSIZE      = 70
FONT_COLOR    = "white"
TIKTOK_SESSION = os.getenv("TIKTOK_SESSION")

# ── Helpers ────────────────────────────────────────────────
def die(msg):
    print("❌", msg); sys.exit(1)

for path, desc in [
    (QUOTES_FILE, "quotes.txt"),
    (IMAGES_FOLDER, "images folder"),
    (MUSIC_FOLDER, "music folder"),
    (OUTPUT_FOLDER, "videos folder"),
]:
    if not os.path.exists(path):
        die(f"Missing {desc}")

def get_random_quote():
    with open(QUOTES_FILE, encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    return random.choice(lines).replace(":", "\\:").replace(",", "\\,")

def get_random_file(folder):
    items = os.listdir(folder)
    if not items: die(f"No files in {folder}")
    return os.path.join(folder, random.choice(items))

# ── Build & run FFmpeg commands ───────────────────────────
def generate_video():
    quote = get_random_quote()
    bg    = get_random_file(IMAGES_FOLDER)
    music = get_random_file(MUSIC_FOLDER)
    temp  = os.path.join(SCRIPT_DIR, "temp.mp4")
    out   = os.path.join(OUTPUT_FOLDER, f"video_{random.randint(1000,9999)}.mp4")

    vf = (
        f"scale={VIDEO_SIZE},"
        f"drawtext=fontfile='{FONT_FILE}':"
        f"text='{quote}':"
        f"fontcolor={FONT_COLOR}:fontsize={FONTSIZE}:"
        f"x=(w-text_w)/2:y=(h-text_h)/2"
    )

    # 1) image + text → silent video
    cmd1 = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", bg,
        "-vf", vf,
        "-t", str(DURATION),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        temp
    ]
    subprocess.run(cmd1, check=True)

    # 2) mux audio
    cmd2 = [
        "ffmpeg", "-y",
        "-i", temp, "-i", music,
        "-c:v", "copy", "-c:a", "aac", "-shortest",
        out
    ]
    subprocess.run(cmd2, check=True)
    os.remove(temp)
    print("✅ Video saved:", out)
    return out

# ── Post to TikTok ────────────────────────────────────────
def post_to_tiktok(video_path):
    if not TIKTOK_SESSION:
        die("TIKTOK_SESSION not set in env")
    from TikTokApi import TikTokApi
    api = TikTokApi(custom_verify_fp=TIKTOK_SESSION)
    with open(video_path, "rb") as vf:
        res = api.upload_video(vf.read(), caption="")  # caption logic if you want
    print("✅ Posted to TikTok:", res)

if __name__ == "__main__":
    video = generate_video()
    post_to_tiktok(video)
