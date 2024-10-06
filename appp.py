import streamlit as st
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

# Function to format time in HH:MM:SS
def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f'{hours:02d}:{minutes:02d}:{secs:06.3f}'

# Function to detect audio dropouts
def detect_dropouts(file_data, dropout_db_threshold=-20, min_duration_ms=100):
    # Load the audio file
    y, sr = librosa.load(file_data, sr=None)

    # Improved time resolution by reducing hop length
    hop_length = 256  # Reduced hop length for better time resolution
    frame_length = hop_length / sr * 1000  # ms per frame

    # Convert the signal to decibels
    rms = librosa.feature.rms(y=y, frame_length=hop_length, hop_length=hop_length)
    rms_db = librosa.power_to_db(rms, ref=np.max)

    # Threshold to find dropouts (segments below the dropout_db_threshold)
    dropout_frames = rms_db[0] < dropout_db_threshold

    # Detect contiguous frames of dropouts lasting at least min_duration_ms
    min_frames = int(min_duration_ms / frame_length)
    dropouts = []
    start = None

    for i, is_dropout in enumerate(dropout_frames):
        if is_dropout and start is None:
            start = i  # Start of a dropout
        elif not is_dropout and start is not None:
            if i - start >= min_frames:
                start_time = start * hop_length / sr
                end_time = i * hop_length / sr
                duration_ms = (end_time - start_time) * 1000  # Convert duration to milliseconds
                dropouts.append((start_time, end_time, duration_ms))
            start = None

    # Handle the case where dropout extends to the end of the file
    if start is not None and len(dropout_frames) - start >= min_frames:
        start_time = start * hop_length / sr
        end_time = len(dropout_frames) * hop_length / sr
        duration_ms = (end_time - start_time) * 1000
        dropouts.append((start_time, end_time, duration_ms))

    return dropouts, y, sr

# Function to plot waveform with dropouts
def plot_waveform_with_dropouts(y, sr, dropouts):
    plt.figure(figsize=(12, 6))
    librosa.display.waveshow(y, sr=sr, alpha=0.6)
    plt.title('Waveform with Detected Dropouts')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')

    # Highlight dropouts
    for dropout in dropouts:
        start_time, end_time, _ = dropout
        plt.axvspan(start_time, end_time, color='red', alpha=0.5, label='Dropout' if 'Dropout' not in plt.gca().get_legend_handles_labels()[1] else "")
    
    plt.legend()
    st.pyplot(plt)

# Streamlit app layout
st.title("Audio Dropout Detection")
st.write("Upload an audio file (WAV format) to detect dropouts in the audio signal.")

# Upload audio file
audio_file = st.file_uploader("Choose an audio file", type=["wav"])

if audio_file is not None:
    # Process the uploaded file
    st.audio(audio_file, format='audio/wav')
    dropouts, y, sr = detect_dropouts(audio_file)

    # Display detected dropouts in a table
    st.subheader("Detected Dropouts")
    if dropouts:
        for dropout in dropouts:
            start, end, duration_ms = dropout
            st.write(f"Start: {format_time(start)} | End: {format_time(end)} | Duration: {duration_ms:.0f} ms")
    else:
        st.write("No significant dropouts detected.")
    
    # Plot waveform with highlighted dropouts
    st.subheader("Waveform with Dropouts")
    plot_waveform_with_dropouts(y, sr, dropouts)
