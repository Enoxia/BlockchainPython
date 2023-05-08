#!/usr/bin/python
# -*- coding: utf-8 -*-

#--- IMPORT PART --- #
from fileinput import close
import getpass
import json
import time
import os
from os import path
import sys
import hashlib
import glob

#Variable for Local blockchain
repo= "D:/Ynov/M2/Ydays/Initiation Blockchain/Fil Rouge/Script/"
genesis_file= "D:/Ynov/M2/Ydays/Initiation Blockchain/Fil Rouge/Script/e-vote-genesis.json"
filename = "D:/Ynov/M2/Ydays/Initiation Blockchain/Fil Rouge/Script/e-vote-0.json"
users = "D:/Ynov/M2/Ydays/Initiation Blockchain/Fil Rouge/Script/BDD_Users.json"
prefix = "e-vote-"
fileblock = repo+prefix+"*"
candidats = list()
abstention = 0

#Login
class authentification:
    def connexion():
        login = input("Numéro de porte-feuille : ") #Recuperation du login & mdp
        mdp = getpass.getpass("Mot de passe : ") 
        hashed = hashlib.md5(mdp.encode()) #Hashage du mdp

        for item in bdd.get_bddUsers(): #Parcours du fichier json
            if item['porte-feuille'] == login: #On recupère l'element du votant
                if item['mdp'] == hashed.hexdigest(): #On check le mot de passe
                    return item
#Recuperation des BDD
class bdd:
    def get_bddUsers(): #Récuperation du fichier json utilisateurs
        with open(users, 'r') as users_file:
            return json.load(users_file)

    def get_bddData(): #Récuperation du fichier json blockchain
        with open(filename, 'r') as blockchain_file:
            return json.load(blockchain_file)

#Recuperation nombre de voix
class voice:
    def get_listCandidat(): #Recuperation de la liste des candidats
        for item in bdd.get_bddUsers(): #Parcours du fichier json
            if item['candidat'] == True:
                candidats.append(item)
    def get_voice(candidat): #Calcul du nombre de voix d'un candidat
        solde = 0
        listblock = glob.glob(fileblock)
        
        for file in listblock:
            if "genesis" not in file:
                with open(file, 'r') as file_block:
                    data = json.load(file_block)
                for item in data: #Parcours du fichier json
                    try:
                        if item['Desti'] == candidat['porte-feuille']: #Pour chaque item dont le destinataire est le candidat
                            if item['Sender'] != "State": #On ne compte pas la transaction de l'etat
                                solde = solde + item['Tokens']
                    except:
                        continue
        return solde

