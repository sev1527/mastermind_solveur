# -*- coding: utf-8 -*-
"""
Une fenêtre graphique pour résoudre les combinaisons de Mastermind.
Créé par sev1527.
Dépot GitHub : https://github.com/sev1527/mastermind_solveur
"""
from tkinter import Tk, Button, Label, Frame, Checkbutton, IntVar, Toplevel, PhotoImage, Canvas
from tkinter.colorchooser import askcolor
from tkinter.messagebox import showwarning, askyesno, showinfo
import webbrowser
from copy import deepcopy
from requests import get

VERSION = "1.3"
SWITCH_BG = b'iVBORw0KGgoAAAANSUhEUgAAACMAAAAPCAYAAABut3YUAAABhWlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV9TtSIVRQuKOASsTnZREcdSxSJYKG2FVh1MLv2CJg1Jiouj4Fpw8GOx6uDirKuDqyAIfoC4ujgpukiJ/0sKLWI9OO7Hu3uPu3eAUCsx1ewIA6pmGYloRExnVkXfK7owgH6MYUhiph5LLqbQdnzdw8PXuxDPan/uz9GrZE0GeETiMNMNi3iDeHbT0jnvEwdYQVKIz4knDbog8SPXZZffOOcdFnhmwEgl5okDxGK+heUWZgVDJZ4hDiqqRvlC2mWF8xZntVRhjXvyF/qz2kqS6zRHEcUSYohDhIwKiijBQohWjRQTCdqPtPGPOP44uWRyFcHIsYAyVEiOH/wPfndr5qan3CR/BOh8se2PccC3C9Srtv19bNv1E8D7DFxpTX+5Bsx9kl5tasEjoG8buLhuavIecLkDDD/pkiE5kpemkMsB72f0TRlg8BboWXN7a+zj9AFIUVfLN8DBITCRp+z1Nu/ubu3t3zON/n4AsDFyv15TgvoAAAAGYktHRAD/AP8A/6C9p5MAAAAJcEhZcwAALiMAAC4jAXilP3YAAAAHdElNRQfnBhIRACZ9LKeUAAAAGXRFWHRDb21tZW50AENyZWF0ZWQgd2l0aCBHSU1QV4EOFwAAAiFJREFUSMftlc9Lk3Ecx197nmebe1pzLrdniQwa5mK0WUvcIYTo0kFCD4NACKG7IAT+A90jQdrJLvPkJcSLBEGHjrbHaozlyg6b2NzUkXO/t6dD8Ii0g0OIoj6n95fP9/P9vvh833y+hkfanMY544XhGVo4fN5jEPiD4t+GWSsUGNnYYDmXO6UBpN8N8zST4VUwiMtk4q6q6voXmOLWAYmoSmEzx1DkGr6Z6xitJsrfjkk8j3PRYyO9ksIZUrjxeAyLU+544Va5THRnh81SiYjLxYzbjVUUeZhM8qZex62q+l63qpIKBPDJ8skz1Q6rvJ17TXD2FvfXH2BxX+DjYlwvSjx5hyPgZGItgjJ2mS8rqY4gh80mc+k0s4ODrI+M4DaZWMxmAYj5/dw2GimNjqKFw7r2yfJpzxwkCwxP+7F57YhmkSuTV/kUS9Ao1QFQJgZRwgOIZhElPEDx82FHmOTxMdOKgtdiwSwITPb3E8vnKbVaZzdwdb+CxXXSdkEScIYUGkc/YWxeu54ziAJaq/N42m80dA8ASAYDIVnmqBsYs72Hyl5ZT7SbbfLxHJJs7Mqgdklir17X101NI14uIwvC2WEuBZwkl97zfbtIq9bi62oa79Qwpl5zVzABq5Wl3V22KxVq7TarhQJTDge9ktRFZ/p6uBO9x4eFDV6OL1PKHHFzvvsR3ydJRH0+FrJZxlWVTLXKvMdzplrD/7/pb4D5AbXOw0DY3yi5AAAAAElFTkSuQmCC'
SWITCH_FG = b'iVBORw0KGgoAAAANSUhEUgAAABEAAAAPCAYAAAACsSQRAAABhWlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV9TtSIVRQuKOASsTnZREcdSxSJYKG2FVh1MLv2CJg1Jiouj4Fpw8GOx6uDirKuDqyAIfoC4ujgpukiJ/0sKLWI9OO7Hu3uPu3eAUCsx1ewIA6pmGYloRExnVkXfK7owgH6MYUhiph5LLqbQdnzdw8PXuxDPan/uz9GrZE0GeETiMNMNi3iDeHbT0jnvEwdYQVKIz4knDbog8SPXZZffOOcdFnhmwEgl5okDxGK+heUWZgVDJZ4hDiqqRvlC2mWF8xZntVRhjXvyF/qz2kqS6zRHEcUSYohDhIwKiijBQohWjRQTCdqPtPGPOP44uWRyFcHIsYAyVEiOH/wPfndr5qan3CR/BOh8se2PccC3C9Srtv19bNv1E8D7DFxpTX+5Bsx9kl5tasEjoG8buLhuavIecLkDDD/pkiE5kpemkMsB72f0TRlg8BboWXN7a+zj9AFIUVfLN8DBITCRp+z1Nu/ubu3t3zON/n4AsDFyv15TgvoAAAAGYktHRAD/AP8A/6C9p5MAAAAJcEhZcwAALiMAAC4jAXilP3YAAAAHdElNRQfnBhIRARJFg2JgAAAAGXRFWHRDb21tZW50AENyZWF0ZWQgd2l0aCBHSU1QV4EOFwAAAURJREFUOMuNk9GSgyAMRU8Q7QyF+p3dv+/gusVOyT6AqJ3ZbvMSkCTee5PI1/WqCogIKCCAKogACiogm1eV8tTewIbLhXe21n1n9uw98lfo/rNSEO2j68GGswcDqBQmUsK0Zu/PqCJIo6wC+ZmxpjMMw0BnO4wYPrWcM4/Hwj0nWlZnOk6nE957QgiEELjdbnjviw+BEDzOOfqhR8RAwYVV2DpRuzQMA7bvAQghAHB2jmV5kHPaOlbNAIjWdlUVCrIC0jnXiq+JgpYO1zqmYTjW4JkzAD/zXDXdWtVEF1AV7EpDV58zaVlYUgIgThMA3/N8nEPWi2K10tCspJRINRlgHEdijIzjyBQjm3I7ZApWNXNPCVKqf9JG6zApW07Vr00Pdqpw9wP6Mpf8txeHIh8vy+vuxBiPK9KE27Z0Fb5QOu6OAr/VG6nSwUWKFwAAAABJRU5ErkJggg=='

