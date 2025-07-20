import os
import random
from moviepy.editor import ImageClip, TextClip, AudioFileClip, CompositeVideoClip
from TikTokApi import TikTokApi

# ====== Configuration ======
QUOTES_FILE = "quotes.txt"
IMAGES_FOLDER = "images"
MUSIC_FOLDER = "music"
OUTPUT_FOLDER = "videos"
VIDEO_SIZE = (1080, 1920)
VIDEO_DURATION = 10  # seconds

# Environment variable: your TikTok session cookie
TIKTOK_SESSION = os.getenv("TIKTOK_SESSION")

# ====== Helper Functions ======
def get_random_line(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return random.choice([line.strip() for line in f if line.strip()])

def get_random_file(folder):
    files = os.listdir(folder)
    return os.path.join(folder, random.choice(files))

def generate_video():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    quote = get_random_line(QUOTES_FILE)
    bg_path = get_random_file(IMAGES_FOLDER)
    music_path = get_random_file(MUSIC_FOLDER)

    # Create image clip
    img_clip = ImageClip(bg_path).resize(height=VIDEO_SIZE[1]).set_duration(VIDEO_DURATION)
    txt_clip = TextClip(quote, fontsize=70, color="white", size=VIDEO_SIZE, method="caption", align="center")               .set_position("center").set_duration(VIDEO_DURATION)
    audio_clip = AudioFileClip(music_path).subclip(0, VIDEO_DURATION)

    video = CompositeVideoClip([img_clip, txt_clip]).set_audio(audio_clip)
    output_path = os.path.join(OUTPUT_FOLDER, f"video_{random.randint(1000,9999)}.mp4")
    video.write_videofile(output_path, fps=24)
    return output_path, quote

def post_to_tiktok(video_path, caption):
    if not TIKTOK_SESSION:
        print("Error: TIKTOK_SESSION environment variable not set.")
        return
    api = TikTokApi(custom_verify_fp=TIKTOK_SESSION)
    with open(video_path, "rb") as video_file:
        response = api.upload_video(video_file.read(), caption=caption)
    print("Posted to TikTok:", response)

if __name__ == "__main__":
    video_path, quote = generate_video()
    caption = f"{quote} \n#fyp #emopop #darkpoetry"
    post_to_tiktok(video_path, caption)