#--- BLOCKCHAIN PART ---#
class Blockchain:
    print("[!] Starting Blockchain E-vote .....")
    # Define variables
    id_transact = 0 # Count each transaction per bloc
    id_total=0 #Count All transactions on Blockchain
    count_bloc = 0
    
    def __init__(self): #Starting the script
        file1,file2 = prefix+"genesis.json", prefix+"0.json"
        list=os.listdir(repo)
        if file1 in list and file2 in list:
            pass
        else:
            self.verify_file(file1)
            self.verify_file(file2)
            print("[!] Initialization of E-vote blockchain ....")
            self.generate_genesis_block(genesis_file)
        print("[!] Start GUI ......")
        self.gui()
        
    def generate_genesis_block(self,path): #Generate the first block (genesis block)
        print("[+] Generate the genesis block ....")
        with open(path, 'r') as f: #Open the file
            init_block = json.load(f)
        
        # Prepare genessis transaction
        t=time.localtime()
        t=time.strftime("%d-%m-%Y_%H:%M:%S", t)
        init_block.append({
            'timestamp': t,
            'id_transact': 0,
            'Tokens': 67,
            'Sender': "State",
            'Desti': "State"
        })   
        with open(path, 'w') as f: #Push the transaction on the block genessis
            json.dump(init_block,f, indent=4)
        next=repo+prefix+str(self.count_bloc)+".json"
        self.add_hash(path,next)
        print("[+] Genese block created !")
            
    def read_json(self,path): #Function to read JSON file (=blocks)
        # Read JSON file
        with open(path, 'r') as f:
            blockchain= json.load(f)
        # print('Lecture complete')
        return blockchain
        
    def verify_block(self): #Function of verification for block's size -> If 10 transactions => Change block
        file = ""
        if self.id_transact != 10 : 
            print("Ok")
            file=repo+prefix+str(self.count_bloc)+".json"
        else: 
            self.count_bloc=self.count_bloc+1 #Incrémente nb_bloc to influence the add_transact function
            file=repo+prefix+str(self.count_bloc)+".json" #Path of new file created
            old=repo+prefix+str(self.count_bloc-1)+".json" #Path of old file
            self.id_transact=0
            self.add_hash(old,file)
            print("Block Completed")
        return file
    
    def verify_file(self,path):
        print("[-] Verify if the file exist ....")
        list=os.listdir(repo)
        if path in list:
            pass
        else:
            print("[+] Create the missing file : ",path)
            with open(path, 'w') as f:
                f.write("[]")
        
    def add_hash(self,path,new_path):
        print("Add previous bloc into hash")    
        hash=hashlib.sha256(open(path,'rb').read()).hexdigest()
        
        t=time.localtime()
        t=time.strftime("%d-%m-%Y_%H:%M:%S", t)
        
        self.verify_file(new_path)
        
        addon=self.read_json(new_path)
        addon.append({
            'timestamp': t,
            'Hash': str(hash)
        })
        with open(new_path, 'w') as f:
            json.dump(addon,f,indent=4)
        print("[+]Link Completed")
            
    def add_transact(self,desti,sender): #Function to add transactions
        print("[+] Generate the transaction ....")
        file=self.verify_block()
        
        #Fill infrmations of the transaction
        t=time.localtime()
        t=time.strftime("%d-%m-%Y_%H:%M:%S", t)


        bloc=self.read_json(file)
        bloc.append({
            'timestamp': t,
            'id_transact': self.id_total,
            'Tokens': 1,
            'Sender': sender,
            'Desti': desti
        })
        #Push the transaction
        with open(file, 'w') as f:
            json.dump(bloc,f,indent=4)
            print("[+]Transaction implemented !")
            self.id_transact=self.id_transact+1 #Incrémente the id_transact transaction to the verify_block function
            self.id_total+=1
                    
    def gui(self): #User menu to use E-vote
        while True:
            abstention = 0
                        
            #Calcul de l'absentention
            for item in bdd.get_bddUsers():
                if item['aVoter'] == False:
                    abstention = abstention + 1
            
            #Affichage
            print("\33[34mRésultat \33[37m(voix):")
            for candidat in candidats:
                solde = voice.get_voice(candidat)
                print(' \33[32m',candidat['nom'], ':\33[37m', solde)
            print('  \33[37mAbstention :', abstention)
            
            #Demande action
            action = input("\n\33[33m1.\33[37m Voter\n\33[33m2.\33[37m Actualiser\n\33[33m3.\33[37m Quitter\n\nQue souhaitez vous faire : ")
            os.system('cls')
            if action == "1": #Vote
                connexion = authentification.connexion()
                os.system('cls')
                if connexion != None: #Si la connexion est operationnel
                    if connexion['aVoter'] == True:
                        print("\33[31mVous avez déjà voté\n")
                    else:
                        check = 0
                        while check == 0:
                            print("\33[34mCandidats :")
                            for candidat in candidats:
                                print("\33[32m",candidat['nom'])
                            
                            choix=input("\33[37mEntrez le nom du candidat pour qui souhaité voter : ")
                            os.system('cls')

                            for candidat in candidats:
                                if candidat['nom'] == choix: #Vérif du nom de candidat
                                    check = 1
                                    self.add_transact(candidat['porte-feuille'],connexion['porte-feuille'])
                                    
                                    with open(users, 'r') as users_file: #Ouverture JSON
                                        data = json.load(users_file)
                                    
                                    count = 0
                                    for d in data:
                                        if connexion['porte-feuille'] == data[count].get("porte-feuille"):
                                            d['aVoter'] = True #Modification futur JSON
                                        count = count+1
                                    
                                    with open(users, 'w') as users_file: #Ecriture JSON
                                        json.dump(data, users_file, indent=4)
                                    
                                    print("\n\33[32mVous avez voté pour",candidat['nom'],"\n")
                                    break
                            if check == 1:
                                break

                            print("\33[31mCandidat :",choix, "introuvable")
                            
                            #Demande action
                            action = input("\n\33[33m1.\33[37m Réessayer \n\33[33m2.\33[37m Quitter\n\nQue souhaitez vous faire : ")
                            os.system('cls')
                            if action == "1": #Réessayer
                                continue
                            elif action == "2": # Quitter
                                break
                            else:
                                continue
                else:
                    print("\33[31mPorte-feuille ou mot de passe incorrecte\n")

            elif action == "2": #Actualisation
                continue

            elif action == "3": #Quitter l'application
                print("\nFermeture de l'application\n")
                sys.exit()

            else:
                print("\33[31mEntrée non valide\n")
                continue

voice.get_listCandidat()   
e_vote=Blockchain()