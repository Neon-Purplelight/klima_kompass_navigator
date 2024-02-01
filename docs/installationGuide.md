# Installation des Klima-Kompass-Navigators

*(English version below)*

Diese Anleitung zeigt Ihnen, wie Sie den Klima-Kompass-Navigator einfach auf Ihrem Computer installieren können. Sie brauchen keine Vorkenntnisse in Python oder Programmierung.

## Schritt-für-Schritt-Anleitung

### 1. Klonen Sie das Repository

Öffnen Sie das Terminal und geben Sie Folgendes ein:

`cd Pfad/zu/Ihrem/Wunschordner`
`git clone https://github.com/Neon-Purplelight/klima_kompass_navigator.git`

Ersetzen Sie `Pfad/zu/Ihrem/Wunschordner` mit dem Pfad, an dem Sie das Programm speichern möchten.

### 2. Wechseln Sie in den neuen Ordner

Geben Sie im Terminal ein:

`cd klima_kompass_navigator`

### 3. Erstellen Sie eine neue virtuelle Umgebung mit venv

Dies erstellt eine isolierte Umgebung für das Projekt.

`python -m venv klima_kompass_navigator_venv`

### 4. Aktivieren Sie die virtuelle Umgebung

Auf Windows:

`klima_kompass_navigator_venv\Scripts\activate`

Auf MacOS/Linux:

`source klima_kompass_navigator_venv/bin/activate`

### 5. Installieren Sie die erforderlichen Pakete

`pip install -r requirements.txt`

### 6. Starten Sie den Navigator

`python app.py`

Das Skript erstellt einen lokalen Server und gibt seine Adresse in der Konsole aus (normalerweise `http://127.0.0.1:8050/`). Öffnen Sie diese Adresse mit einem beliebigen Browser um die Webanwendung lokal von ihrem PC ausführen zu können.

Nach der ersten Installation können Sie die Webanwendung einfach ausführen, indem Sie die Umgebung aktivieren, in den geklonten Ordner wechseln und die Hauptdatei ausführen:

```cd Pfad/zu/Ihrem/Wunschordner/klima_kompass_navigator
klima_kompass_navigator_venv\Scripts\activate # Windows
source klima_kompass_navigator_venv/bin/activate # MacOS/Linux
python app.py
```

## Installation of the Climate Compass Navigator

This guide will show you how to easily install the Climate Compass Navigator on your computer. You don't need any prior knowledge in Python or programming.

## Step-by-Step Instructions

### 1. Clone the Repository

Open your terminal and enter the following:

`cd path/to/your/desired/folder`

`git clone https://github.com/Neon-Purplelight/klima_kompass_navigator.git`

Replace path/to/your/desired/folder with the path where you want to save the program.

### 2. Navigate to the New Folder

Enter in the terminal:

`cd klima_kompass_navigator`

### 3. Create a New Virtual Environment with venv

This creates an isolated environment for the project.

`python -m venv klima_kompass_navigator_venv`

### 4. Activate the Virtual Environment

On Windows:

`klima_kompass_navigator_venv\Scripts\activate`

On MacOS/Linux:

`source klima_kompass_navigator_venv/bin/activate`

### 5. Install the Required Packages

`pip install -r requirements.txt`

### 6. Start the Navigator

`python app.py`

The script creates a local server and displays its address in the console (usually `http://127.0.0.1:8050/`). Open this address in any browser to run the web application locally from your PC.

After the initial installation, you can easily run the web application by activating the environment, navigating to the cloned folder, and executing the main file:

```cd path/to/your/desired/folder/klima_kompass_navigator
klima_kompass_navigator_venv\Scripts\activate # Windows
source klima_kompass_navigator_venv/bin/activate # MacOS/Linux
python app.py
```
