#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
[Ce bloc est la documentation du module]
Un Tetris avec Pygame.
Ce code est basee sur le code de Sébastien CHAZALLET,
auteur du livre 'Python 3, les fondamentaux du language'
"""

__author__ = 'votre nom'
__copyright__ = 'Copyright 2022'
__credits__ = ['Sébastien CHAZALLET', 'Vincent NGUYEN', 'votre nom']
__license__ = 'GPL'
__version__ = '1.0'
__maintainer__ = 'votre nom'
__email__ = 'votre email'

# Probleme de l'ordre des imports
from pygame.locals import *
import random
import time
import pygame
import sys

from constantes import *

# Classe Tetris
class Jeu:
  """
	La classe du jeu Tetris avec ces méthodes pour faire fonctionner le jeux

	Args:
			clock (Clock): Gère le temps
			surface (): Gère la taille du plateau par rapport a la taille de la fenêtre
			fonts (Font): Les fonts de base
	"""

    def __init__(self) -> None:
        """Déclaration des variables utiles au jeux Tetris
		"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode(TAILLE_FENETRE)
        self.fonts = {
            'defaut': pygame.font.Font('freesansbold.ttf', 18),
            'titre': pygame.font.Font('freesansbold.ttf', 100),
        }
        pygame.display.set_caption('Application ' + APP_NAME)

    def start(self) -> None:
        """Lance le jeux
		"""
        self._afficher_texte(APP_NAME, CENTRE_FENETRE, font='titre')
        self._afficher_texte('Appuyer sur une touche...', POS)
        self._attente()

    def stop(self) -> None:
        """Stop et ferme le jeux ( fenêtre )
		"""
        self._afficher_texte('Perdu', CENTRE_FENETRE, font='titre')
        self._attente()
        self._quitter()

    def _afficher_texte(self,
                        text: str,
                        position,
                        couleur: int = 9,
                        font: str = 'defaut') -> None:
        """Permet d'afficher le texte en paramètre en fonction des paramètres

		Args:
			text (str): Texte a afficher
			position (_type_): Position du texte
			couleur (int, optional): Couleur du texte . Defaults to 9.
			font (str, optional): Font du texte. Defaults to 'defaut'.
		"""
        font = self.fonts.get(font, self.fonts['defaut'])
        couleur = COULEURS.get(couleur, COULEURS[9])
        rendu = font.render(text, True, couleur)
        rect = rendu.get_rect()
        rect.center = position
        self.surface.blit(rendu, rect)

    def _get_event(self) -> None:
        """Récupère l'entrer de l'utilisateur

		Returns:
			None: Entrée clavier de l'utilisateur
		"""
        for event in pygame.event.get():
            if event.type == QUIT:
                self._quitter()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self._quitter()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    continue
                return event.key

    def _quitter(self) -> None:
        """Ferme la fenêtre du jeux
		"""
        print("Quitter")
        pygame.quit()
        sys.exit()

    def _rendre(self) -> None:
        """Met a jour l'affichage de la fenêtre
		"""
        pygame.display.update()
        self.clock.tick()

    def _attente(self) -> None:
        """Met en pause le jeux
		"""
        print("Attente")
        while self._get_event() == None:
            self._rendre()

    def _get_piece(self) -> list[str] | None:
        """Récupère une pièce parmis la liste des pièces dans les constantes

		Returns:
			list[str] | None: Une pièce
		"""
        return PIECES.get(random.choice(PIECES_KEYS))

    def _get_current_piece_color(self) -> str:
        """Retourne la couleur de la pièce actuelle

		Returns:
			str: Couleur de la pièce
		"""
        for l in self.current[0]:
            for c in l:
                if c != 0:
                    return c
        return 0

    def _calculer_donnees_piece_courante(self) -> None:
        """Calcule les données de la pièce actuelle
		"""
        m = self.current[self.position[2]]
        coords = []
        for i, l in enumerate(m):
            for j, k in enumerate(l):
                if k != 0:
                    coords.append([i + self.position[0], j + self.position[1]])
        self.coordonnees = coords

    def _est_valide(self, x: int = 0, y: int = 0, r: int = 0) -> bool:
        """Retourne si la position de la pièce est valide ou non sur plateur

		Args:
			x (int, optional): Position en x. Defaults to 0.
			y (int, optional): Position en y. Defaults to 0.
			r (int, optional): Valeur de la rotation de la pièce. Defaults to 0.

		Returns:
			bool: _description_
		"""
        max_x, max_y = DIM_PLATEAU
        if r == 0:
            coordonnees = self.coordonnees
        else:
            m = self.current[(self.position[2] + r) % len(self.current)]
            coords = []
            for i, l in enumerate(m):
                for colonne, k in enumerate(l):
                    if k != 0:
                        coords.append(
                            [i + self.position[0], colonne + self.position[1]])
            coordonnees = coords
