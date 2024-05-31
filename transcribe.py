#STEP 1: INSTALL PYTHON
#STEP 2: INSTALL PIP
#### Run in terminal if pip is installed
#### install pip: curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
#STEP 3: INSTALL DEPENDENCIES WITH PIP
#pip install moviepy openai-whisper transformers ffmpeg
#STEP 4: OPEN POWERSHELL ON ANACONDA.NAVIGATOR ("POWERSHELL PROMPT")
#STEP 5: INSTALL CONDA
# conda install ffmpeg
## Windows:OPTIONAL: 
# Install ffmpeg via chocolatey https://chocolatey.org/install
# choco install ffmpeg-full (then hit A for All). You may also need to use anaconda to install this package
# Step 5: Make sure temp, output, & input files are next to the python script. TODO: Ensure if folders dont exist that script
from moviepy.editor import VideoFileClip
from transformers import pipeline
import whisper, os, datetime, itertools

def extract_audio_from_video(video_path, audio_path):
    print("Starting Video conversion with", video_path, audio_path)
    video = VideoFileClip(video_path)
    print("Starting Audio write with", audio_path)
    video.audio.write_audiofile(audio_path)
    print("Writing Audio complete")

def transcribe_audio(audio_path):
    print("Starting Transcribe with Whisper for file", audio_path)
    model = whisper.load_model("base")
    if(os.path.isfile(audio_path)):
        result = model.transcribe(audio_path)
        print("Transcription complete")
        return result["text"]
    else:
        print("No Valid File avaliable")
        exit()

def summarize_text(text, max_length=500, min_length=50):
    summarizer = pipeline("summarization")
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False, truncation=True)
    return summary[0]['summary_text']

#find files:
import os, fnmatch
def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result

def process_video(video_path):
    if not isinstance(video_path, str):
        raise TypeError(f"Expecting a string as a value, not {type(video_path)}.")
    else:
        audio_path = "DONT_DELETE-temp_audio.wav"
        print("Sending video files for extraction", video_path)

        try:
            print("Starting extracting Audio")
            extract_audio_from_video(video_path, audio_path)
            print("Extracted Audio complete")
            transcription = transcribe_audio(audio_path)
            print("Starting Clean up temp audio file")
            os.remove(audio_path)  # Clean up the temporary audio file
            # print("Processing Summary of:", transcription)
            summary = summarize_text(transcription)
            print("Summary Generation Successful", summary)
            try:
                now = datetime.datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
                # outputDirectory = os.path.join(os.path.expanduser('~'),'output')
                outputDirectory =  os.path.join(os.getcwd(),'output')
                text_file = open(os.path.join(outputDirectory, f"Test-{now}.txt"), "w")
                text_file.write("Full Text: \n")
                text_file.write(transcription)
                text_file.write("\n Summary: \n")
                text_file.write(summary)
                text_file.close()
                return summary
            except BaseException as e:
                print("Failed to write Text File", "Error:", str(e))
        except BaseException as e:
            print("Failed to Summarize Audio", "Error:", str(e))


try:
    # video_path = find('*.mp4', r'C:\Users\Antonio\Downloads\python')
    # Pulls File Path and starts converting video
    video_path = find('*.mp4', os.getcwd())
    print(video_path)
    print("\n - ".join(itertools.chain(
        ["Pulling videos from:"],
        video_path
    )))

    for video in video_path:
        print(f"Beginning Summary for: {video}")
        summary = process_video(video)
        print("Summary of the quarterly report:", summary)
except BaseException as e:
    print("Error:", str(e))

