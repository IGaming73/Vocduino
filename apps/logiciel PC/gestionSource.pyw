import PyQt5.QtWidgets as Qt  # gestion de l'UI
import PyQt5.QtGui as QtGui  # gestion de certaines propriétés comme le style du texte
from PyQt5 import QtCore  # gestion de certaines propriétés comme l'alignement du texte
from PyQt5 import uic  # importation de l'UI depuis un fichier
from tkinter import filedialog  # sauvegarder un fichier
import os  # interaction avec le système
import threading  # effectuer des actions en parallèle
import pyperclip  # interraction avec le presse-papier

class MainGUI(Qt.QMainWindow):
    """Classe permettant de gérer la fenêtre principale et les boîtes de dialogue du logiciel"""
    
    def __init__(self):
        """On initialise la fenêtre principale"""
        super().__init__()  # on appelle la classe parente QMainWindow
        uic.loadUi("UI/main.ui", self)  # on charge le fichier UI de la fenêtre principale

        self.dict_keys = {
            "Ctrl gauche": "KEY_MOD_LCTRL", "Ctrl droit": "KEY_MOD_RCTRL",
            "Shift gauche": "KEY_MOD_LSHIFT", "Shift droit": "KEY_MOD_RSHIFT",
            "Alt gauche": "KEY_MOD_LALT", "Alt droit": "KEY_MOD_RALT",
            "Windows gauche": "KEY_MOD_LMETA", "Windows droit": "KEY_MOD_RMETA",
            "A": "KEY_A", "B": "KEY_B", "C": "KEY_C", "D": "KEY_D",
            "E": "KEY_E", "F": "KEY_F", "G": "KEY_G", "H": "KEY_H",
            "I": "KEY_I", "J": "KEY_J", "K": "KEY_K", "L": "KEY_L",
            "M": "KEY_M", "N": "KEY_N", "O": "KEY_O", "P": "KEY_P",
            "Q": "KEY_Q", "R": "KEY_R", "S": "KEY_S", "T": "KEY_T",
            "U": "KEY_U", "V": "KEY_V", "W": "KEY_W", "X": "KEY_X",
            "Y": "KEY_Y", "Z": "KEY_Z",
            "&": "KEY_1", "é": "KEY_2", '"': "KEY_3", "'": "KEY_4",
            "(": "KEY_5", "-": "KEY_6", "è": "KEY_7", "_": "KEY_8",
            "ç": "KEY_9", "à": "KEY_0",
            "Return": "KEY_ENTER", "Esc": "KEY_ESC", "Backspace": "KEY_BACKSPACE",
            "Tab": "KEY_TAB", "Space": "KEY_SPACE", "-": "KEY_MINUS",
            "=": "KEY_EQUAL", "[": "KEY_LEFTBRACE", "]": "KEY_RIGHTBRACE",
            "\\": "KEY_BACKSLASH", ";": "KEY_SEMICOLON",
            "'": "KEY_APOSTROPHE", "`": "KEY_GRAVE", ",": "KEY_COMMA",
            ".": "KEY_DOT", "/": "KEY_SLASH", "CapsLock": "KEY_CAPSLOCK",
            "F1": "KEY_F1", "F2": "KEY_F2", "F3": "KEY_F3", "F4": "KEY_F4",
            "F5": "KEY_F5", "F6": "KEY_F6", "F7": "KEY_F7", "F8": "KEY_F8",
            "F9": "KEY_F9", "F10": "KEY_F10", "F11": "KEY_F11", "F12": "KEY_F12",
            "PrintScreen": "KEY_SYSRQ", "ScrollLock": "KEY_SCROLLLOCK",
            "Pause": "KEY_PAUSE", "Ins": "KEY_INSERT", "Home": "KEY_HOME",
            "PgUp": "KEY_PAGEUP", "Del": "KEY_DELETE", "End": "KEY_END",
            "PgDown": "KEY_PAGEDOWN", "Right": "KEY_RIGHT",
            "Left": "KEY_LEFT", "Down": "KEY_DOWN", "Up": "KEY_UP",
            "NumLock": "KEY_NUMLOCK", "/": "KEY_KPSLASH", "*": "KEY_KPASTERISK",
            "-": "KEY_KPMINUS", "+": "KEY_KPPLUS", "Enter": "KEY_KPENTER",
            "1": "KEY_KP1", "2": "KEY_KP2", "3": "KEY_KP3", "4": "KEY_KP4",
            "5": "KEY_KP5", "6": "KEY_KP6", "7": "KEY_KP7", "8": "KEY_KP8",
            "9": "KEY_KP9", "0": "KEY_KP0", ".": "KEY_KPDOT",
            "Power": "KEY_POWER", "=": "KEY_KPEQUAL",
            "F13": "KEY_F13", "F14": "KEY_F14", "F15": "KEY_F15",
            "F16": "KEY_F16", "F17": "KEY_F17", "F18": "KEY_F18",
            "F19": "KEY_F19", "F20": "KEY_F20", "F21": "KEY_F21",
            "F22": "KEY_F22", "F23": "KEY_F23", "F24": "KEY_F24",
            "Execute": "KEY_OPEN", "Help": "KEY_HELP", "Menu": "KEY_PROPS",
            "Select": "KEY_FRONT", "Stop": "KEY_STOP", "Again": "KEY_AGAIN",
            "Undo": "KEY_UNDO", "Cut": "KEY_CUT", "Copy": "KEY_COPY",
            "Paste": "KEY_PASTE", "Find": "KEY_FIND", "Mute": "KEY_MUTE",
            "Volume Up": "KEY_VOLUMEUP", "Volume Down": "KEY_VOLUMEDOWN",
            "WWW": "KEY_MEDIA_WWW", "Back": "KEY_MEDIA_BACK",
            "Forward": "KEY_MEDIA_FORWARD", "Stop": "KEY_MEDIA_STOP",
            "Find": "KEY_MEDIA_FIND", "Scroll Up": "KEY_MEDIA_SCROLLUP",
            "Scroll Down": "KEY_MEDIA_SCROLLDOWN", "Edit": "KEY_MEDIA_EDIT",
            "Sleep": "KEY_MEDIA_SLEEP", "Coffee": "KEY_MEDIA_COFFEE",
            "Refresh": "KEY_MEDIA_REFRESH", "Calculator": "KEY_MEDIA_CALC",
            "(": "KEY_KPLEFTPAREN", ")": "KEY_KPRIGHTPAREN"
        }

        self.action_exit.triggered.connect(self.close)  # action quitter
        self.action_firmware.triggered.connect(self.load_firmware_dialog)  # on associe l'action modifier le firmware de l'Arduino
        self.action_code.triggered.connect(self.generate_code)  # action générer le code
        self.action_save.triggered.connect(lambda: self.save(save_under=False))  # action sauvegarder
        self.action_save_under.triggered.connect(lambda: self.save(save_under=True))  # action sauvegarder sous
        self.action_load.triggered.connect(self.load)  # action charger
        self.button_add.clicked.connect(self.add_command)  # bouton pour ajouter une commande
        self.button_delete_all.clicked.connect(self.delete_everything)  # bouton pour supprimer toutes les commandes
        self.button_sort.clicked.connect(self.sort)  # bouton pour trier les commandes par ordre alphabétique

        self.save_path = None  # dernier emplacement de sauvegarde
        self.commands = []  # liste de toutes les commandes dans l'ordre, chacune sous sa propre liste comme ceci : [commande, type_action, [objets_ui], [details_commande]]
        self.show()  # on montre la fenêtre
    
    def load_firmware_dialog(self):
        """On charge la boîte de dialogue pour gérer le firmware de l'Arduino et on gère la mise à jour du firmware"""
        self.dialog_firmware = Qt.QDialog()  # on définit un objet QDialog
        uic.loadUi("UI/firmware.ui", self.dialog_firmware)  # on charge le fichier UI
        self.dialog_firmware.button_firmware_normal.clicked.connect(lambda: self.change_firmware("normal"))  # on charge le firmware normal si on clique
        self.dialog_firmware.button_firmware_keyboard.clicked.connect(lambda: self.change_firmware("keyboard"))  # on charge le firmware clavier si on clique
        self.dialog_firmware.exec()  # on exécute la fenêtre
    
    def change_firmware(self, firmware:str):
        # on met le bon fichier selon le firmware demandé
        if firmware == "normal":
            self.firmware_path = 'Arduino-uno.hex'
        elif firmware == "keyboard":
            self.firmware_path = 'Arduino-keyboard.hex'
        else:
            raise ValueError(f'Invalid firmware : "{firmware}", must be "normal" or "keyboard"')
        
        self.dialog_firmware.button_firmware_normal.setEnabled(False)  # on désactive les boutons
        self.dialog_firmware.button_firmware_keyboard.setEnabled(False)
        thr_firmware = threading.Thread(target=self.change_firmware_thread)  # on crée et lance un thread pour changer le firmware afin de ne pas freeze l'UI
        thr_firmware.start()
    
    def change_firmware_thread(self):
        """Thread qui charge le firmware en parallèle"""
        program = os.getcwd() + "\\dfu-programmer\\dfu-programmer.exe"  # le chemin absolu vers l'exécutable dfu-programmer.exe
        # on change le firmware
        os.system(f'"{program}" atmega16u2 erase')
        os.system(f'"{program}" atmega16u2 flash --debug 1 dfu-programmer/{self.firmware_path}')
        os.system(f'"{program}" atmega16u2 reset')
        
        self.dialog_firmware.button_firmware_normal.setEnabled(True)  # on réactive les boutons
        self.dialog_firmware.button_firmware_keyboard.setEnabled(True)
    
    def sort(self):
        """Trie les commandes dans l'ordre alphabétique"""
        self.commands.sort(key=lambda l: l[0])  # on trie la liste selon les commandes
        self.refresh_widgets()  # on recharge les widgets
    
    def add_command(self):
        """Ajouter une commande à l'interface"""
        index = len(self.commands)  # index de la commande dans la liste
        self.commands.append(["nouvelle commande", "Aucun", [], []])  # on crée une nouvelle commande sans action
        # on définis le widgets propres à cette commande et on les place à la fin de la grille
        self.create_line_widgets(index)
    
    def create_line_widgets(self, index:int):
        """Crée dans la liste et place les widgets de la commande à l'indexe désigné sur la ligne correspondante"""
        line = index * 2 + 4  # ligne de la grille sur laquelle on met le widget
        self.commands[index][2] = []  # on vide si besoin les objets widgets de la liste
        widgets = self.commands[index][2]  # on crée une référence à la sous-liste des widgets pour raccourcir la suite du code

        # on crée tous les objets widget et on les stocke dans une sous-liste de la liste de la commande
        widgets.append(Qt.QLineEdit("nouvelle commande"))  # zone de saisie de texte
        widgets[0].editingFinished.connect(lambda: self.change_command(index))  # changer le nom de la commande
        widgets.append(Qt.QLabel(self.normalize_command(index, "nouvelle commande")))  # nom de la fonction pour l'Arduino
        widgets[1].setAlignment(QtCore.Qt.AlignCenter)  # alignement du label
        widgets[1].setFont(QtGui.QFont("Arial", 11))  # police d'écriture et taille du label
        widgets[1].setWordWrap(True)  # autorise le texte en plusieurs lignes
        widgets.append(Qt.QLabel("Aucun"))  # label de l'action
        widgets[2].setAlignment(QtCore.Qt.AlignCenter)  # alignement du label
        widgets[2].setFont(QtGui.QFont("Arial", 11))  # police d'écriture et taille du label
        widgets[2].setWordWrap(True)  # autorise le texte en plusieurs lignes
        widgets.append(Qt.QPushButton("Modifier"))  # bouton modifier
        widgets[3].clicked.connect(lambda: self.modify_command(index))  # fonction pour modifier
        widgets.append(Qt.QPushButton("Supprimer"))  # bouton supprimer
        widgets[4].clicked.connect(lambda: self.delete_command(index))  # fonction pour supprimer
        widgets.append(Qt.QFrame())  # ligne de séparation
        widgets[5].setFrameShape(Qt.QFrame.HLine)
        widgets[5].setFrameShadow(Qt.QFrame.Sunken)
        
        # on place les widgets dans l'UI dans la bonne ligne selon leur index
        for k in range(5):
            self.grid_layout.addWidget(widgets[k], line, k*2)  # on ajoute les widgets à l'écran
        self.grid_layout.addWidget(widgets[5], line-1, 0, 1, -1)  # séparateur
    
    def change_command(self, index:int, new_command:str=None):
        """Changer le nom d'une commande"""
        if new_command:  # on change directement la commande si elle est fournie
            self.commands[index][0] = new_command
            self.commands[index][2][0].setText(new_command)
            self.commands[index][2][1].setText(self.normalize_command(index, new_command))
        else:  # sinon on la prend de la fenêtre principale
            new_name = self.commands[index][2][0].text()  # on récupère le nouveau nom
            self.commands[index][0] = new_name  # on actualise le nom de la commande dans la liste principale
            self.commands[index][2][1].setText(self.normalize_command(index, new_name))  # on met le nouveau nom de la fonction
        self.refresh_widgets()
    
    def delete_everything(self):
        """Supprimer toutes les commandes et widgets associés si confirmation"""
        if self.ask_confirm("Voulez-vous vraiment supprimer toutes les commandes ?"):
            self.delete_widgets()  # on supprime les widgets des commandes
            self.commands = []  # on supprime les données
    
    def ask_confirm(self, text:str="Êtes-vous sûr ?", yes:str="Oui", no:str="Annuler") -> bool:
        """Fait apparaître une boîte de dialogue qui demande une confirmation, renvoie True si validé et False si annulé"""
        msgBox = Qt.QMessageBox()
        msgBox.setIcon(Qt.QMessageBox.Question)
        msgBox.setWindowTitle("Confirmation")
        msgBox.setText(text)
        msgBox.setStandardButtons(Qt.QMessageBox.Yes | Qt.QMessageBox.Cancel)
        button_yes = msgBox.button(Qt.QMessageBox.Yes)
        button_no = msgBox.button(Qt.QMessageBox.Cancel)
        button_yes.setText(yes)
        button_no.setText(no)
        msgBox.setDefaultButton(button_no)
        answer = msgBox.exec()
        return answer == Qt.QMessageBox.Yes  # renvoie True si l'action est confirmée, False si elle est annulée
    
    def load_from_list(self):
        """Charge l'interface (qui doit être vide) en mettant tous les widgets de la liste principale, selon le format habituel"""
        for i in range(len(self.commands)):
            self.create_line_widgets(i)  # on crée l'UI petit à petit en répétant une section pour chaque commande
            self.commands[i][2][0].setText(self.commands[i][0])  # on met le nom de la commande dans la zone de texte
            self.commands[i][2][1].setText(self.normalize_command(i, self.commands[i][0]))  # on met le nom de la fonction dans le label
            self.commands[i][2][2].setText(self.get_action_display(i))  # on met l'action dans le label descriptif de la commande
    
    def delete_command(self, index:int):
        """Supprime une commande"""
        if self.ask_confirm(f'Voulez-vous vraiment supprimer la commande "{self.commands[index][0]}" ?'):  # on demande confirmation
            self.delete_widgets()  # on supprime les widgets à l'écran
            self.commands.pop(index)  # on retire les données de la commande à supprimer de la liste principale
            self.load_from_list()  # on recharge toute l'UI avec la nouvelle liste sans la commande
    
    def delete_widgets(self):
        """Supprime tous les widgets liés aux commandes, mais pas les données"""
        for command in self.commands:
                for widget in command[2]:
                    widget.deleteLater()  # on supprime tous les widgets de l'UI

    def refresh_widgets(self):
        """Actualise les widgets à l'écran"""
        self.delete_widgets()
        self.load_from_list()
    
    def modify_command(self, index:int):
        """Modifie l'action réalisée par une commande"""
        self.dialog_modify = Qt.QDialog()  # on définit un objet QDialog
        uic.loadUi("UI/command.ui", self.dialog_modify)  # on charge le fichier UI
        actions = ["Aucun", "Sortie digitale", "Sortie analogue", "Led rgb", "Raccourcis clavier"]  # liste pour avoir les index des actions
        self.dialog_modify.finished.connect(self.refresh_widgets)  # on actualise l'affichage
        self.dialog_modify.command_name.setText(self.commands[index][0])  # on met le nom de la commande
        self.dialog_modify.command_name.editingFinished.connect(lambda: self.change_command(index, self.dialog_modify.command_name.text()))  # changer le nom de la commande
        self.dialog_modify.action_choice.currentIndexChanged.connect(lambda: self.change_action(index, self.dialog_modify.action_choice.currentText()))  # fonction à appeler quand on choisit une action
        self.dialog_modify.action_choice.setCurrentIndex(actions.index(self.commands[index][1]))  # on met sur la bonne action
        self.dialog_modify.exec()  # on exécute la fenêtre
    
    def change_action(self, index:int, action:str):
        """Change l'action d'une commande"""
        keep_values = action == self.commands[index][1]  # si on reprend la même action ou si on change
        self.commands[index][1] = action  # on actualise les données
        self.clear_layout(self.dialog_modify.options_layout)

        if action == "Aucun":
            self.commands[index][3] = []  # fonction vide
            label = Qt.QLabel("La fonction dans le code sera vide")
            self.dialog_modify.options_layout.addWidget(label)  # création du label
            label.setAlignment(QtCore.Qt.AlignCenter)  # alignement du label
            label.setWordWrap(True)  # autorise le texte en plusieurs lignes
        
        elif action == "Sortie digitale":
            if not keep_values:
                self.commands[index][3] = ["2", "ON"]  # broche et état du signal
            label1 = Qt.QLabel("Broche :")
            self.dialog_modify.options_layout.addWidget(label1, 0, 0)  # création du label
            label1.setAlignment(QtCore.Qt.AlignRight)  # alignement du label
            label1.setWordWrap(True)  # autorise le texte en plusieurs lignes
            label2 = Qt.QLabel("Sortie :")
            self.dialog_modify.options_layout.addWidget(label2, 1, 0)  # création du label
            label2.setAlignment(QtCore.Qt.AlignRight)  # alignement du label
            label2.setWordWrap(True)  # autorise le texte en plusieurs lignes

            combo_box1 = Qt.QComboBox()
            combo_box1.addItems([str(k) for k in range(2, 14)] + ["A"+str(k) for k in range(0, 6)])  # liste des ports utilisables
            combo_box1.setCurrentText(self.commands[index][3][0])
            combo_box1.currentIndexChanged.connect(lambda i: self.commands[index][3].__setitem__(0, combo_box1.itemText(i)))  # on change la broche
            self.dialog_modify.options_layout.addWidget(combo_box1, 0, 1)
            combo_box2 = Qt.QComboBox()
            combo_box2.addItems(["ON", "OFF"])  # liste des états possibles
            combo_box2.setCurrentText(self.commands[index][3][1])
            combo_box2.currentIndexChanged.connect(lambda i: self.commands[index][3].__setitem__(1, combo_box2.itemText(i)))  # on change l'état
            self.dialog_modify.options_layout.addWidget(combo_box2, 1, 1)
        
        elif action == "Sortie analogue":
            if not keep_values:
                self.commands[index][3] = ["3", 0]  # broche et intensité du signal
            label1 = Qt.QLabel("Broche :")
            self.dialog_modify.options_layout.addWidget(label1, 0, 0)  # création du label
            label1.setAlignment(QtCore.Qt.AlignRight)  # alignement du label
            label1.setWordWrap(True)  # autorise le texte en plusieurs lignes
            label2 = Qt.QLabel("Intensité 0-255 :")
            self.dialog_modify.options_layout.addWidget(label2, 1, 0)  # création du label
            label2.setAlignment(QtCore.Qt.AlignRight)  # alignement du label
            label2.setWordWrap(True)  # autorise le texte en plusieurs lignes

            combo_box = Qt.QComboBox()
            combo_box.addItems(["3","5","6","9","10","11"])  # liste des ports utilisables
            combo_box.setCurrentText(self.commands[index][3][0])
            combo_box.currentIndexChanged.connect(lambda i: self.commands[index][3].__setitem__(0, combo_box.itemText(i)))  # on change la broche
            self.dialog_modify.options_layout.addWidget(combo_box, 0, 1)
            spin_box = Qt.QSpinBox()
            spin_box.setMinimum(0)
            spin_box.setMaximum(255)
            spin_box.setValue(self.commands[index][3][1])
            spin_box.valueChanged.connect(lambda i: self.commands[index][3].__setitem__(1, spin_box.value()))  # on change l'intensité
            self.dialog_modify.options_layout.addWidget(spin_box, 1, 1)
        
        elif action == "Led rgb":
            if not keep_values:
                self.commands[index][3] = [[0, 0, 0], ["3", "5", "6"]]  # valeurs R, G et B et broches
            label1 = Qt.QLabel("Rouge :")
            self.dialog_modify.options_layout.addWidget(label1, 0, 0)  # création du label
            label1.setAlignment(QtCore.Qt.AlignRight)  # alignement du label
            label1.setWordWrap(True)  # autorise le texte en plusieurs lignes
            spin_box1 = Qt.QSpinBox()
            spin_box1.setMinimum(0)
            spin_box1.setMaximum(255)
            spin_box1.setValue(self.commands[index][3][0][0])
            spin_box1.valueChanged.connect(lambda i: self.commands[index][3][0].__setitem__(0, spin_box1.value()))  # on change la valeur R
            self.dialog_modify.options_layout.addWidget(spin_box1, 0, 1)
            combo_box1 = Qt.QComboBox()
            combo_box1.addItems(["3","5","6","9","10","11"])  # liste des ports utilisables
            combo_box1.setCurrentText(self.commands[index][3][1][0])
            combo_box1.currentIndexChanged.connect(lambda i: self.commands[index][3][1].__setitem__(0, combo_box1.itemText(i)))  # on change la broche
            self.dialog_modify.options_layout.addWidget(combo_box1, 0, 2)
            
            label2 = Qt.QLabel("Vert :")
            self.dialog_modify.options_layout.addWidget(label2, 1, 0)  # création du label
            label2.setAlignment(QtCore.Qt.AlignRight)  # alignement du label
            label2.setWordWrap(True)  # autorise le texte en plusieurs lignes
            spin_box2 = Qt.QSpinBox()
            spin_box2.setMinimum(0)
            spin_box2.setMaximum(255)
            spin_box2.setValue(self.commands[index][3][0][1])
            spin_box2.valueChanged.connect(lambda i: self.commands[index][3][0].__setitem__(1, spin_box2.value()))  # on change la valeur G
            self.dialog_modify.options_layout.addWidget(spin_box2, 1, 1)
            combo_box2 = Qt.QComboBox()
            combo_box2.addItems(["3","5","6","9","10","11"])  # liste des ports utilisables
            combo_box2.setCurrentText(self.commands[index][3][1][1])
            combo_box2.currentIndexChanged.connect(lambda i: self.commands[index][3][1].__setitem__(1, combo_box2.itemText(i)))  # on change la broche
            self.dialog_modify.options_layout.addWidget(combo_box2, 1, 2)
            
            label3 = Qt.QLabel("Bleu :")
            self.dialog_modify.options_layout.addWidget(label3, 2, 0)  # création du label
            label3.setAlignment(QtCore.Qt.AlignRight)  # alignement du label
            label3.setWordWrap(True)  # autorise le texte en plusieurs lignes
            spin_box3 = Qt.QSpinBox()
            spin_box3.setMinimum(0)
            spin_box3.setMaximum(255)
            spin_box3.setValue(self.commands[index][3][0][2])
            spin_box3.valueChanged.connect(lambda i: self.commands[index][3][0].__setitem__(2, spin_box3.value()))  # on change la valeur B
            self.dialog_modify.options_layout.addWidget(spin_box3, 2, 1)
            combo_box3 = Qt.QComboBox()
            combo_box3.addItems(["3","5","6","9","10","11"])  # liste des ports utilisables
            combo_box3.setCurrentText(self.commands[index][3][1][2])
            combo_box3.currentIndexChanged.connect(lambda i: self.commands[index][3][1].__setitem__(2, combo_box3.itemText(i)))  # on change la broche
            self.dialog_modify.options_layout.addWidget(combo_box3, 2, 2)
        
        elif action == "Raccourcis clavier":

            corres = {"Ctrl":0, "Shift":1, "Alt":2, "Meta":3}
            complete_special_keys = ["Ctrl gauche", "Shift gauche", "Alt gauche", "Windows gauche", "Ctrl droit", "Shift droit", "Alt droit", "Windows droit"]

            def generate_callback(elem):
                """Règle un problème avec la variable elem qui ne prend que la dernière valeur"""
                return lambda state: change_modif_shortcut(state, elem)
            
            def change_modif_shortcut(state, key):
                """Actualise les données pour les cases à cocher"""
                if state == QtCore.Qt.Checked:
                    if key not in self.commands[index][3][0]:
                        self.commands[index][3][0].append(key)
                else:
                    self.commands[index][3][0].remove(key)
            
            def change_keys():
                """Actualise les données et les cases à cocher avec le nouveau raccourcis entré"""
                str_keys = key_sequence.keySequence().toString()  # commande au format "special1+special2+normal1, special1+special2+normal2, ..."
                ls_keys = str_keys.split(", ")
                normal_keys = [k.split("+")[-1] for k in ls_keys]  # touches normales
                modif_keys = ls_keys[0].split("+")[:-1]  # touches spéciales
                for k in modif_keys:
                    checkboxes[corres[k]].setChecked(True)  # on coche les touches spéciales si besoin
                if normal_keys[0]:
                    self.commands[index][3][1] = normal_keys
                else:
                    self.commands[index][3][1] = []
                if modif_keys:  # on change le contenu uniquement si des touches spéciales sont à enlever
                    key_sequence.setKeySequence(", ".join(normal_keys))

            if not keep_values:
                self.commands[index][3] = [[], []]  # touches de modification et touches normales, en str
            key_sequence = Qt.QKeySequenceEdit()
            key_sequence.setKeySequence(", ".join(self.commands[index][3][1]))
            key_sequence.keySequenceChanged.connect(lambda: change_keys())
            self.dialog_modify.options_layout.addWidget(key_sequence, 0, 0, 1, 2)  # on place la zone de raccourcis
            checkboxes = []
            for i in range(len(complete_special_keys)):
                checkboxes.append(Qt.QCheckBox(complete_special_keys[i]))  # on crée toutes les cases à cocher
                if complete_special_keys[i] in self.commands[index][3][0]:
                    checkboxes[-1].setChecked(True)
                checkboxes[-1].stateChanged.connect(generate_callback(complete_special_keys[i]))
                self.dialog_modify.options_layout.addWidget(checkboxes[-1], (i%4)+1, i//4)  # on place les raccourcis
        
        else:  # si l'action n'est pas référencée (ne devrais pas arriver, mais prévu au cas où)
            self.commands[index][3] = []
            label = Qt.QLabel("Erreur : cette fonctionnalité n'est pas présente dans le code")
            self.dialog_modify.options_layout.addWidget(label)  # création du label
            label.setAlignment(QtCore.Qt.AlignCenter)  # alignement du label
            label.setWordWrap(True)  # autorise le texte en plusieurs lignes
    
    def get_action_display(self, index:int) -> str:
        """renvoie le texte à placer dans le label décrivant l'action de la commande"""
        action = self.commands[index][1]  # type de l'action
        parameters = self.commands[index][3]  # paramètres de l'action
        if action == "Aucun":
            return "Aucun"
        elif action == "Sortie digitale":
            return f"Sortie en {parameters[1]} broche {parameters[0]}"
        elif action == "Sortie analogue":
            return f"Sortie analogue {parameters[1]} broche {parameters[0]}"
        elif action == "Led rgb":
            return f"Led RGB valeurs {parameters[0][0]}, {parameters[0][1]}, {parameters[0][2]} ports {parameters[1][0]}, {parameters[1][1]}, {parameters[1][2]}"
        elif action == "Raccourcis clavier":
            return f"Raccourcis clavier {'+'.join(parameters[0])} / {'+'.join(parameters[1])}"
    
    def normalize_command(self, index:int, command:str=None) -> str:
        """Formate la commande de sorte qu'elle soit unique et compatible pour créer une fonction Arduino"""
        if not command:
            command = self.commands[index][2][0].text()  # on prend la commande de la zone de texte si aucune n'est donnée
        valid_chars = [chr(k) for k in range(48, 58)] + [chr(k) for k in range(65, 91)] + [chr(k) for k in range(97, 123)] + ["_"]
        if not command:
            command = "fonction"
        command = command.replace(" ", "_")
        new_command = ""
        for c in command:
            if c in valid_chars:
                new_command += c
        while True:
            if new_command:
                if new_command[0] in [chr(k) for k in range(48, 58)]:
                    new_command = new_command[1:]
                else:
                    break
            else:
                new_command = "fonction"
                break
        other_func = [self.commands[i][2][1].text() for i in range(len(self.commands)) if i != index and len(self.commands[i][2]) > 1]
        while new_command in other_func:
            end_part = new_command.split("_")[-1]
            if all([k in [chr(k) for k in range(48, 58)] for k in end_part]):  # si on a un format avec un trait du bas et un nombre à la fin
                new_command = "_".join(new_command.split("_")[:-1]) + "_" + str(int(new_command.split("_")[-1]) + 1)  # on augmente le nombre à la fin
            else:
                new_command += "_1"  # sinon on met "_1" à la fin
        return new_command
    
    def clear_layout(self, layout:Qt.QLayout):
        """Supprime tous les widgets du layout donné"""
        while layout.count():  # tant qu'il reste des widgets
            layout.takeAt(0).widget().deleteLater()  # on supprime le widget
    
    def save_file(self, content:str, ext:str=".*", desc:str="Fichier", path:str=None) -> str:
        """Enregistrer un fichier et renvoie son chemin"""
        types = [(desc, ext), ("Fichier texte", ".txt")]
        if ext != ".*":
            types.append(("Fichier", ".*"))
        if not path:
            file = filedialog.asksaveasfile(defaultextension=ext, filetypes=types)
            if file:
                path = file.name
                file.close()
            saved = bool(file)
        else:
            saved = True
        if saved:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return path
    
    def save(self, save_under:bool=False):
        """Enregistre un nouveau fichier"""
        if save_under:
            path = None
        else:
            path = self.save_path
        self.save_path = self.save_file(str([[cmd[0], cmd[1], [], cmd[3]] for cmd in self.commands]), ext=".sav", desc="Fichier de sauvegarde", path=path)
    
    def load(self):
        """Charger un fichier"""
        file = filedialog.askopenfile(mode ='r', defaultextension=".sav", filetypes =[('Fichier de sauvegarde', '.sav'), ("Fichier", ".*")])
        if file:
            self.delete_widgets()
            self.save_path = None
            self.commands = eval(file.read())
            self.load_from_list()
    
    def generate_code(self):
        """Génère le code ardunino et affiche la fenêtre correspondante"""
        with open("structure.ino", "r", encoding="utf-8") as f:
            self.code = f.read()
        # à remplacer : "// pinmodes ici", "// appels fonctions ici", "// definir fonctions ici"
        pinmodes, func_call, func_def = "", "", ""  # morceaux de code à insérer

        for command in self.commands:  # boucle pour chaque commande
            func_call += 'if (voice == "' + command[0] + '") {\n            ' + command[2][1].text() + '();\n        }\n        '
            func_def += 'void ' + command[2][1].text() + '() {\n    '
            
            if command[1] == "Aucun":
                func_def += '// insérer code ici\n}\n'
            
            elif command[1] == "Sortie digitale":
                pinmodes += f'pinMode({command[3][0]}, OUTPUT);\n    '
                func_def += 'digitalWrite(' + command[3][0] + ', '
                if command[3][1] == "ON":
                    func_def += "HIGH"
                else:
                    func_def += "LOW"
                func_def += ');\n}\n'
            
            elif command[1] == "Sortie analogue":
                pinmodes += f'pinMode({command[3][0]}, OUTPUT);\n    '
                func_def += 'analogWrite(' + command[3][0] + ', '+ str(command[3][1]) + ');\n}\n'
            
            elif command[1] == "Led rgb":
                for i in range(3):
                    pinmodes += f'pinMode({command[3][1][i]}, OUTPUT);\n    '
                    func_def += 'analogWrite(' + command[3][1][i] + ', '+ str(command[3][0][i]) + ');\n}\n'
            
            elif command[1] == "Raccourcis clavier":
                if command[3][0]:  # si touches de modification
                    func_def += 'buf[0] = ' + ' | '.join([self.dict_keys[t] for t in command[3][0]]) + ';\n    '
                if command[3][1]:  # si touches normales
                    for i in range(len(command[3][1])):
                        func_def += 'buf[' + str(i+2) + '] = ' + self.dict_keys[command[3][1][i]] + ';\n    '
                func_def += '\n    Serial.write(buf, 8);\n    delayReleaseKey(100);\n}\n'
         
        self.code = self.code.replace("// pinmodes ici", pinmodes)
        self.code = self.code.replace("// appels fonctions ici", func_call)
        self.code = self.code.replace("// definir fonctions ici", func_def)
        
        self.dialog_code = Qt.QDialog()
        uic.loadUi("UI/code.ui", self.dialog_code)
        self.dialog_code.text_display.setFontFamily("Monospace")
        self.dialog_code.text_display.setText(self.code)
        self.dialog_code.button_copy.clicked.connect(lambda: pyperclip.copy(self.code))
        self.dialog_code.button_save.clicked.connect(lambda: self.save_file(self.code, ext=".ino", desc="Code Arduino"))
        self.dialog_code.exec()


if __name__ == "__main__":  # si on lance le programme directement
    App = Qt.QApplication([])  # on instancie la classe de l'application
    Window = MainGUI()  # on instancie la classe de la fenêtre principale
    App.exec_()  # on exécute l'application
