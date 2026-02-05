import streamlit as st
import struct
import base64
import io
import wave
import math

def generate_tone(frequency, duration, volume=0.5, sample_rate=22050):
    n_samples = int(sample_rate * duration)
    samples = []
    for i in range(n_samples):
        t = i / sample_rate
        fade = 1.0
        if i > n_samples * 0.7:
            fade = (n_samples - i) / (n_samples * 0.3)
        value = volume * fade * math.sin(2 * math.pi * frequency * t)
        samples.append(int(value * 32767))

    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        for s in samples:
            wf.writeframes(struct.pack('<h', s))
    return buf.getvalue()

def generate_correct_sound():
    s1 = generate_tone(523, 0.15, 0.4)
    s2 = generate_tone(659, 0.15, 0.4)
    s3 = generate_tone(784, 0.25, 0.4)

    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(22050)
        for src in [s1, s2, s3]:
            r = io.BytesIO(src)
            with wave.open(r, 'rb') as rf:
                wf.writeframes(rf.readframes(rf.getnframes()))
    return buf.getvalue()

def generate_wrong_sound():
    s1 = generate_tone(200, 0.3, 0.4)
    s2 = generate_tone(150, 0.4, 0.3)

    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(22050)
        for src in [s1, s2]:
            r = io.BytesIO(src)
            with wave.open(r, 'rb') as rf:
                wf.writeframes(rf.readframes(rf.getnframes()))
    return buf.getvalue()

def generate_select_sound():
    return generate_tone(440, 0.1, 0.3)

def generate_victory_sound():
    notes = [523, 659, 784, 1047]
    parts = []
    for note in notes:
        parts.append(generate_tone(note, 0.2, 0.4))

    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(22050)
        for src in parts:
            r = io.BytesIO(src)
            with wave.open(r, 'rb') as rf:
                wf.writeframes(rf.readframes(rf.getnframes()))
    return buf.getvalue()

def play_sound(wav_data):
    b64 = base64.b64encode(wav_data).decode()
    st.markdown(f"""
        <audio autoplay>
            <source src="data:audio/wav;base64,{b64}" type="audio/wav">
        </audio>
    """, unsafe_allow_html=True)
