from tkinter import Tk, Button, Label, Frame, Checkbutton, IntVar
from tkinter.colorchooser import askcolor
from tkinter.messagebox import showwarning
from copy import deepcopy

combinaisons = []
combinaisons_double = []
couleurs = ["#e40000", "#0067ff", "#909090", "#00df2d", "#ff21d4", "#ffffff", "#ff8a00", "#f4f700"]

def double(liste):
    for i in range(len(liste)):
        l = liste[0:i]+liste[i+1:len(liste)]
        if liste[i] in l:
            return True
    return False

for i1 in couleurs:
    for i2 in couleurs:
        for i3 in couleurs:
            for i4 in couleurs:
                comb = [i1, i2, i3, i4]
                combinaisons_double.append(comb)
                if not double(comb):
                    combinaisons.append(comb)


def noter(item, liste):
    n = 0
    for i in liste:
        for c in range(len(item)):
            if item[c] == i[c]:
                n += 5
            elif item[c] in i:
                n += 1
    return n

def calculer(liste, double):
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
            copie_entree = deepcopy(entree)
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
        n = noter(ret[r], ret)
        nret.append(ret[r]+[n])
    return trier(nret, -1, False)

def trier(liste, key, croissant=True):
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
    def a():
        f(*args, **kwargs)
    return a


class Fen(Tk):
    def __init__(self):
        super().__init__()
        self.title("Solveur de Mastermind")
        
        Label(self, text="Solveur de Mastermind", font="Arial 18").pack()
        self.boutons = []
        self.but_f = Frame(self)
        self.but_f.pack()
        for l in range(5):
            f = Frame(self.but_f)
            f.pack()
            self.boutons.append([])
            for b in range(4):
                but = Button(f, text="\n", command=fonction(self.bouton_couleur_reception, l, b), bg=couleurs[0], width=5)
                but.pack(side="left")
                self.boutons[-1].append(but)
            
            Label(f).pack(side="left")
            but = Button(f, text="0", command=fonction(self.bouton_valeur, l, len(self.boutons[-1])), bg="white", height=2, width=5)
            but.pack(side="left")
            self.boutons[-1].append(but)
            but = Button(f, text="0", command=fonction(self.bouton_valeur, l, len(self.boutons[-1])), bg="red", height=2, width=5)
            but.pack(side="left")
            self.boutons[-1].append(but)
            Label(f).pack(side="left")
            but = Button(f, text="o/N", command=fonction(self.bouton_activer, l, len(self.boutons[-1])), bg="red", height=2, width=5)
            but.pack(side="left")
            self.boutons[-1].append(but)
        
        Label(self).pack()
        self.boutons_couleur = []
        f = Frame(self)
        f.pack()
        for i in range(8):
            b = Button(f, text="\n", bg=couleurs[i], width=5, command=fonction(self.bouton_couleur_selection, i))
            b.pack(side="left")
            self.boutons_couleur.append(b)
        self.id_couleur = 0
        self.boutons_couleur[self.id_couleur].config(relief="sunken")
        b = Button(f, text="Modifier", width=10, height=2, command=self.bouton_couleur_modification)
#        b.pack(side="left")
        
        Label(self).pack()
        Button(self, text="Voir les possibilités", command=self.valider, width=100, height=2, bg="light green").pack()
        self.doublons = IntVar(self)
        Checkbutton(self, text="Autoriser les doublons.", variable=self.doublons).pack()
        
        self.affiche = Label(self)
        self.affiche.pack()
        
    def bouton_couleur_reception(self, l, nb):
        self.boutons[l][nb].config(bg=couleurs[self.id_couleur])
    
    def bouton_couleur_modification(self):
        showwarning("Attention", "Cette fonction ne marche pas encore !")
        c = askcolor(color=couleurs[self.id_couleur])[1]
        self.boutons_couleur[self.id_couleur].config(bg=c)
    
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
        entrees = []
        for b in self.boutons:
            if b[-1]["text"] == "O/n":
                entrees.append([])
                for b2 in b[0:-3]:
                    entrees[-1].append(b2["bg"])
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
                Label(f, text="      ", bg=c).pack(side="left")
            Label(f, text=f"Score : {p[-1]}").pack(side="left")


if __name__ == "__main__":
    Fen().mainloop()

