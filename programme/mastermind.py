# -*- coding: utf-8 -*-
"""
Une fenêtre graphique pour résoudre les combinaisons de Mastermind.
Créé par sev1527.
Dépot GitHub : https://github.com/sev1527/mastermind_solveur
"""
from tkinter import Tk, Button, Label, Frame, Checkbutton, IntVar, Toplevel
from tkinter.colorchooser import askcolor
from tkinter.messagebox import showwarning, askyesno, showinfo
import webbrowser
from requests import get
from copy import deepcopy

VERSION = "1.2.2"

combinaisons = []
combinaisons_double = []
couleurs = ["#e40000", "#0067ff", "#909090", "#00df2d", "#ff21d4", "#ffffff", "#ff8a00", "#f4f700"]
items = list(range(8))

def double(liste):
    """
    Y a-t-il un double dans la liste ?
    """
    for i in range(len(liste)):
        l = liste[0:i]+liste[i+1:len(liste)]
        if liste[i] in l:
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
    n = 0
    for i in liste:
        for c in range(len(item)):
            if item[c] == i[c]:
                n += 5
            elif item[c] in i:
                n += 1
    return n

def calculer(liste, double):
    """
    Calculer toutes les possibilités possibles avec les contraintes indiquée.
    """
    if double:
        liste_utilise = combinaisons_double
    else:
        liste_utilise = combinaisons
    ret = []
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
            ret.append(combinaison)

    nret = []
    for r in range(len(ret)):
        n = _noter(ret[r], ret)
        nret.append(ret[r]+[n])
    return trier(nret, -1, False)

def trier(liste, key, croissant=True):
    """
    Trie les items de la liste.
    """
    n = []
    for i in liste:
        f = True
        for c, p in zip(n, range(len(n))):
            if i[key]<c[key]:
                n.insert(p, i)
                f = False
                break
        if f:
            n.append(i)
    if croissant:
        return n
    return list(reversed(n))

def fonction(f, *args, **kwargs):
    """
    Transforme une fonction en lambda.
    """
    def a():
        f(*args, **kwargs)
    return a


class infoBulle(Toplevel):
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
        l = Label(self, text=texte, bg="ghost white", justify='left')
        l.update_idletasks()
        l.pack()
        l.update_idletasks()
        self.tipwidth = l.winfo_width()
        self.tipheight = l.winfo_height()
        self.master.bind('<Enter>', self.delai)
        self.master.bind('<Button-1>', self.efface)
        self.master.bind('<Leave>', self.efface)
    def delai(self, event):
        self.action = self.master.after(self.tps, self.affiche)
    def affiche(self):
        self.update_idletasks()
        posX = self.master.winfo_rootx() + self.master.winfo_width()
        posY = self.master.winfo_rooty() + self.master.winfo_height()
        if posX + self.tipwidth > self.winfo_screenwidth():
            posX = posX - self.winfo_width() - self.tipwidth
        if posY + self.tipheight > self.winfo_screenheight():
            posY = posY - self.winfo_height() - self.tipheight
        #~ print posX,print posY
        self.geometry('+%d+%d'%(posX,posY))
        self.deiconify()
    def efface(self,event):
        self.withdraw()
        self.master.after_cancel(self.action)

