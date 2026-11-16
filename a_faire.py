"""Signale une fonction que vous n'avez pas encore écrite.

Chaque fonction à compléter se termine, dans le kit, par

    raise AFaire(2, "lister_projets")

Tant que cette ligne est là :
  - les tests qui ont besoin de la fonction sont comptés « À FAIRE »
    (et non « ÉCHEC ») ;
  - le site affiche une page qui indique l'étape et la fonction à écrire.

Remplacez la ligne par votre code. Ne modifiez pas ce fichier.
"""


class AFaire(NotImplementedError):
    def __init__(self, etape, fonction):
        self.etape = etape
        self.fonction = fonction
        if "." in fonction:                      # un fichier, comme schema.sql
            message = f"étape {etape} : {fonction} à compléter"
        else:
            message = f"étape {etape} : fonction {fonction}() à écrire"
        super().__init__(message)
