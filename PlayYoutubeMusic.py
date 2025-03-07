import yt_dlp
import ffmpeg

async def search_opening(search):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True
    }
    while True:
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(f"ytsearch:{search}", download=False)
                if 'entries' in result:
                    primeiro_video = result['entries'][0]
                    return primeiro_video['url']
        except:
            pass

