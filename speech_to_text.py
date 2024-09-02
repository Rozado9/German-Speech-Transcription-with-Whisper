import os
import numpy as np
import torch
import whisper
import sounddevice as sd
import wavio
import time

# Überprüfen, ob CUDA verfügbar ist und das Gerät auswählen
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Funktion zur Audioaufnahme
def record_audio(duration, filename, samplerate=16000):
    print("Starte Aufnahme...")
    print("! Bitte Reden !.")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')

    for remaining in range(duration, 0, -1):
        print(f"Aufnahme läuft... {remaining} Sekunden verbleiben", end='\r', flush=True)
        time.sleep(1)

    sd.wait()  # Aufnahme beenden
    wavio.write(filename, recording, samplerate, sampwidth=2)
    print("\nAufnahme abgeschlossen!")


# verfügbaren Sprachen anzeigen
language_options = whisper.tokenizer.TO_LANGUAGE_CODE
languages = list(language_options.keys())
print("Verfügbare Sprachen:")
for lang in languages:
    print(lang)


# Sprache und Aufgabe über die Eingabeaufforderung abfragen
language = input("Wähle eine Sprache: ")
if language not in languages:
    print(f"Ungültige Sprache gewählt: {language}")
    exit()

task = input("Wähle eine Aufgabe (transcribe/translate): ")
if task not in ['transcribe', 'translate']:
    print(f"Ungültige Aufgabe gewählt: {task}")
    exit()

# Modell basierend auf der Benutzerauswahl laden
if language == "english":
    model = whisper.load_model("base.en")
else:
    model = whisper.load_model("base")

model.to(device)

print(
    f"Das Modell ist {'multilingual' if model.is_multilingual else 'nur Englisch'} "
    f"und hat {sum(np.prod(p.shape) for p in model.parameters()):,} Parameter."
)

# Optionen für die Transkription festlegen
options = whisper.DecodingOptions(language=language, task=task, without_timestamps=True)

# Benutzer fragen, ob eine neue Aufnahme gemacht werden soll oder eine vorhandene Datei verwendet wird
use_existing = input("Möchtest du eine vorhandene Audiodatei verwenden? (ja/nein): ").strip().lower()

if use_existing == 'ja':
    # Pfad zur vorhandenen Audio-Datei
    audio_path = input("Gib den Pfad zur vorhandenen Audiodatei an: ").strip()
    if not os.path.exists(audio_path):
        print("Die angegebene Datei existiert nicht.")
        exit()
else:
    # Audioaufnahme
    audio_filename = "aufnahme.wav"
    record_duration = int(input("Gib die Aufnahmedauer in Sekunden ein: "))
    record_audio(record_duration, audio_filename)
    audio_path = audio_filename

# Laden der Audio-Datei mit einer spezifischen Samplerate
audio = whisper.load_audio(audio_path, sr=16000)
audio = torch.tensor(audio).to(device)

# Berechnung der Gesamtdauer des Audios in Sekunden
duration_in_seconds = audio.shape[0] / 16000  # Da wir die Samplerate auf 16000 Hz festgelegt haben

# Setzen der Länge jedes Segments auf 30 Sekunden
segment_length = 30  # in Sekunden

# Sammeln der Ergebnisse aus jedem Segment
full_transcription = ""
for start in range(0, int(duration_in_seconds), segment_length):
    end = start + segment_length
    if end > duration_in_seconds:
        end = duration_in_seconds

    # Sicherstellen, dass Start und Ende ganzzahlige Werte sind
    start_index = int(start * 16000)
    end_index = int(end * 16000)

    # Lade und verarbeite das Audiosegment
    segment = whisper.pad_or_trim(audio[start_index:end_index].cpu().numpy())
    mel = whisper.log_mel_spectrogram(segment).to(device)
    result = model.decode(mel, options)
    full_transcription += result.text + " "

# Ausgabe
print("Vollständige Transkription:")
print(full_transcription)
