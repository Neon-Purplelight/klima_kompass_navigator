# Installation

Diese Datei führt Sie durch die Installation der erforderlichen Komponenten, um den Klima-Kompass-Navigator auf Ihrem Computer auszuführen. Es setzt keine Vorkenntnisse in Python oder Programmiererfahrung voraus. Zur Installation der Notwendigen Pakete wird die Verwendung der [Anaconda- Paketverwaltung](https://www.anaconda.com/download) empfohlen.

## Schritt für Schritt Anleitung für das Terminal

- Klonen Sie dieses Repository in einen Ordner Ihrer Wahl auf Ihrem PC:
`cd voller/pfad/zum/gewünschten/installations/ordner/`  
`git clone https://github.com/Neon-Purplelight/klima_kompass_navigator.git`
- Gehen Sie in den neu erstellten Ordner:  
`cd klima_kompass_navigator`
- Erstellen Sie eine neue virtuelle Conda-Umgebung, um die notwendigen Pakete in einer isolierten Umgebung zu installieren:
`conda create -n klima_kompass_navigator Python==3.10`
- Aktivieren Sie die neu erstellte Umgebung:  
`conda activate pklima_kompass_navigator`
- Installieren Sie die erforderlichen Pakete:  
`pip install -r requirements.txt`
- Starten Sie den Navigator:  
`python app.py`
- Das Skript erstellt einen lokalen Server und gibt seine Adresse in der Konsole aus (normalerweise `http://127.0.0.1:8050/`). Öffnen Sie diese Adresse mit einem beliebigen Browser um die Webanwendung lokal von ihrem PC ausführen zu können.

Nach der ersten Installation können Sie die Webanwendung einfach ausführen, indem Sie die Umgebung aktivieren, in den geklonten Ordner wechseln und die Hauptdatei ausführen:

```python
conda activate klima_kompass_navigator
cd ../klima_kompass_navigator/
python app.py
```

## Installation (English)

This file guides you through the installation of the necessary components to run the Climate Compass Navigator on your computer. It does not require any prior knowledge of Python or programming experience. For the installation of the necessary packages, it is recommended to use the [Anaconda package manager](https://www.anaconda.com/download).

## Step-by-Step Instructions for the Terminal

- Clone this repository into a folder of your choice on your PC:
`cd full/path/to/desired/installation/folder/`  
`git clone https://github.com/Neon-Purplelight/klima_kompass_navigator.git`
- Navigate to the newly created folder:  
`cd klima_kompass_navigator`
- Create a new virtual Conda environment to install the necessary packages in an isolated environment:
`conda create -n klima_kompass_navigator Python==3.10`
- Activate the newly created environment:
`conda activate pklima_kompass_navigator`
- Install the required packages:
`pip install -r requirements.txt`
- Start the navigator:
`python app.py`
- The script creates a local server and displays its address in the console (usually `http://127.0.0.1:8050/`).  Open this address in any browser, and you should be able to browse the web application.

After the initial installation, you can simply run the web application by activating the environment, navigating to the cloned folder, and executing the main file:

```python
conda activate klima_kompass_navigator
cd ../klima_kompass_navigator/
python app.py
```