combinaisons = []
combinaisons_double = []
couleurs = ["#e40000", "#0067ff", "#909090", "#00df2d", "#ff21d4", "#ffffff", "#ff8a00", "#f4f700"]
items = list(range(8))

def double(liste):
    """
    Y a-t-il un double dans la liste ?
    """
    for i in range(len(liste)):
        liste_sans = liste[0:i]+liste[i+1:len(liste)]
        if liste[i] in liste_sans:
            return True
    return False

for i1 in items:
    for i2 in items:
        for i3 in items:
            for i4 in items:
                comb = [i1, i2, i3, i4]
                combinaisons_double.append(comb)
                if not double(comb):
                    combinaisons.append(comb)

def _noter(item, liste):
    note = 0
    for i in liste:
        for couleur in range(len(item)):
            if item[couleur] == i[couleur]:
                note += 5
            elif item[couleur] in i:
                note += 1
    return note

def calculer(liste, utiliser_doubles):
    """
    Calculer toutes les possibilités possibles avec les contraintes indiquée.
    """
    if utiliser_doubles:
        liste_utilise = combinaisons_double
    else:
        liste_utilise = combinaisons
    retours = []
    for combinaison in liste_utilise:
        marche = True
        for entree in liste:
            nb_places = 0
            nb_bons = 0
            decalage = 0
            copie_combinaison = deepcopy(combinaison)
            copie_entree = deepcopy(entree)[0:len(combinaison)]
            for i in range(len(copie_combinaison)):
                if copie_entree[i-decalage] == copie_combinaison[i-decalage]:
                    del copie_combinaison[i-decalage]
                    del copie_entree[i-decalage]
                    nb_places += 1
                    decalage += 1
            decalage = 0
            for i in range(len(copie_combinaison)):
                if copie_combinaison[i-decalage] in copie_entree:
                    del copie_entree[copie_entree.index(copie_combinaison[i-decalage])]
                    del copie_combinaison[i-decalage]
                    nb_bons += 1
                    decalage += 1
            if entree[-2] != nb_bons or entree[-1] != nb_places:
                marche = False
        if marche:
            retours.append(combinaison)

    nretours = []
    for retour in retours:
        note = _noter(retour, retours)
        nretours.append(retour+[note])
    return trier(nretours, -1, False)

