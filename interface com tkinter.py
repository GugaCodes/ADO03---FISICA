"""Interface interativa do ADO-3. Execute com python interface com matplotlib.py."""

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
from matplotlib.ticker import FuncFormatter, MaxNLocator

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
    def __init__(self, janela):
        self.janela = janela
        janela.title("ADO-3 | Colisões elásticas")
        janela.geometry("1160x760")
        janela.minsize(900, 640)
        janela.configure(fg_color=FUNDO)
        janela.grid_columnconfigure(1, weight=1)
        janela.grid_rowconfigure(1, weight=1)

        cabecalho = ctk.CTkFrame(janela, fg_color="transparent")
        cabecalho.grid(row=0, column=0, columnspan=2, sticky="ew", padx=22, pady=(16, 9))
        ctk.CTkLabel(cabecalho, text="Colisões elásticas",
                     font=ctk.CTkFont(size=27, weight="bold"),
                     text_color=TEXTO).pack(side="left")
        ctk.CTkLabel(cabecalho, text="ADO-3 · Opção A",
                     text_color=SECUNDARIO).pack(side="right")

        self.caso = 1
        self.reinicio_pendente = None
        self.criar_controles()
        area = ctk.CTkFrame(janela, fg_color=BRANCO, corner_radius=12)
        area.grid(row=1, column=1, sticky="nsew", padx=(0, 22), pady=(0, 18))
        area.grid_columnconfigure(0, weight=1)
        area.grid_rowconfigure(0, weight=1)
        self.fig = Figure(figsize=(7.6, 4.6), dpi=100, facecolor=BRANCO)
        self.canvas = FigureCanvasTkAgg(self.fig, master=area)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=8, pady=(8, 0))
        self.criar_pista()
        self.criar_resultados(area)
        self.reiniciar()
        self.animacao = FuncAnimation(
            self.fig, self.avancar, init_func=self.desenhar,
            interval=33, blit=self.canvas.supports_blit, cache_frame_data=False,
        )
        janela.protocol("WM_DELETE_WINDOW", self.fechar)

    def criar_controles(self):
        painel = ctk.CTkFrame(self.janela, width=240, fg_color=BRANCO, corner_radius=12)
        painel.grid(row=1, column=0, sticky="ns", padx=(22, 14), pady=(0, 18))
        painel.grid_columnconfigure(0, minsize=200, weight=1)
        ctk.CTkLabel(painel, text="Configuração",
                     font=ctk.CTkFont(size=17, weight="bold"),
                     text_color=TEXTO).grid(row=0, column=0, sticky="w", padx=16, pady=(14, 4))

        ctk.CTkLabel(painel, text="Caso de colisão", text_color=TEXTO).grid(
            row=1, column=0, sticky="w", padx=16,
        )
        self.menu = ctk.CTkOptionMenu(painel, values=list(CASOS), command=self.selecionar,
                                       fg_color=AZUL, button_color="#194987",
                                       button_hover_color="#163b70")
        self.menu.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 10))
        self.menu.set(next(iter(CASOS)))

        m1, m2, v1, v2 = obter_dados_caso(self.caso)
        parametros = [
            ("Massa do bloco 1", "kg", .5, 8, m1, .1),
            ("Massa do bloco 2", "kg", .5, 8, m2, .1),
            ("Velocidade do bloco 1", "m/s", -10, 10, v1, .1),
            ("Velocidade do bloco 2", "m/s", -10, 10, v2, .1),
            ("Duração do contato", "ms", 1, 150, 10, 1),
        ]
        self.sliders = []
        self.valores = []
        for i, (nome, unidade, minimo, maximo, inicial, passo) in enumerate(parametros):
            linha = 3 + i * 2
            legenda = ctk.CTkLabel(painel, text="", text_color=TEXTO)
            legenda.grid(row=linha, column=0, sticky="w", padx=16)
            slider = ctk.CTkSlider(
                painel, from_=minimo, to=maximo,
                number_of_steps=round((maximo - minimo) / passo),
                command=self.ajustar, progress_color=AZUL, button_color=AZUL,
            )
            slider.set(inicial)
            slider.grid(row=linha + 1, column=0, sticky="ew", padx=16, pady=(0, 10))
            self.sliders.append(slider)
            self.valores.append((legenda, nome, unidade, 0 if passo == 1 else 1))
        self.atualizar_controles()

        self.pausa = ctk.CTkButton(painel, text="Pausar", command=self.alternar_pausa,
                                    fg_color=AZUL, hover_color="#194987")
        self.pausa.grid(row=13, column=0, sticky="ew", padx=16, pady=(4, 6))
        ctk.CTkButton(painel, text="Reiniciar", command=self.reiniciar,
                      fg_color=GRADE, hover_color="#c6d8ef", text_color=TEXTO).grid(
            row=14, column=0, sticky="ew", padx=16, pady=(0, 14),
        )

    def atualizar_controles(self):
        for slider, (legenda, nome, unidade, casas) in zip(self.sliders, self.valores):
            valor = f"{slider.get() + 0.0:.{casas}f}".replace(".", ",")
            legenda.configure(text=f"{nome} · {valor} {unidade}")

    def ajustar(self, _valor):
        self.atualizar_controles()
        if self.reinicio_pendente is not None:
            self.janela.after_cancel(self.reinicio_pendente)
        self.reinicio_pendente = self.janela.after(50, self.aplicar_ajuste)

    def aplicar_ajuste(self):
        self.reinicio_pendente = None
        self.reiniciar()

    def criar_pista(self):
        self.pista = self.fig.add_axes([.10, .55, .86, .36], facecolor=BRANCO)
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

    def criar_resultados(self, area):
        self.graficos = []
        for x, titulo, unidade in [
            (.12, "Momento linear total", "kg·m/s"),
            (.60, "Energia cinética total", "J"),
        ]:
            eixo = self.fig.add_axes([x, .12, .36, .245], facecolor=BRANCO)
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

        painel = ctk.CTkFrame(area, fg_color=FUNDO, corner_radius=8)
        painel.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 12))
        painel.grid_columnconfigure((0, 1), weight=1)
        self.leitura = ctk.CTkLabel(painel, text="", text_color=SECUNDARIO)
        self.leitura.grid(row=0, column=0, columnspan=2, sticky="w", padx=12, pady=(4, 0))
        for coluna, titulo in enumerate(("Velocidades (m/s)", "Impulso e força média")):
            ctk.CTkLabel(painel, text=titulo, text_color=TEXTO,
                         font=ctk.CTkFont(size=13, weight="bold")).grid(
                row=1, column=coluna, sticky="w", padx=12,
            )
        self.velocidade_1 = ctk.CTkLabel(painel, text="", text_color=AZUL)
        self.velocidade_2 = ctk.CTkLabel(painel, text="", text_color=LARANJA)
        self.impulsos = ctk.CTkLabel(painel, text="", text_color=TEXTO)
        self.forca = ctk.CTkLabel(painel, text="", text_color=TEXTO)
        self.velocidade_1.grid(row=2, column=0, sticky="w", padx=12)
        self.velocidade_2.grid(row=3, column=0, sticky="w", padx=12, pady=(0, 4))
        self.impulsos.grid(row=2, column=1, sticky="w", padx=12)
        self.forca.grid(row=3, column=1, sticky="w", padx=12, pady=(0, 4))

    def selecionar(self, nome):
        self.caso = CASOS[nome]
        for slider, valor in zip(self.sliders, obter_dados_caso(self.caso)):
            slider.set(valor)
        self.atualizar_controles()
        self.reiniciar()

    def alternar_pausa(self):
        if self.t >= self.fim:
            self.reiniciar()
        elif self.pausado:
            self.pausado = False
            self.pausa.configure(text="Pausar")
            self.animacao.resume()
            self.canvas.draw_idle()
        else:
            self.pausado = True
            self.pausa.configure(text="Continuar")
            self.animacao.pause()
            self.canvas.draw_idle()

    def reiniciar(self):
        if self.reinicio_pendente is not None:
            self.janela.after_cancel(self.reinicio_pendente)
            self.reinicio_pendente = None
        m1, m2, v1, v2, contato = (slider.get() for slider in self.sliders)
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
        self.pausa.configure(text="Pausar")
        self.desenhar()
        # Exibe o quadro inicial antes de retomar a animação.
        if hasattr(self, "animacao"):
            self.animacao.resume()
        self.canvas.draw_idle()

    def atualizar_resultados(self, dados, m1, m2):
        v1, v2 = self.iniciais
        u1, u2 = self.finais
        if self.sem_choque:
            p = momento_linear(m1, m2, v1, v2)
            k = energia_cinetica(m1, m2, v1, v2)
            pares = ((p, None), (k, None))
            self.leitura.configure(text="Sem colisão. Os gráficos mostram os valores iniciais.")
            self.impulsos.configure(text="J₁ e J₂  ·  sem impulso de colisão")
            self.forca.configure(text="Força média de colisão  ·  —")
        else:
            pares = ((dados["p_antes"], dados["p_depois"]),
                     (dados["K_antes"], dados["K_depois"]))
            self.leitura.configure(
                text=                f"Momento e energia se conservam.   ΔK = {numero(dados['delta_K'])} J"
            )
            self.impulsos.configure(text=f"J₁ = {numero(dados['J1'])} N·s     "
                                   f"J₂ = {numero(dados['J2'])} N·s")
            self.forca.configure(text=f"Força média  ·  {numero(dados['F_med'])} N")
        for i, (texto, inicial, final) in enumerate(
            ((self.velocidade_1, v1, u1), (self.velocidade_2, v2, u2)), start=1
        ):
            texto.configure(text=f"Bloco {i}   {numero(inicial)} → {numero(final)}")

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
            self.pausa.configure(text="Repetir")
            self.canvas.draw_idle()
        return artistas


    def fechar(self):
        if self.reinicio_pendente is not None:
            self.janela.after_cancel(self.reinicio_pendente)
        if self.animacao.event_source is not None:
            self.animacao.event_source.stop()
        self.janela.destroy()


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    janela = ctk.CTk()
    simulador = Simulador(janela)
    janela.mainloop()

