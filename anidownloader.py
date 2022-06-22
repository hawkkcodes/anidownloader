# Community made AnimeFLV API import
from this import d
from animeflv import AnimeFLV
from pip import main
animeAPI = AnimeFLV()

# Community made Mega API import
from mega import Mega
megaDL = Mega()

# Creates a temporary anonymous login into MEGA
megaAnonLogin = megaDL.login()

# File managing library
import os

# Default download path, if you are using Windows change 'ismaf' to your account name
downloadPath = "C:\\Users\\ismaf\\Videos"

# Main menu print
def showMenu():
    print("Bienvenido a Anidownloader" + '\n' + 
            "------------------------------" + '\n' +
            "(0) - Cambiar la ruta de descarga [RECOMENDABLE SI USTED NO HA MODIFICADO EL CÓDIGO]" + '\n' +
            "(1) - Buscar animes" + '\n' +
            "(2) - Ver la información de un anime" + '\n' +
            "(3) - Descargar capítulos de un anime" + '\n' +
            "(4) - Finalizar script" + '\n')

# Download options menu print
def downloadMenu():
    print("(0) - Descargar todos los capítulos" + '\n' +
            "(1) - Descargar un capítulo en concreto")

# Changes the download route
def changeRoute():
    downloadPath = input("Escriba la nueva ruta de descarga [NOTA - Si estás en Windows, añade un backlash extra (\) en cada salto de directorio]: ")

# Checks if a filename has the correct syntax for Windows File Naming
def getFilename(filename):
    # Banned characters: \ / : * ? " < > |
    filename = filename.replace("'\'", "")
    filename = filename.replace("/", "")
    filename = filename.replace(":", "")
    filename = filename.replace("*", "")
    filename = filename.replace("?", "")
    filename = filename.replace('"', "")
    filename = filename.replace("<", "")
    filename = filename.replace(">", "")
    filename = filename.replace("|", "")
    return filename


# Asks for a string, prints all matching results
def animeFinderNoArg():
    stringSearch = input("Introduzca un término de búsqueda: ")
    results = animeAPI.search(stringSearch)
    if len(results) == 0:
        print("No se ha encontrado ningún resultado" + '\n')
    else:
        if len(results)==1:
            print("Se ha encontrado 1 resultado" + '\n')
        else:
            print("Se han encontrado " + str(len(results)) + " resultados" + '\n')
        for i in range(0, len(results)):
            print(str(i+1) + ". " + results[i].get("title") + '\n')

# Gets a list, to identify an anime to get its info later
def animeDetailsFinder(stringSearch, viewingChoice):
    results = animeAPI.search(stringSearch)
    results = results[viewingChoice-1]
    return str(results.get("id"))

# Used for getting an anime and check its details later       
def animeFinderVisual(stringSearch):
    results = animeAPI.search(stringSearch)
    if len(results) == 0:
        print("No se ha encontrado ningún resultado, volviendo al menú principal" + '\n')
        selected = -1
    else:
        if len(results) == 1:
            print("Se ha encontrado 1 resultado" + '\n')
        else:
            print("Se han encontrado " + str(len(results)) + " resultados" + '\n')
        for i in range(0, len(results)):
            print(str(i + 1) + "." + results[i].get("title") + '\n')
        
        selected = input("Escoja una de las opciones mostradas: ")
        selected = int(selected)

        if selected<1 or selected>len(results):
            print("El valor introducido está fuera de rango, volviendo al menú principal." + '\n')
            selected = -1
    return selected
        
