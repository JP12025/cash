# Cash

![some coins](https://4.bp.blogspot.com/-H754wB9V3kA/UnAmo0rfwUI/AAAAAAAACbI/TWQineE6nvw/s400/eurocoins.png)

# Le problème à résoudre

Supposons que vous travaillez dans un commerce et qu'un enfant vous achète un chewing-gum à 0,36€.
Il vous donne une pièce de 1€ et il faut donc lui rendre 64 centimes. Sachant que vous avez des pièces de
`50`, `20`, `10`, `5`, `2` et `1` centimes, vous avez plusieurs solutions pour rendre la monnaie.

Par exemple, `2x20 + 2x10 + 1x2 + 2x1` qui utilise 7 pièces ou `3x20 + 1x2 + 2x1` qui utilise 6 pièces ou `3x20 + 2x2` qui utilise 5 pièces ou `1x50 + 1x10 + 2x2` qui utilise 4 pièces.

Dans un fichier nommé `cash.py`, vous devez écrire un programme qui demande à l'utilisateur le montant à rendre (en centimes sur 1€). Une fois que l'utilisateur a répondu, le programme affiche le nombre **minimum** de pièces nécessaires sur la sortie standard.

```bash
$ python cash.py
Amount: 64
4
```

> [!TIP]
> Pour transformer un `str`en `int`, il suffit d'utiliser la fonction `int()`

Si l'utilisateur ne rentre pas un `int` entre 0 et 100, il faut redemander sans afficher de message d'erreur, comme dans l'exemple ci-dessous.

```bash
$ python cash.py
Amount: 103
Amount: -2
Amount: 26
3
```

> [!TIP]
> Pour savoir combien il y a `25` dans `64`, il suffit de faire `64 // 25` (et il restera `64 % 25`)

# Les tests

N'oubliez pas qu'il est important de tester son programme.
En effet, lorsque vous décidez de tester un programme cela vous amène à vous poser des questions
sur ce que fait votre programme et les cas particuliers.

Que se passe-t-il :
* Si vous tapez `-1` ?
* Si vous tapez `0` ?
* Si vous tapez `1` ?
* Si vous tapez `4` ?
* Si vous tapez `5` ?
* Si vous tapez `24` ?
* Si vous tapez `99` ?
* Si vous tapez `127` ?

# Le rendu via git
A tout moment, vous pouvez soumettre votre travail sur github visa un `push`.

```bash
git add cash.py
git commit -m "My answer"
git push
```

Des tests automatiques seront lancés dont vous pourrez voir les résultats sur github.
