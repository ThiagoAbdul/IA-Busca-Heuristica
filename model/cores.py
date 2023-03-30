VERMELHO = (200, 10, 10)
VERDE = (10, 200, 10)
AZUL = (10, 10, 200)
MARROM = (160, 120, 40)
BRANCO = (255, 255, 255)
LARANJA = (255, 200, 0)
ROXO = (200, 10, 200)
TURQUESA = (10, 200, 200)
CINZA = (127, 127, 127)


def clarear(cor):
    return [tom + 150 if (tom + 150) < 256 else 255 for tom in cor]


def escurecer(cor):
    return [tom - 200 if (tom - 200) >= 0 else 0 for tom in cor]

