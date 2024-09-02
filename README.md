# German-Speech-Transcription-with-Whisper

Dieses Repository enthält ein Python-Skript zur Transkription deutscher Sprache, das die OpenAI Whisper-Technologie nutzt. Das Projekt verwendet FFmpeg für die Audioverarbeitung.

## Inhalte

1. `requirements.txt` - Abhängigkeiten für das Projekt.
2. `speech_to_text.py` - Das Hauptskript für die Sprachtranskription.

## Installation

### Vorbereitungen

Klone das Repository und installiere die erforderlichen Python-Bibliotheken:

```bash
git clone https://github.com/IhrUsername/German-Speech-Transcription-with-Whisper.git
cd German-Speech-Transcription-with-Whisper
pip install -r requirements.txt
```
### FFmpeg-Installation
FFmpeg ist essentiell für die Audioverarbeitung. Die Installation variiert je nach Betriebssystem.

Windows
- Lade FFmpeg von der offiziellen FFmpeg-Builds-Seite herunter:
  - [Download FFmpeg Windows 64-bit GPL](https://github.com/BtbN/FFmpeg-Builds/releases/download/autobuild-2024-09-02-12-48/ffmpeg-N-116839-g3f9ca51015-win64-lgpl-shared.zip)

-  Entpacke die heruntergeladene Datei in das Verzeichnis deiner Wahl, z.B.:
```bash
C:\Program Files\ffmpeg
```
- Umgebungsvariablen einrichten
  Füge den bin-Ordner von FFmpeg zu den Umgebungsvariablen hinzu:
  ```bash
  C:\Program Files\ffmpeg\bin
  ```
  Gehe zu den Systemeinstellungen -> Erweiterte Systemeinstellungen -> Umgebungsvariablen -> Path -> Bearbeiten -> Neu -> Füge den Pfad ein -> OK.


- - Überprüfen der Installation
  Überprüfe die Installation von FFmpeg, indem du das folgende Kommando in der Kommandozeile ausführst:
  ```bash
  ffmpeg -version
  ```
  
Linux
- Installation:
  Installiere FFmpeg direkt über den Paketmanager deiner Distribution:
  ```bash
  sudo apt-get install ffmpeg  # Für Debian/Ubuntu
  ```

- Überprüfen der Installation
Überprüfe die Installation von FFmpeg auf Windows und Linux:
  ```bash
  ffmpeg -version
  ```
### Nutzung
Um das Transkriptionsskript zu starten, führe speech_to_text.py aus dem Hauptverzeichnis aus:

 ```bash
  python speech_to_text.py
  ```