#			print('Rotation testée: %s' % coordonnees)
        for cx, cy in coordonnees:
            if not 0 <= x + cx < max_x:
                #				print('Non valide en X: cx=%s, x=%s' % (cx, x))
                return False
            elif cy < 0:
                continue
            elif y + cy >= max_y:
                #				print('Non valide en Y: cy=%s, y=%s' % (cy, y))
                return False
            else:
                if self.plateau[cy + y][cx + x] != 0:
                    #					print('Position occupée sur le plateau')
                    return False
#		print('Position testée valide: x=%s, y=%s' % (x, y))
        return True

    def _poser_piece(self) -> None:
        """Pose la pièce sur le plateau ( position définitive )
		"""
        print("La pièce est posée")
        if self.position[1] <= 0:
            self.perdu = True
        # Ajout de la pièce parmi le plateau
        couleur = self._get_current_piece_color()
        for cx, cy in self.coordonnees:
            self.plateau[cy][cx] = couleur
        completees = []
        # calculer les lignes complétées
        for i, line in enumerate(self.plateau[::-1]):
            for case in line:
                if case == 0:
                    break
            else:
                print(self.plateau)
                print(">>> %s" % (DIM_PLATEAU[1] - 1 - i))
                completees.append(DIM_PLATEAU[1] - 1 - i)
        lignes = len(completees)
        for i in completees:
            self.plateau.pop(i)
        for i in range(lignes):
            self.plateau.insert(0, [0] * DIM_PLATEAU[0])
        # calculer le score et autre
        self.lignes += lignes
        self.score += lignes * self.niveau
        self.niveau = int(self.lignes / 10) + 1
        if lignes >= 4:
            self.tetris += 1
            self.score += self.niveau * self.tetris
        # Travail avec la pièce courante terminé
        self.current = None

    def _first(self) -> None:
        """
		Initialise les valeurs du jeux et de la première pièces
		"""
        self.plateau = [[0] * DIM_PLATEAU[0] for i in range(DIM_PLATEAU[1])]
        self.score, self.pieces, self.lignes, self.tetris, self.niveau = SCORE_START, 0, 0, 0, NIVEAU
        self.current, self.next, self.perdu = None, self._get_piece(), False

    def _next(self) -> None:
        """Passe a la pièce suivante
		"""
        print("Piece suivante")
        self.current, self.next = self.next, self._get_piece()
        self.pieces += 1
        self.position = [int(DIM_PLATEAU[0] / 2) - 2, -4, 0]
        self._calculer_donnees_piece_courante()
        self.dernier_mouvement = self.derniere_chute = time.time()

    def _gerer_evenements(self) -> None:
        """Gère les évènements en fonction de l'entrée du joueur
		"""
        event = self._get_event()
        if event == KEY_PAUSE:
            print("Pause")
            self.surface.fill(COULEURS.get(0))
            self._afficher_texte('Pause', CENTRE_FENETRE, font='titre')
            self._afficher_texte('Appuyer sur une touche...', POS)
            self._attente()
        elif event == KEY_LEFT:
            print("Mouvement vers la gauche")
            if self._est_valide(x=-1):
                self.position[0] -= 1
        elif event == KEY_RIGHT:
            print("Mouvement vers la droite")
            if self._est_valide(x=1):
                self.position[0] += 1
        elif event == KEY_DOWN:
            print("Mouvement vers le bas")
            if self._est_valide(y=1):
                self.position[1] += 1
        elif event == KEY_UP:
            print("Mouvement de rotation")
            if self._est_valide(r=1):
                self.position[2] = (self.position[2] + 1) % len(self.current)
        elif event == KEY_INSTANT_DOWN:
            print("Mouvement de chute %s / %s" %
                  (self.position, self.coordonnees))
            if self.position[1] <= 0:
                self.position[1] = 1
                self._calculer_donnees_piece_courante()
            a = 0
            while self._est_valide(y=a):
                a += 1
            self.position[1] += a - 1
        self._calculer_donnees_piece_courante()

    def _gerer_gravite(self) -> None:
        """Gère la gravité et permet a une pièce de changer sa position vers le bas si elle peut encore déscendre
		"""
        if time.time() - self.derniere_chute > GRAVITE:
            self.derniere_chute = time.time()
            if not self._est_valide():
                print("On est dans une position invalide")
                self.position[1] -= 1
                self._calculer_donnees_piece_courante()
                self._poser_piece()
            elif self._est_valide() and not self._est_valide(y=1):
                self._calculer_donnees_piece_courante()
                self._poser_piece()
            else:
                print("On déplace vers le bas")
                self.position[1] += 1
                self._calculer_donnees_piece_courante()

    def _dessiner_plateau(self) -> None:
        """Dessine le plateur de jeu
		"""
        self.surface.fill(COULEURS.get(0))
        pygame.draw.rect(self.surface, COULEURS[8],
                         START_PLABORD + TAILLE_PLABORD, BORDURE_PLATEAU)
        for i, ligne in enumerate(self.plateau):
            for j, case in enumerate(ligne):
                couleur = COULEURS[case]
                position = j, i
                coordonnees = tuple([
                    START_PLATEAU[k] + position[k] * TAILLE_BLOC[k]
                    for k in range(2)
                ])
                pygame.draw.rect(self.surface, couleur,
                                 coordonnees + TAILLE_BLOC)
        if self.current is not None:
            for position in self.coordonnees:
                couleur = COULEURS.get(self._get_current_piece_color())
                coordonnees = tuple([
                    START_PLATEAU[k] + position[k] * TAILLE_BLOC[k]
                    for k in range(2)
                ])
                pygame.draw.rect(self.surface, couleur,
                                 coordonnees + TAILLE_BLOC)
        self.score, self.pieces, self.lignes, self.tetris, self.niveau  #TODO
        self._afficher_texte('Score: >%s' % self.score, POSITION_SCORE)
        self._afficher_texte('Pièces: %s' % self.pieces, POSITION_PIECES)
        self._afficher_texte('Lignes: %s' % self.lignes, POSITION_LIGNES)
        self._afficher_texte(APP_NAME + ': %s' % self.tetris, POSITION_TETRIS)
        self._afficher_texte('Niveau: %s' % self.niveau, POSITION_NIVEAU)

        self._rendre()

    def play(self) -> None:
        """Gère le jeu tant que la partie n'est pas perdu (les évènements, la gravité)
		"""
        print("Jouer")
        self.surface.fill(COULEURS.get(0))
        self._first()
        while not self.perdu:
            if self.current is None:
                self._next()
            self._gerer_evenements()
            self._gerer_gravite()
            self._dessiner_plateau()

if __name__ == '__main__':
    j = Jeu()
    print("Jeu prêt")
    j.start()
    print("Partie démarée")
    j.play()
    print("Partie terminée")
    j.stop()
    print("Arrêt du programme")