# Shows extra details of an anime such as user rating or airing status
def viewInfoOrDL(gonnaDownload):
    stringSearch = input("Introduzca el nombre del anime: ")
    viewingChoice = animeFinderVisual(stringSearch)
    if viewingChoice != -1:
        animeChosen = animeDetailsFinder(stringSearch, viewingChoice)

        # If you get an error here, you must modify the API. Go to animeflv's __init__.py folder,
        # head over to lines 180 and 181, and replace them with this piece of code:

        """
        "title": soup.select_one('body div.Wrapper div.Body div div.Ficha.fchlt div.Container h1.Title').string,
        "poster": soup.find("meta", property="og:image")['content'],
        """

        animeChosen = animeAPI.getAnimeInfo(animeChosen)
        if gonnaDownload == 0:
             print("Título: " + animeChosen.get("title") + '\n' +
                    "AnimeFLV id: " + animeChosen.get("id") + '\n' +
                    "Tipo: " + animeChosen.get("type") + '\n' +
                    "Sinopsis: " + animeChosen.get("synopsis") + '\n' +
                    "Episodios: " + str(len(animeChosen["episodes"])) + '\n' +
                    "Puntuación: " + str(animeChosen.get("rating")) + " / 5" + '\n')      
        else:
            downloader(animeChosen)

# Downloads the actual chapters
def downloadChapter(animeChosen, episodeNumber):
    # Gets all possible download links for the desired chapter
    downloadLink = animeAPI.downloadLinksByEpisodeID(animeChosen["episodes"][episodeNumber-1].get("id"))

    found = 0     
    # Looks for the MEGA link position
    for i in range (0, len(downloadLink)):
        if downloadLink[i].get("server") == "MEGA":
            megaPos = i
            found = 1
            break
    if found == 0:
        print("No se ha encontrado ningún enlace de MEGA para este capítulo." + '\n')
    else:
        downloadLink = downloadLink[megaPos]["url"]

        # Sets the name of the file to the anime title and its chapter number
        chapterFilename = animeChosen["title"] + " - Episodio " + str(episodeNumber+1) + ".mp4"
        chapterFilename = getFilename(chapterFilename)
        print("Descargando " + chapterFilename)
                
        # If it throws a PermissionError [WinError 32] here, go to MegaAPI mepa.py file and remove a tab from lines 745 and 746
        # The file should be in the next path (Windows): 
        # C:\Users\YourUsername\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\mega
        megaAnonLogin.download_url(downloadLink, downloadPath, chapterFilename)

# Chooses what chapters to download
def downloader(animeChosen):
    downloadMenu()
    dlMenuOption = input("Escoja una opción: ")
    dlMenuOption = int(dlMenuOption)
    if dlMenuOption<0 or dlMenuOption>1:
        print("Valor erróneo, volviendo al menú principal." + '\n')
    else:
        # Download all possible chapters
        if dlMenuOption == 0:
            for i in range (0, len(animeChosen["episodes"])):
                downloadChapter(animeChosen, i)
        
        # Download a single chapter
        elif dlMenuOption == 1:
            dlMenuOption = input("Escoja un capítulo a descargar: ")
            dlMenuOption = int(dlMenuOption)-1
            downloadChapter(animeChosen, dlMenuOption)
        
mainMenuOption = 0
# Main program loop
while(mainMenuOption!=4):
    #This line is here just in case the API doesn't work properly for the first time (happened while testing)
    animeAPI = AnimeFLV()

    showMenu()
    mainMenuOption = input("Escoja una opción: ")
    mainMenuOption = int(mainMenuOption)

    # Loops until a correct option is chosen
    while(mainMenuOption<0 and mainMenuOption>4):
        mainMenuOption = input("Valor erróneo, introduzca una opción de la lista anterior: ")
    
    if mainMenuOption==0:
        changeRoute()
    elif mainMenuOption==1:
        animeFinderNoArg()
    elif mainMenuOption==2:
        gonnaDownload=0
        viewInfoOrDL(gonnaDownload)
    elif mainMenuOption==3:
        gonnaDownload=1
        viewInfoOrDL(gonnaDownload)

__version__ = '1.0.0'
__title__ = 'anidownloader'
__author__ = 'hawkkcodes'
__license__ = 'MIT'