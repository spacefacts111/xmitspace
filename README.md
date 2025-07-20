# TikTok Bot for Railway

This project auto-generates short videos combining quotes, images, and your music, then posts them to TikTok.

## Setup

1. **Import to Railway**  
   - Create a new Railway project using this repository (upload this zip).  
2. **Environment Variables**  
   - Set `TIKTOK_SESSION` to your TikTok session cookie.  
3. **Upload Media**  
   - In Railway's file manager, upload your `images/` folder (backgrounds), `music/` folder (MP3s), and `quotes.txt`.  

## Deployment

Railway will install dependencies from `requirements.txt` and run the `worker` process defined in `Procfile`, executing `main.py`.

## Scheduling

Use Railway's [Cron Plugin](https://railway.app/plugins/cron) to set how often you want the bot to run (e.g., every 8 hours).
