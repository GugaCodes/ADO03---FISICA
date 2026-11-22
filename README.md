# Simulador de Colisões Elásticas em Python

Projeto desenvolvido para a **ADO-3 de Física: Práticas Extensivas**, do curso de Ciência da Computação. O grupo escolheu a **opção A**, que estuda colisões elásticas entre dois blocos que se movimentam em linha reta.

## Objetivo

Investigar como as massas e as velocidades iniciais influenciam o movimento dos blocos após uma colisão. O simulador permite observar quando um bloco para, muda de sentido ou continua avançando. Os gráficos mostram como o momento linear e a energia cinética totais se conservam, mesmo quando cada bloco muda de velocidade.

## Como funciona

A interface foi desenvolvida em Python com **Matplotlib**. O usuário escolhe um dos três casos predefinidos ou ajusta as massas, as velocidades e a duração do contato pelos controles deslizantes.

A animação mostra o movimento antes e depois do choque. Os botões permitem pausar, continuar e reiniciar a simulação. Dois gráficos comparam o momento linear e a energia cinética totais antes e depois da colisão. O painel também apresenta as velocidades dos blocos, os impulsos e a força média durante o contato.

## Casos simulados

Nos três casos, o bloco 2 começa em repouso. Uma velocidade positiva indica movimento para a direita, e uma velocidade negativa indica movimento para a esquerda.

| Caso | Massa do bloco 1 | Massa do bloco 2 | Velocidade inicial do bloco 1 | Resultado após o choque |
| --- | ---: | ---: | ---: | --- |
| Massas iguais | 1 kg | 1 kg | 4 m/s | O bloco 1 para e o bloco 2 segue a 4 m/s. |
| Bloco 1 mais leve | 1 kg | 4 kg | 5 m/s | O bloco 1 volta a −3 m/s e o bloco 2 segue a 2 m/s. |
| Bloco 1 mais pesado | 4 kg | 1 kg | 5 m/s | Os dois avançam. O bloco 1 segue a 3 m/s e o bloco 2 a 8 m/s. |

## Fórmulas utilizadas

Nas equações, `m1` e `m2` são as massas em quilogramas. As velocidades iniciais são `v1` e `v2`, e as velocidades após o choque são `u1` e `u2`, todas em metros por segundo.

### 1. Velocidades após a colisão

Em uma colisão elástica unidimensional, as velocidades finais são calculadas por:

```text
u1 = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
u2 = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)
```

### 2. Momento linear

O momento linear total é a soma dos momentos dos dois blocos. Como o sistema é isolado na direção horizontal, o total se conserva. A unidade é `kg·m/s`.

```text
p_antes  = m1 * v1 + m2 * v2
p_depois = m1 * u1 + m2 * u2
```

### 3. Energia cinética

A energia cinética é medida em joules (`J`). Na colisão elástica, um bloco pode transferir energia ao outro, e a variação da energia cinética total é zero.

```text
K_antes  = (m1 * v1² + m2 * v2²) / 2
K_depois = (m1 * u1² + m2 * u2²) / 2

ΔK = K_depois - K_antes
```

### 4. Impulso e força média

O impulso é a variação do momento linear de cada bloco. Os impulsos têm o mesmo módulo e sentidos opostos. Para calcular o módulo da força média, o programa converte a duração do contato de milissegundos para segundos.

```text
J1 = m1 * (u1 - v1)
J2 = m2 * (u2 - v2)

tempo_em_segundos = tempo_em_milissegundos / 1000
forca_media = abs(J1) / tempo_em_segundos
```

O impulso é medido em `N·s` e a força média em `N`. Para o mesmo impulso, multiplicar a duração do contato por dez reduz a força média a um décimo.

### 5. Instante da colisão e posição dos blocos

O bloco 1 começa à esquerda do bloco 2, com uma distância de 3 m entre suas bordas. Quando `v1 > v2`, essa distância diminui até o contato. O tempo até a colisão é calculado por:

```text
tc = 3 / (v1 - v2)
```

Cada bloco se move com velocidade constante antes e depois do choque. Para cada um, `x0` é a posição inicial e `x(tc)` é a posição no instante do contato.

```text
Antes do choque:   x(t) = x0 + v * t
Depois do choque:  x(t) = x(tc) + u * (t - tc)
```

Se `v1 <= v2`, o bloco 1 não alcança o bloco 2 e a interface informa que não ocorre colisão.

## Como interpretar os gráficos

No caso de **massas iguais**, o bloco 1 começa a 4 m/s e transfere seu movimento ao bloco 2. No gráfico de momento linear, as duas colunas marcam **4 kg·m/s**. No gráfico de energia cinética, ambas marcam **8 J**. As colunas de cada gráfico têm a mesma altura porque representam o total dos dois blocos.

## Estrutura do projeto

| Arquivo | Função |
| --- | --- |
| `formulas.py` | Define os casos e calcula velocidades, momento linear, energia cinética, impulsos e força média. |
| `interface.py` | Exibe os controles, anima os blocos e atualiza os gráficos e o painel de resultados. |


