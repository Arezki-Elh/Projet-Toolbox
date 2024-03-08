import socket #importer le module socket
from datetime import datetime #pour calculer le temps d’exécution du scan
import threading #permet d’exécuter des programmes simultanément


def get_target(): #donne la main à l’utilisateur pour qu’il saisisse sa cible
    NUMERODELIP = input("Veuillez entrer l'address IP : ")  # Nous permet de mettre l'adress IP Ciblée
    IPCIBLE = socket.gethostbyname(NUMERODELIP) #retourne l’adresse IPv4 associée à celui-ci et s’il entre une adresse IP
    print(f'IP visée > {IPCIBLE}') #Nous affiche l'IP Ciblée, une fois que le code est lancée
    return IPCIBLE


def get_port_list(): #retourner la liste des ports connus
    print(f'rangement des ports  > [1 – 1024]') #on met de quel port à quel port, on souhaite scanner
    return range(1, 1024) # sa nous retourne la valeur


def scan_port(target, port): #  on crée l’objet socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #AF_INET correspond à l’adressage IPv4 et SOCK_STREAM fait référence au protocole TCP
        test = s.connect_ex((target, port)) #Test de connexion
        if test == 0: # Si le test est égale a 0
            print(f'Le port {port} est [OUVERT]') # sa va nous sortir comme quoi le port est bien ouvert
        else: # Sinon
             print(f'Le port {port} est [FERMER]') # sa va nous sortir comme quoi le port est bien Fermer
    

def port_scanner(): #On defenie la fonction port_scanner
    try: # ca va essayer
        target = get_target() # récupérer les valeurs qu’elles retournent dans les variables target et port_list
        port_list = get_port_list() # récupérer les valeurs qu’elles retournent dans les variables target et port_list
        thread_list = list() #parcourt la liste des ports
        start_time = datetime.now() #récupérer les temps de début de l’opération de balayage des ports

        for port in port_list: # Pour les ports qui sont dans la listes des ports 
            scan = threading.Thread(target=scan_port, args=(target, port)) #la classe Thread qui prend comme paramètres scan_port
            thread_list.append(scan) # le append permet d'ajouter un élément à la fin d'une liste existante 
            scan.daemon = True #pour qu’ils n’empêchent pas le programme principal de se terminer correctement
            scan.start() #on lance notre scan avec la méthode start()

        for scan in thread_list: #
            scan.join() # pour que le programme principal se mette en pause et attende que l’exécution de tous les threads se termine.
    except: # une exeption
        print("Quelque chose ne va pas !") # nous affiche ce message si y'a eu une exception
    else: # sinon, fais ça
        end_time = datetime.now() #récupérer les temps de fin de l’opération de balayage des ports
        print("le scanning a etait accomplie avec succées le", end_time , start_time) # Nous affiche a la fin du balayage la date et l'heure du début et de fin du scanning


if __name__ == '__main__': # Cette condition est utilisée pour développer un module pouvant à la fois être exécuté directement mais aussi être importé par un autre module pour apporter ses fonctions.
    port_scanner()