class Fen(Tk):
    def __init__(self):
        super().__init__()
        self.title("Solveur de Mastermind")

        f = Frame(self)
        f.pack()
        Label(f, text=f"Solveur de Mastermind {VERSION}  ", font="Arial 18").pack(side="left")
        u = Button(f, text="🗘", command=self.mise_a_jour)
        u.pack(side="left")
        infoBulle(u, "Rechercher les mises à jour")
        i = Button(f, text="ⓘ", command=self.a_propos)
        i.pack(side="left")
        infoBulle(i, "À propos")
        self.boutons = []
        self.but_f = Frame(self)
        self.but_f.pack()
        for l in range(5):
            f = Frame(self.but_f)
            f.pack()
            self.boutons.append([])
            for b in range(4):
                but = Button(f, text="\n", command=fonction(self.bouton_couleur_reception, l, b),
                             bg=couleurs[0], width=5)
                but.pack(side="left")
                self.boutons[-1].append(but)

            Label(f).pack(side="left")
            but = Button(f, text="0", bg="white", height=2, width=5,
                         command=fonction(self.bouton_valeur, l, len(self.boutons[-1]))                         )
            but.pack(side="left")
            self.boutons[-1].append(but)
            but = Button(f, text="0", bg="red", height=2, width=5,
                         command=fonction(self.bouton_valeur, l, len(self.boutons[-1])))
            but.pack(side="left")
            self.boutons[-1].append(but)
            Label(f).pack(side="left")
            but = Button(f, text="o/N", bg="red", height=2, width=5,
                         command=fonction(self.bouton_activer, l, len(self.boutons[-1])))
            but.pack(side="left")
            self.boutons[-1].append(but)

        Label(self).pack()
        self.boutons_couleur = []
        f = Frame(self)
        f.pack()
        for i in range(8):
            b = Button(f, text="\n", bg=couleurs[i], width=5,
                       command=fonction(self.bouton_couleur_selection, i))
            b.pack(side="left")
            self.boutons_couleur.append(b)
        self.id_couleur = 0
        self.boutons_couleur[self.id_couleur].config(relief="sunken")
        b = Button(f, text="Modifier", width=10, height=2,
                   command=self.bouton_couleur_modification)
        b.pack(side="left")
        infoBulle(b, "Modifier la couleur active")
        b = Button(f, text="Réinit.", width=5, height=2,
                   command=self.bouton_reinitialiser)
        b.pack(side="left")
        infoBulle(b, "Remettre toutes les couleurs à zéro.")

        Label(self).pack()
        Button(self, text="Voir les possibilités", command=self.valider, width=100, height=2,
               bg="light green").pack()
        self.doublons = IntVar(self)
        c = Checkbutton(self, text="Autoriser les doublons.", variable=self.doublons)
        c.pack()
        infoBulle(c, "La combinaison à trouver comporte-t-elle des couleurs qui se répètent ?")
        
        self.affiche = Label(self)
        self.affiche.pack()
        
        self.after(1000, fonction(self.mise_a_jour, False))

    def a_propos(self):
        if askyesno("À propos du solveur de Mastermind",
                    """Ce solveur de mastermind a été créé par sev1527.
Souhaitez-vous ouvrir le dépôt GitHub pour en apprendre plus ?"""):
            webbrowser.open("https://github.com/sev1527/mastermind_solveur")

    def mise_a_jour(self, manuel=True):
        try:
            r = get("https://github.com/sev1527/mastermind_solveur/raw/main/donn%C3%A9es.json")
            json = r.json()
            print(json)
            n = "\n"
            if VERSION < json["update"]["last"]:
                if askyesno("Mise à jour",
                            f"""La version {json["update"]["last"]} est disponible (vous avez {VERSION}).
Nouveautés :
{''.join(f'- {i}{n}' for i in json["update"]["new"])}

Souhaitez-vous ouvrir le dépôt GitHub pour l'installer ?"""):
                    webbrowser.open("https://github.com/sev1527/mastermind_solveur")
            elif manuel:
                showinfo("Mise à jour", "Aucune mise à jour disponible.")
        except ConnectionError:
            if manuel:
                showwarning("Échec", "Échec de la requête")

    def bouton_reinitialiser(self):
        if not askyesno("Réinitialiser", "Remettre l'affichage à zéro ?"):
            return
        for ligne in self.boutons:
            for bouton in ligne[0:-3]:
                bouton.config(bg=couleurs[0])
        for bouton, c in zip(self.boutons_couleur, couleurs):
            bouton.config(bg=c)
        
    def bouton_couleur_reception(self, l, nb):
        c = self.boutons_couleur[self.id_couleur]["bg"]
        self.boutons[l][nb].config(bg=c)
    
    def bouton_couleur_modification(self):
        c = askcolor(color=couleurs[self.id_couleur])[1]
        tbg = (i["bg"] for i in self.boutons_couleur)
        if c in tbg:
            showwarning("Attention", "Une couleur ne peut pas être présente deux fois")
            return
        ancienne = self.boutons_couleur[self.id_couleur]["bg"]
        self.boutons_couleur[self.id_couleur].config(bg=c)
        for l in self.boutons:
            for b in l:
                if b["bg"] == ancienne:
                    b.config(bg=c)

    def bouton_couleur_selection(self, nb):
        self.boutons_couleur[self.id_couleur].config(relief="raised")
        self.boutons_couleur[nb].config(relief="sunken")
        self.id_couleur = nb
    
    def bouton_valeur(self, l, nb):
        n = int(self.boutons[l][nb]["text"])
        n += 1
        n %= 5
        self.boutons[l][nb].config(text=n)

    def bouton_activer(self, l, nb):
        a = self.boutons[l][nb]["text"]
        if a == "O/n":
            self.boutons[l][nb].config(text="o/N", bg="red")
        else:
            self.boutons[l][nb].config(text="O/n", bg="#00E300")

    def valider(self):
        try:
            self.suppr.destroy()
        except AttributeError:
            pass
        convertir = {}
        for b, c in zip(self.boutons_couleur, range(len(self.boutons_couleur))):
            convertir[b["bg"]] = c
        entrees = []
        for b in self.boutons:
            if b[-1]["text"] == "O/n":
                entrees.append([])
                for b2 in b[0:-3]:
                    entrees[-1].append(convertir[b2["bg"]])
                for b2 in b[-3:-1]:
                    entrees[-1].append(int(b2["text"]))
        ret = calculer(entrees, self.doublons.get())
        n = combinaisons_double if self.doublons.get() else combinaisons
        self.affiche.config(text=f"""{len(ret)}/{len(n)} résultat(s)
Essayez :""")
        self.suppr = Frame(self)
        self.suppr.pack()
        for p in ret[0:10]:
            f = Frame(self.suppr)
            f.pack()
            for c in p[0:-1]:
                l = Label(f, text="      ", bg=self.boutons_couleur[c]["bg"])
                l.pack(side="left")
                infoBulle(l, f"couleur {c+1}")
            Label(f, text=f"Score : {p[-1]}").pack(side="left")


if __name__ == "__main__":
    Fen().mainloop()

