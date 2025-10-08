# Movie Database Project

## Beschreibung
Eine Anwendung zum Verwalten von Filmen. Filme können über die OMDb API hinzugefügt werden und werden lokal in einer SQLite-Datenbank gespeichert. Zusätzlich kann eine Website mit allen Filmen generiert werden.

## Installation

1. Repository klonen:
```bash
git clone <repo-url>
In das Projektverzeichnis wechseln:

bash
Code kopieren
cd project
Abhängigkeiten installieren:

bash
Code kopieren
pip install -r requirements.txt
.env Datei erstellen mit OMDb API Key:

ini
Code kopieren
OMDB_API_KEY=<dein-key>
Nutzung
bash
Code kopieren
python run.py
Menüoptionen:

Filme listen

Filme hinzufügen (über OMDb)

Filme löschen

Filme aktualisieren

Statistik anzeigen

Zufälligen Film anzeigen

Filme nach Bewertung sortieren

Website generieren