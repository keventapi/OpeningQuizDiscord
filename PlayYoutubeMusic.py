import yt_dlp
import ffmpeg

def search_opening(search):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(f"ytsearch:{search}", download=False)
        if 'entries' in result:
            primeiro_video = result['entries'][0]
            return primeiro_video['url'] 
        else:
            return None

def convert_webm_to_mp3(input_file, output_file):
    try:
        ffmpeg.input(input_file).output(output_file, codec='libmp3lame', audio_bitrate='192k').run()
    except ffmpeg.Error as e:
        print("Erro ao converter o arquivo:", e)
