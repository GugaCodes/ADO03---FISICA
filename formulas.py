def colisao_elastica(m1,m2,v1,v2):
    u1 = ((m1-m2) * v1 + 2 * m2 * v2) / (m1 + m2)
    u2 = ((m2-m1) * v2 + 2 * m1 * v1) / (m1+m2)

    return u1, u2

def momento_linear(m1, m2, v1, v2):
    p = m1 * v1 + m2 * v2

    return p

def energia_cinetica(m1, m2, v1, v2):
    K = (m1 * v1 **2 )/ 2 + (m2 * v2** 2 ) / 2

    return K

def calcular_impulso(m1, m2, v1, v2, u1, u2):

    J1 = m1 * (u1 - v1)
    J2 = m2 * (u2 - v2)

    return J1, J2

def calcular_forca_media(J, delta_t):
    F_med = abs(J) / delta_t

    return  F_med



def obter_dados_caso(caso):

    if caso == 1:
        m1 = 1.0
        m2 = 1.0
        v1 = 4.0
        v2 = 0.0

    elif caso == 2:
        m1 = 1.0
        m2 = 4.0
        v1 = 5.0
        v2 = 0.0

    elif caso == 3:
        m1 = 4.0
        m2 = 1.0
        v1 = 5.0
        v2 = 0.0

    else:
        return None

    return m1, m2, v1, v2


def calcular_resultados(caso, delta_t_ms, m1=None, m2=None, v1=None, v2=None):
    """
    Calcula os resultados físicos de uma colisão elástica unidimensional.

    Pode utilizar um dos três casos predefinidos ou receber
    valores personalizados de massa e velocidade.

    Retorna um dicionário com velocidades finais, momento linear,
    energia cinética, impulsos e força média.
    """

    # Se nenhum valor personalizado foi informado, utiliza um dos três casos
    if m1 is None and m2 is None and v1 is None and v2 is None:

        dados = obter_dados_caso(caso)

        if dados is None:
            return None

        m1, m2, v1, v2 = dados

    # Verifica se todos os valores personalizados foram informados
    elif m1 is None or m2 is None or v1 is None or v2 is None:
        return {
            "mensagem": "Informe todos os valores de massa e velocidade."
        }

    # Verifica se as massas são positivas
    if m1 <= 0 or m2 <= 0:
        return {
            "mensagem": "As massas devem ser maiores que zero."
        }

    # Verifica se o tempo de colisão é válido
    if delta_t_ms <= 0:
        return {
            "mensagem": "O tempo de colisão deve ser maior que zero."
        }

    # Verifica se os blocos irão colidir
    if v1 <= v2:
        return {
            "mensagem": "Não ocorre colisão: v1 deve ser maior que v2."
        }

    # Calcula as velocidades finais
    u1, u2 = colisao_elastica(m1, m2, v1, v2)

    # Calcula o momento linear antes e depois da colisão
    p_antes = momento_linear(m1, m2, v1, v2)
    p_depois = momento_linear(m1, m2, u1, u2)

    # Calcula a energia cinética antes e depois da colisão
    K_antes = energia_cinetica(m1, m2, v1, v2)
    K_depois = energia_cinetica(m1, m2, u1, u2)

    # Calcula a variação da energia cinética
    delta_K = K_depois - K_antes

    # Calcula os impulsos dos dois blocos
    J1, J2 = calcular_impulso(m1, m2, v1, v2, u1, u2)

    # Converte o tempo de milissegundos para segundos
    delta_t = delta_t_ms / 1000

    # Calcula a força média
    F_med = calcular_forca_media(J1, delta_t)

    # Retorna todos os resultados em um dicionário
    return {
        "m1": m1,
        "m2": m2,
        "v1": v1,
        "v2": v2,
        "u1": u1,
        "u2": u2,
        "p_antes": p_antes,
        "p_depois": p_depois,
        "K_antes": K_antes,
        "K_depois": K_depois,
        "delta_K": delta_K,
        "J1": J1,
        "J2": J2,
        "F_med": F_med
    }

def verificar_conservacao(resultados):

    momento_conservado = abs(
        resultados["p_antes"] - resultados["p_depois"]
    ) < 0.000001

    energia_conservada = abs(
        resultados["K_antes"] - resultados["K_depois"]
    ) < 0.000001

    return momento_conservado, energia_conservada

def verificar_impulsos(resultados):

    impulsos_opostos = abs(
        resultados["J1"] + resultados["J2"]
    ) < 0.000001

    return impulsos_opostos

def verificar_resultados(resultados):

    momento, energia = verificar_conservacao(resultados)

    impulsos = verificar_impulsos(resultados)

    return {
        "momento_conservado": momento,
        "energia_conservada": energia,
        "impulsos_opostos": impulsos
    }


if __name__ == "__main__":

    # Teste dos três casos
    for caso in range(1, 4):
        resultados = calcular_resultados(caso, 10)

        print(f"\n===== CASO {caso} =====")
        print(resultados)

    # Teste sem colisão
    teste = calcular_resultados(1, 10, 1, 1, 2, 4)

    print("\n===== TESTE SEM COLISÃO =====")
    print(teste)

    print("\n===== TESTE COM VALORES PERSONALIZADOS =====")

    resultado = calcular_resultados(
        caso=1,
        delta_t_ms=10,
        m1=2,
        m2=3,
        v1=6,
        v2=0
    )

    print(resultado)

    resultado = calcular_resultados(1, 10)

    momento, energia = verificar_conservacao(resultado)

    print("Momento conservado:", momento)
    print("Energia conservada:", energia)

resultado = calcular_resultados(1, 10)

print("Impulsos opostos:", verificar_impulsos(resultado))

resultado = calcular_resultados(1, 10)

verificacoes = verificar_resultados(resultado)

print(verificacoes)