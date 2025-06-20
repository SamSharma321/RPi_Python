import regex as re
from RealtimeSTT import AudioToTextRecorder
import keyboard
import sounddevice as sd
import pyautogui

# Code to get mics connected to RPi
devices = sd.query_devices()
for i, device in enumerate(devices):
    if device['max_input_channels'] > 0:
        print(f"Index: {i}, Name: {device['name']}")

from RealtimeSTT import AudioToTextRecorder
import pyautogui

string = []

if __name__ == '__main__':
    recorder = AudioToTextRecorder(
        wake_words ="jarvis", 
        wake_word_buffer_duration = 3, 
        on_wakeword_detection_end = 'over', 
        language='en', 
        ensure_sentence_ends_with_period=False)

    print('Say "Jarvis" to start recording.')
    while True:
        print(recorder.text())
    
# stt.start()
# stt.listen()
# for text in stt.stream():
#     string.append()
#     if text:
#         print("You said:", text)
#     if keyboard.is_pressed('q'):
#         break
        