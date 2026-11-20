"""Interface interativa do ADO-3. Execute com python interface.py."""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
from matplotlib.ticker import FuncFormatter, MaxNLocator
from matplotlib.widgets import Button, RadioButtons, Slider

from formulas import calcular_resultados, energia_cinetica, momento_linear, obter_dados_caso


FUNDO = "#eef2f7"
BRANCO = "#ffffff"
TEXTO = "#152642"
SECUNDARIO = "#475c75"
AZUL = "#235bb0"
LARANJA = "#a63d1d"
VERDE = "#176a59"
GRADE = "#d8e1ed"

CASOS = {
    "Massas iguais": 1,
    "Bloco 1 mais leve": 2,
    "Bloco 1 mais pesado": 3,
}


def numero(valor):
    valor = round(valor, 2) + 0.0
    return f"{valor:.2f}".replace(".", ",")


def posicoes(t, tc, origens, iniciais, finais):
    antes = min(t, tc)
    depois = t - antes
    return tuple(x + v * antes + u * depois
                 for x, v, u in zip(origens, iniciais, finais))


class Simulador:
    def __init__(self):
        self.fig = plt.figure(figsize=(12.5, 7.6), facecolor=FUNDO)
        self.fig.canvas.manager.set_window_title("ADO-3 | Colisões elásticas")
        self.fig.text(.045, .938, "Colisões elásticas", fontsize=24,
                      weight="bold", color=TEXTO)
        self.fig.text(.955, .944, "ADO-3  /  OPÇÃO A", ha="right",
                      weight="bold", color=SECUNDARIO)

        self.caso = 1
        self.criar_controles()
        self.criar_pista()
        self.criar_resultados()
        self.reiniciar()
        self.animacao = FuncAnimation(
            self.fig, self.avancar, init_func=self.desenhar,
            interval=33, blit=self.fig.canvas.supports_blit, cache_frame_data=False,
        )

    def criar_controles(self):
        fundo = self.fig.add_axes([.043, .061, .243, .815], facecolor=BRANCO)
        fundo.set_xticks([])
        fundo.set_yticks([])
        for borda in fundo.spines.values():
            borda.set_visible(False)
        self.fig.text(.06, .833, "Configuração", fontsize=15, weight="bold", color=TEXTO)
        self.fig.text(.06, .791, "Casos predefinidos", weight="bold", color=TEXTO)
        eixo = self.fig.add_axes([.06, .628, .207, .152], facecolor=BRANCO)
        self.menu = RadioButtons(eixo, list(CASOS), activecolor=AZUL)
        self.menu.on_clicked(self.selecionar)

        m1, m2, v1, v2 = obter_dados_caso(self.caso)
        parametros = [
            ("Massa do bloco 1 (kg)", .5, 8, m1, .1),
            ("Massa do bloco 2 (kg)", .5, 8, m2, .1),
            ("Velocidade do bloco 1 (m/s)", -10, 10, v1, .1),
            ("Velocidade do bloco 2 (m/s)", -10, 10, v2, .1),
            ("Duração do contato (ms)", 1, 150, 10, 1),
        ]
        self.sliders = []
        for i, (nome, minimo, maximo, inicial, passo) in enumerate(parametros):
            y = .57 - i * .084
            self.fig.text(.06, y + .03, nome, color=TEXTO, fontsize=9)
            eixo = self.fig.add_axes([.062, y, .155, .019], facecolor=FUNDO)
            slider = Slider(eixo, "", minimo, maximo, valinit=inicial,
                            valstep=passo, color=AZUL,
                            valfmt="%d" if passo == 1 else "%.1f")
            slider.on_changed(self.reiniciar)
            self.sliders.append(slider)

        eixo_pausa = self.fig.add_axes([.06, .10, .098, .052])
        eixo_reinicio = self.fig.add_axes([.169, .10, .098, .052])
        self.pausa = Button(eixo_pausa, "Pausar", color=GRADE, hovercolor="#c6d8ef")
        self.reinicio = Button(eixo_reinicio, "Reiniciar", color=GRADE, hovercolor="#c6d8ef")
        self.pausa.on_clicked(self.alternar_pausa)
        self.reinicio.on_clicked(self.reiniciar)

    def criar_pista(self):
        self.pista = self.fig.add_axes([.33, .563, .625, .293], facecolor=BRANCO)
        self.pista.set_title("Movimento dos blocos", loc="left", color=TEXTO, weight="bold")
        self.pista.set_ylim(0, 2)
        self.pista.set_yticks([])
        self.pista.set_xlabel("Posição na pista (m)", color=SECUNDARIO)
        self.pista.tick_params(axis="x", colors=SECUNDARIO)
        for borda in self.pista.spines.values():
            borda.set_color(GRADE)
        self.pista.grid(axis="x", color=GRADE, alpha=.55)
        self.pista.axhline(.28, color=GRADE)
        self.status = self.pista.text(.023, .86, "", transform=self.pista.transAxes,
                                      color=SECUNDARIO)
        self.blocos = []
        self.rotulos = []
        for i, cor in enumerate((AZUL, LARANJA), start=1):
            bloco = Rectangle((0, .28), 1, 1, facecolor=cor, zorder=3)
            self.pista.add_patch(bloco)
            self.blocos.append(bloco)
            self.rotulos.append(self.pista.text(
                0, .28, f"B{i}", ha="center", va="center",
                color=BRANCO, weight="bold", zorder=4,
            ))

    def criar_resultados(self):
        self.fig.text(.33, .482, "Antes e depois do choque", fontsize=14,
                      weight="bold", color=TEXTO)
        self.graficos = []
        for x, titulo, unidade in [
            (.385, "Momento linear total", "kg·m/s"),
            (.710, "Energia cinética total", "J"),
        ]:
            eixo = self.fig.add_axes([x, .235, .245, .205], facecolor=BRANCO)
            eixo.set_title(titulo, loc="left", color=TEXTO, fontsize=11, weight="bold")
            eixo.set_ylabel(unidade, color=SECUNDARIO, fontsize=9)
            eixo.set_xlim(-.65, 1.65)
            eixo.set_xticks([0, 1], ["Antes", "Depois"])
            eixo.tick_params(colors=SECUNDARIO, labelsize=9, length=0, pad=5)
            eixo.yaxis.set_major_locator(MaxNLocator(nbins=4))
            eixo.yaxis.set_major_formatter(
                FuncFormatter(lambda valor, _: f"{valor:g}".replace(".", ","))
            )
            eixo.set_axisbelow(True)
            eixo.grid(axis="y", color=GRADE, linewidth=.8)
            eixo.axhline(0, color=SECUNDARIO, linewidth=.9)
            for lado, borda in eixo.spines.items():
                borda.set_visible(lado in ("left", "bottom"))
                borda.set_color(GRADE)
            barras = eixo.bar([0, 1], [0, 0], width=.43, color=[AZUL, VERDE])
            rotulos = [
                eixo.annotate("", (i, 0), xytext=(0, 5), textcoords="offset points",
                              ha="center", va="bottom", color=TEXTO,
                              fontsize=9, weight="bold")
                for i in range(2)
            ]
            self.graficos.append((eixo, barras, rotulos))

        self.leitura = self.fig.text(.33, .174, "", color=SECUNDARIO, fontsize=10)
        self.fig.text(.33, .126, "Velocidades (m/s)", weight="bold", color=TEXTO)
        self.fig.text(.655, .126, "Impulso e força média", weight="bold", color=TEXTO)
        self.velocidade_1 = self.fig.text(.33, .091, "", color=AZUL)
        self.velocidade_2 = self.fig.text(.33, .056, "", color=LARANJA)
        self.impulsos = self.fig.text(.655, .091, "", color=TEXTO)
        self.forca = self.fig.text(.655, .056, "", color=TEXTO)

    def selecionar(self, nome):
        self.caso = CASOS[nome]
        for slider, valor in zip(self.sliders, obter_dados_caso(self.caso)):
            slider.eventson = slider.drawon = False
            slider.set_val(valor)
            slider.eventson = slider.drawon = True
        self.reiniciar()

    def alternar_pausa(self, _evento):
        if self.t >= self.fim:
            self.reiniciar()
        elif self.pausado:
            self.pausado = False
            self.pausa.label.set_text("Pausar")
            self.animacao.resume()
            self.fig.canvas.draw_idle()
        else:
            self.pausado = True
            self.pausa.label.set_text("Continuar")
            self.animacao.pause()
            self.fig.canvas.draw_idle()

    def reiniciar(self, _evento=None):
        m1, m2, v1, v2, contato = (slider.val for slider in self.sliders)
        dados = calcular_resultados(self.caso, contato, m1=m1, m2=m2, v1=v1, v2=v2)
        self.iniciais = (v1, v2)
        self.sem_choque = "mensagem" in dados
        self.finais = self.iniciais if self.sem_choque else (dados["u1"], dados["u2"])

        larguras = (.7 + .14 * m1, .7 + .14 * m2)
        for bloco, largura in zip(self.blocos, larguras):
            bloco.set_width(largura)
            bloco.set_height(.40 + .31 * largura)
        self.origens = (0, 3 + sum(larguras) / 2)
        self.tc = float("inf") if self.sem_choque else 3 / (v1 - v2)
        self.fim = 2.5 if self.sem_choque else self.tc + 1.3
        self.passo = max(.033, self.fim / 210)
        self.t = 0.0
        self.pausado = False
        extremos = self.origens + self.centros(self.fim)
        if not self.sem_choque:
            extremos += self.centros(self.tc)
        margem = max(larguras) / 2 + .65
        self.pista.set_xlim(min(extremos) - margem, max(extremos) + margem)

        self.atualizar_resultados(dados, m1, m2)
        self.pausa.label.set_text("Pausar")
        self.desenhar()
        if hasattr(self, "animacao"):
            self.animacao.resume()
        self.fig.canvas.draw_idle()

    def atualizar_resultados(self, dados, m1, m2):
        v1, v2 = self.iniciais
        u1, u2 = self.finais
        if self.sem_choque:
            p = momento_linear(m1, m2, v1, v2)
            k = energia_cinetica(m1, m2, v1, v2)
            pares = ((p, None), (k, None))
            self.leitura.set_text("Sem colisão. Os gráficos mostram os valores iniciais.")
            self.impulsos.set_text("J₁ e J₂  ·  sem impulso de colisão")
            self.forca.set_text("Força média de colisão  ·  —")
        else:
            pares = ((dados["p_antes"], dados["p_depois"]),
                     (dados["K_antes"], dados["K_depois"]))
            self.leitura.set_text(
                f"Momento e energia se conservam.   ΔK = {numero(dados['delta_K'])} J"
            )
            self.impulsos.set_text(f"J₁ = {numero(dados['J1'])} N·s     "
                                   f"J₂ = {numero(dados['J2'])} N·s")
            self.forca.set_text(f"Força média  ·  {numero(dados['F_med'])} N")
        for i, (texto, inicial, final) in enumerate(
            ((self.velocidade_1, v1, u1), (self.velocidade_2, v2, u2)), start=1
        ):
            texto.set_text(f"Bloco {i}   {numero(inicial)} → {numero(final)}")

        for (eixo, barras, rotulos), par in zip(self.graficos, pares):
            medidas = [0 if valor is None else valor for valor in par]
            baixo, alto = min(0, *medidas), max(0, *medidas)
            escala = alto - baixo or 1
            eixo.set_ylim(baixo - .25 * escala if baixo < 0 else 0,
                          alto + .27 * escala)
            for i, (barra, rotulo, medida, valor) in enumerate(zip(barras, rotulos, medidas, par)):
                barra.set_height(medida)
                barra.set_visible(valor is not None)
                rotulo.xy = (i, medida)
                rotulo.set_position((0, -5 if medida < 0 else 5))
                rotulo.set_verticalalignment("top" if medida < 0 else "bottom")
                rotulo.set_text("—" if valor is None else numero(valor))

    def centros(self, t):
        return posicoes(t, self.tc, self.origens, self.iniciais, self.finais)

    def desenhar(self):
        for bloco, rotulo, centro in zip(self.blocos, self.rotulos, self.centros(self.t)):
            bloco.set_x(centro - bloco.get_width() / 2)
            rotulo.set_position((centro, .28 + bloco.get_height() / 2))
        if self.sem_choque:
            fase = "Sem colisão  ·  v₁ ≤ v₂"
        elif self.t < self.tc:
            fase = f"Antes do choque  ·  contato em {numero(self.tc)} s"
        elif self.t == self.tc:
            fase = "Choque"
        else:
            fase = "Após o choque"
        self.status.set_text(f"{numero(self.t)} s   |   {fase}")
        return (*self.blocos, *self.rotulos, self.status)

    def avancar(self, _quadro):
        if self.pausado or self.t >= self.fim:
            self.animacao.event_source.stop()
            return self.desenhar()

        proximo = min(self.t + self.passo, self.fim)
        # Reserva um quadro para o instante em que as bordas se tocam.
        self.t = self.tc if self.t < self.tc <= proximo else proximo
        artistas = self.desenhar()
        if self.t >= self.fim:
            self.animacao.pause()
            self.pausa.label.set_text("Repetir")
            self.fig.canvas.draw_idle()
        return artistas


if __name__ == "__main__":
    simulador = Simulador()
    plt.show()