def trier(liste, key, croissant=True):
    """
    Trie les items de la liste.
    """
    nouvelle_liste = []
    for en_traitement in liste:
        fin = True
        for ligne, i_ligne in zip(nouvelle_liste, range(len(nouvelle_liste))):
            if en_traitement[key] < ligne[key]:
                nouvelle_liste.insert(i_ligne, en_traitement)
                fin = False
                break
        if fin:
            nouvelle_liste.append(en_traitement)
    if croissant:
        return nouvelle_liste
    return list(reversed(nouvelle_liste))

def fonction(fonct, *args, **kwargs):
    """
    Transforme une fonction en lambda.
    """
    def retour(*_):
        fonct(*args, **kwargs)
    return retour


class InfoBulle(Toplevel):
    """
    Inspiré de https://www.developpez.net/forums/d241112/autres-langages/python/gui/tkinter/info-bulle-tkinter/#post_1542643
    """
    def __init__(self, master, texte='', temps=1000):
        super().__init__(master, bd=1, bg='black')
        self.tps = temps
        self.master = master
        self.withdraw()
        self.overrideredirect(1)
        self.transient()
        label = Label(self, text=texte, bg="ghost white", justify='left')
        label.update_idletasks()
        label.pack()
        label.update_idletasks()
        self.tipwidth = label.winfo_width()
        self.tipheight = label.winfo_height()
        self.master.bind('<Enter>', self._delai)
        self.master.bind('<Button-1>', self._efface)
        self.master.bind('<Leave>', self._efface)
    def _delai(self, _):
        self.action = self.master.after(self.tps, self._affiche)
    def _affiche(self):
        self.update_idletasks()
        posx = self.master.winfo_rootx() + self.master.winfo_width()
        posy = self.master.winfo_rooty() + self.master.winfo_height()
        if posx + self.tipwidth > self.winfo_screenwidth():
            posx = posx - self.winfo_width() - self.tipwidth
        if posy + self.tipheight > self.winfo_screenheight():
            posy = posy - self.winfo_height() - self.tipheight
        #~ print posX,print posY
        self.geometry(f"+{posx}+{posy}")
        self.deiconify()
    def _efface(self, _):
        self.withdraw()
        self.master.after_cancel(self.action)


class Fen(Tk):
    """
    La fenêtre principale du programme.
    """
    def __init__(self):
        super().__init__()
        self.title("Solveur de Mastermind")
        self.images = {
            "switch_bg": PhotoImage(data=SWITCH_BG),
            "switch_fg": PhotoImage(data=SWITCH_FG),
        }

        frame = Frame(self)
        frame.pack()
        Label(frame, text=f"Solveur de Mastermind {VERSION}  ", font="Arial 18").pack(side="left")
        bouton = Button(frame, text="🗘", command=self.mise_a_jour)
        bouton.pack(side="left")
        InfoBulle(bouton, "Rechercher les mises à jour")
        bouton = Button(frame, text="ⓘ", command=self.a_propos)
        bouton.pack(side="left")
        InfoBulle(bouton, "À propos")
        self.boutons = []
        self.but_f = Frame(self)
        self.but_f.pack()
        for ligne in range(5):
            frame = Frame(self.but_f)
            frame.pack()
            self.boutons.append([])
            for i in range(4):
                bouton = Button(frame, text="\n", bg=couleurs[0], width=5,
                                command=fonction(self.bouton_couleur_reception, ligne, i))
                bouton.pack(side="left")
                self.boutons[-1].append(bouton)

            Label(frame).pack(side="left")
            for couleur in ["white", "red"]:
                bouton = Button(frame, text="0", bg=couleur, height=2, width=5,
                             command=fonction(self.bouton_valeur, ligne, len(self.boutons[-1])))
                bouton.pack(side="left")
                self.boutons[-1].append(bouton)
            
            Label(frame).pack(side="left")
            switch = Canvas(frame, height=self.images["switch_bg"].height(),
                                   width=self.images["switch_bg"].width())
            switch.create_image(self.images["switch_bg"].width()//2+1,
                                self.images["switch_bg"].height()//2+1,
                                image=self.images["switch_bg"])
