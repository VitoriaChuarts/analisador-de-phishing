MARCAS = [
    "paypal", "google", "facebook", "instagram", "amazon", "microsoft",
    "apple", "netflix", "nubank", "itau", "bradesco", "santander",
    "mercadolivre", "whatsapp",
]


def distancia_edicao(a: str, b: str) -> int:
    anterior = list(range(len(b) + 1))

    for i, letra_a in enumerate(a, start=1):
        atual = [i]
        for j, letra_b in enumerate(b, start=1):
            custo = 0 if letra_a == letra_b else 1
            atual.append(min(
                anterior[j] + 1,
                atual[j - 1] + 1,
                anterior[j - 1] + custo,
            ))
        anterior = atual

    return anterior[-1]


def marca_parecida(dominio: str):
    for marca in MARCAS:
        distancia = distancia_edicao(dominio, marca)
        limite = 1 if len(marca) <= 5 else 2
        if 0 < distancia <= limite:
            return marca
    return None