#ADO-3 | Simulador de Colisões Elásticas
Projeto da disciplina de Física: Práticas Extensivas, do curso de Ciência da Computação. O simulador representa uma colisão elástica unidimensional entre dois blocos e permite observar como o momento linear e a energia cinética totais se conservam durante o choque.
Objetivo
Simular o choque entre dois blocos em uma dimensão e investigar como a massa e a velocidade de cada bloco afetam o movimento após a colisão. A animação mostra quando os blocos se tocam e em que direção seguem. Os gráficos comparam o momento linear e a energia cinética totais antes e depois do choque.
Modelo físico e fórmulas
O simulador considera dois blocos em uma dimensão, sem força externa resultante na direção horizontal. A direita é o sentido positivo.
Símbolo	Significado	Unidade
m1, m2	Massas dos blocos	kg
v1, v2	Velocidades antes do choque	m/s
u1, u2	Velocidades depois do choque	m/s
dt_ms	Duração do contato	ms


Velocidades após a colisão
u1 = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
u2 = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)
Momento linear e energia cinética
p_antes  = m1 * v1 + m2 * v2
p_depois = m1 * u1 + m2 * u2

K_antes  = (m1 * v1^2 + m2 * v2^2) / 2
K_depois = (m1 * u1^2 + m2 * u2^2) / 2
delta_K  = K_depois - K_antes
O momento linear total é medido em kg·m/s, e a energia cinética total, em joules (J). Na colisão elástica, o momento total permanece igual e a variação da energia cinética total é zero. A energia pode ser transferida de um bloco para o outro.
Impulso e força média
J1 = m1 * (u1 - v1)
J2 = m2 * (u2 - v2)
dt = dt_ms / 1000
F_media = |J1| / dt
Os impulsos J1 e J2, medidos em N·s, têm o mesmo módulo e sentidos opostos. O painel mostra o módulo da força média em newtons (N) e usa a duração do contato em segundos.
Instante da colisão e movimento
O bloco 1 começa à esquerda do bloco 2, com 3 m entre as bordas. Se v1 > v2, a diferença de velocidades determina quando eles se tocam.
d0 = 3 m
tc = d0 / (v1 - v2)

Antes do choque:  x(t) = x0 + v * t
Depois do choque: x(t) = x(tc) + u * (t - tc)
As equações de posição valem para cada bloco, usando sua posição inicial x0 e suas velocidades v e u. Quando v1 <= v2, os blocos mantêm as velocidades iniciais. O ajuste da duração do contato altera a força média, e a animação troca as velocidades no instante tc.
Casos predefinidos
Nos três casos, o bloco 2 começa em repouso. Velocidades negativas indicam movimento para a esquerda.
Caso	Massa do bloco 1 (kg)	Massa do bloco 2 (kg)	Velocidade inicial do bloco 1 (m/s)	Velocidades finais (m/s)
Massas iguais	1	1	4	Bloco 1: 0 · Bloco 2: 4
Bloco 1 mais leve	1	4	5	Bloco 1: −3 · Bloco 2: 2
Bloco 1 mais pesado	4	1	5	Bloco 1: 3 · Bloco 2: 8


No caso de massas iguais, o bloco 1 para e o bloco 2 passa a se mover a 4 m/s. O momento total é 4 kg·m/s e a energia cinética total é 8 J, antes e depois do choque. Com um contato de 10 ms, os impulsos são −4 N·s e +4 N·s e a força média tem módulo de 400 N.
Como usar o simulador
- Selecione um dos três casos para carregar os valores iniciais.
- Ajuste as massas, as velocidades ou a duração do contato pelos controles deslizantes.
- Use os botões para pausar, continuar ou reiniciar a animação.
- Compare o momento linear e a energia cinética totais nos gráficos de antes e depois do choque. O painel também mostra as velocidades, os impulsos e a força média.
- Se o bloco 1 estiver com velocidade menor ou igual à do bloco 2, o simulador indica que não ocorre colisão.