#                         command=fonction(self.bouton_activer, ligne, len(self.boutons[-1])))
            switch.bind("<Button>", fonction(self.bouton_activer, ligne, len(self.boutons[-1])))
            switch.state = False
            switch.affiche = switch.create_image(self.images["switch_fg"].width()//2+1,
                                                 self.images["switch_fg"].height()//2+1,
                                                 image=self.images["switch_fg"])
            switch.pack(side="left")
            self.boutons[-1].append(switch)

        Label(self).pack()
        self.boutons_couleur = []
        frame = Frame(self)
        frame.pack()
        for i in range(8):
            bouton = Button(frame, text="\n", bg=couleurs[i], width=5,
                       command=fonction(self.bouton_couleur_selection, i))
            bouton.pack(side="left")
            self.boutons_couleur.append(bouton)
        self.id_couleur = 0
        self.boutons_couleur[self.id_couleur].config(relief="sunken")
        bouton = Button(frame, text="Modifier", width=10, height=2,
                   command=self.bouton_couleur_modification)
        bouton.pack(side="left")
        InfoBulle(bouton, "Modifier la couleur active")
        bouton = Button(frame, text="Réinit.", width=5, height=2,
                   command=self.bouton_reinitialiser)
        bouton.pack(side="left")
        InfoBulle(bouton, "Remettre toutes les couleurs à zéro.")

        Label(self).pack()
        Button(self, text="Voir les possibilités", command=self.valider, width=100, height=2,
               bg="light green").pack()
        self.doublons = IntVar(self)
        case = Checkbutton(self, text="Autoriser les doublons.", variable=self.doublons)
        case.pack()
        InfoBulle(case, "La combinaison à trouver comporte-t-elle des couleurs qui se répètent ?")

        self.affiche = Label(self)
        self.affiche.pack()

        self.suppr = Label(self, text="Effectuez une recherche.")
        self.suppr.pack()

        self.after(100, fonction(self.mise_a_jour, False))

    def a_propos(self):
        """
        Bouton "à propos" pressé.
        """
        if askyesno("À propos du solveur de Mastermind",
                    """Ce solveur de mastermind a été créé par sev1527.
Souhaitez-vous ouvrir le dépôt GitHub pour en apprendre plus ?"""):
            webbrowser.open("https://github.com/sev1527/mastermind_solveur")

    def mise_a_jour(self, manuel=True):
        """
        Bouton de demande de mise à jour pressé.
        """
        try:
            requ = get("https://github.com/sev1527/mastermind_solveur/raw/main/donn%C3%A9es.json",
                    timeout=3)
            json = requ.json()
            print(json)
            n_l = "\n"
            if VERSION < json["update"]["last"]:
                if askyesno("Mise à jour",
                            f"""La version {json["update"]["last"]} est disponible"""\
                            f"""(vous avez {VERSION}).
Nouveautés :
{''.join(f'- {i}{n_l}' for i in json["update"]["new"])}

Souhaitez-vous ouvrir le dépôt GitHub pour l'installer ?"""):
                    webbrowser.open("https://github.com/sev1527/mastermind_solveur")
            elif manuel:
                showinfo("Mise à jour", "Aucune mise à jour disponible.")
        except ConnectionError:
            if manuel:
                showwarning("Échec", "Échec de la requête")
        except TimeoutError:
            if manuel:
                showwarning("Échec", "Échec de la requête")

    def bouton_reinitialiser(self):
        """
        Bouton de réinitialisation pressé.
        """
        if not askyesno("Réinitialiser", "Remettre l'affichage à zéro ?"):
            return
        for ligne in self.boutons:
            for bouton in ligne[0:-3]:
                bouton.config(bg=couleurs[0])
        for bouton, couleur in zip(self.boutons_couleur, couleurs):
            bouton.config(bg=couleur)

    def bouton_couleur_reception(self, ligne, colonne):
        """
        Bouton changer la couleur de la case sélectionnée pressé.
        """
        couleur = self.boutons_couleur[self.id_couleur]["bg"]
        self.boutons[ligne][colonne].config(bg=couleur)

    def bouton_couleur_modification(self):
        """
        Bouton pour modifier la couleur active pressé.
        """
        couleur = askcolor(color=couleurs[self.id_couleur])[1]
        liste_couleurs = (i["bg"] for i in self.boutons_couleur)
        if couleur in liste_couleurs:
            showwarning("Attention", "Une couleur ne peut pas être présente deux fois")
            return
        ancienne = self.boutons_couleur[self.id_couleur]["bg"]
        self.boutons_couleur[self.id_couleur].config(bg=couleur)
        for ligne in self.boutons:
            for bouton in ligne:
                if bouton["bg"] == ancienne:
                    bouton.config(bg=couleur)

    def bouton_couleur_selection(self, nombre):
        """
        Bouton pour sélectionner une nouvelle couleur pressé.
        """
        self.boutons_couleur[self.id_couleur].config(relief="raised")
        self.boutons_couleur[nombre].config(relief="sunken")
        self.id_couleur = nombre

    def bouton_valeur(self, ligne, colonne):
        """
        Bouton du nombre de cas bien/mal placé pressé.
        """
        nouveau = int(self.boutons[ligne][colonne]["text"])
        nouveau += 1
        nouveau %= 5
        self.boutons[ligne][colonne].config(text=nouveau)

    def bouton_activer(self, ligne, colonne):
        """
        Bouton pour activer/désactiver une ligne pressé.
        """
        self.boutons[ligne][colonne].state = not self.boutons[ligne][colonne].state
        if self.boutons[ligne][colonne].state:
            self._bouton_activer_animation(ligne, colonne, 1, 1,
                                           self.images["switch_bg"].width()//2+1)
        else:
            self._bouton_activer_animation(ligne, colonne, 1+self.images["switch_bg"].width()//2+1, -1,
                                           self.images["switch_bg"].width()//2+1)

    def _bouton_activer_animation(self, ligne, colonne, position, operation, restant):
        if not restant:
            return
        nombre = self.boutons[ligne][colonne].affiche
        self.boutons[ligne][colonne].moveto(nombre, position+operation, 1)
        self.after(5, fonction(self._bouton_activer_animation, ligne, colonne, position+operation,
                                                                operation, restant-1))

    def valider(self):
        """
        Bouton valider pressé.
        """
        self.suppr.destroy()
        convertir = {}
        for bouton, couleur in zip(self.boutons_couleur, range(len(self.boutons_couleur))):
            convertir[bouton["bg"]] = couleur
        entrees = []
        for bouton in self.boutons:
            if bouton[-1].state:
                entrees.append([])
                for bouton2 in bouton[0:-3]:
                    entrees[-1].append(convertir[bouton2["bg"]])
                for bouton2 in bouton[-3:-1]:
                    entrees[-1].append(int(bouton2["text"]))
        ret = calculer(entrees, self.doublons.get())
        nombre_total = len(combinaisons_double if self.doublons.get() else combinaisons)
        self.affiche.config(text=f"""{len(ret)}/{nombre_total} résultat(s)
Essayez :""")
        self.suppr = Frame(self)
        self.suppr.pack()
        for possibilite in ret[0:10]:
            frame = Frame(self.suppr)
            frame.pack()
            for couleur in possibilite[0:-1]:
                label = Label(frame, text="      ", bg=self.boutons_couleur[couleur]["bg"])
                label.pack(side="left")
                InfoBulle(label, f"couleur {couleur+1}")
            Label(frame, text=f"Score : {possibilite[-1]}").pack(side="left")


if __name__ == "__main__":
    Fen().mainloop()
