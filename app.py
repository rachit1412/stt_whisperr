from flask import Flask, request, render_template, jsonify
import wave
import os
import pyaudio
import soundfile as sf
from faster_whisper import WhisperModel
from colorama import init, Fore, Style

app = Flask(__name__)

# Initialize colorama
init()

# Initialize the Whisper model
model_size = "medium.en"
model = WhisperModel(model_size, device="cpu", compute_type="float32")

# Function to record audio chunk
def record_chunk(p, stream, file_path, chunk_length=10):
    frames = []
    for _ in range(0, int(16000 / 1024 * chunk_length)):
        data = stream.read(1024)
        frames.append(data)

    wf = wave.open(file_path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)
    wf.writeframes(b''.join(frames))
    wf.close()

# Function to transcribe audio chunk
def transcribe_chunk(model, file_path):
    audio, _ = sf.read(file_path)
    segments_generator, _ = model.transcribe(audio)
    transcription = ''.join(segment.text for segment in segments_generator)
    return transcription

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    # Record and transcribe audio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

    chunk_file = "temp_chunk.wav"
    record_chunk(p, stream, chunk_file, chunk_length=5)
    transcription = transcribe_chunk(model, chunk_file)
    os.remove(chunk_file)

    stream.stop_stream()
    stream.close()

    return jsonify({'transcription': transcription})

if __name__ == "__main__":
    app.run(debug=True)
