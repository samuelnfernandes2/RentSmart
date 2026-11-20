import csv
from decimal import Decimal, ROUND_HALF_UP


def dinheiro(valor):
    """Formata um valor Decimal no padrão brasileiro."""
    valor = Decimal(valor).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


class Imovel:
    """Representa o imóvel escolhido pelo cliente."""

    PRECOS_BASE = {
        "apartamento": Decimal("700.00"),
        "casa": Decimal("900.00"),
        "estudio": Decimal("1200.00"),
    }

    def __init__(self, tipo, quartos=0, vagas=0):
        if tipo not in self.PRECOS_BASE:
            raise ValueError("Tipo de imóvel inválido.")

        if tipo in ("apartamento", "casa") and quartos not in (1, 2):
            raise ValueError("Casas e apartamentos devem ter 1 ou 2 quartos.")

        if tipo == "estudio" and quartos != 0:
            raise ValueError("Estúdios não possuem seleção de quartos neste sistema.")

        if tipo in ("apartamento", "casa") and vagas not in (0, 1):
            raise ValueError("Casas e apartamentos permitem 0 ou 1 vaga.")

        if tipo == "estudio" and vagas < 2:
            raise ValueError("Estúdios começam com um pacote mínimo de 2 vagas.")

        self.tipo = tipo
        self.quartos = quartos
        self.vagas = vagas
        self.aluguel_base = self.PRECOS_BASE[tipo]

    def calcular_adicional_quartos(self):
        if self.tipo == "apartamento" and self.quartos == 2:
            return Decimal("200.00")
        if self.tipo == "casa" and self.quartos == 2:
            return Decimal("250.00")
        return Decimal("0.00")

    def calcular_adicional_garagem(self):
        if self.tipo in ("apartamento", "casa"):
            return Decimal("300.00") if self.vagas == 1 else Decimal("0.00")

        # Estúdio: pacote inicial de 2 vagas por R$ 250;
        # cada vaga acima das duas custa mais R$ 60.
        return Decimal("250.00") + Decimal(self.vagas - 2) * Decimal("60.00")

    def calcular_adicionais(self):
        return self.calcular_adicional_quartos() + self.calcular_adicional_garagem()


class Orcamento:
    """Calcula o aluguel, o desconto e a taxa contratual."""

    TAXA_CONTRATUAL = Decimal("2000.00")

    def __init__(self, imovel, possui_criancas, parcelas):
        if not 1 <= parcelas <= 5:
            raise ValueError("A taxa contratual deve ser parcelada de 1 a 5 vezes.")

        self.imovel = imovel
        self.possui_criancas = possui_criancas
        self.parcelas = parcelas

    def calcular_subtotal(self):
        return self.imovel.aluguel_base + self.imovel.calcular_adicionais()

    def calcular_desconto(self):
        if self.imovel.tipo == "apartamento" and not self.possui_criancas:
            return (self.calcular_subtotal() * Decimal("0.05")).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
        return Decimal("0.00")

    def calcular_aluguel_final(self):
        return self.calcular_subtotal() - self.calcular_desconto()

    def calcular_valores_parcelas(self):
        """Distribui os centavos para que a soma seja exatamente R$ 2.000."""
        centavos = int(self.TAXA_CONTRATUAL * 100)
        base, resto = divmod(centavos, self.parcelas)
        return [
            (Decimal(base + (1 if i < resto else 0)) / 100).quantize(Decimal("0.01"))
            for i in range(self.parcelas)
        ]

    def gerar_resumo(self):
        print("\n========== ORÇAMENTO RENTSMART ==========")
        print(f"Imóvel: {self.imovel.tipo.capitalize()}")
        if self.imovel.tipo != "estudio":
            print(f"Quartos: {self.imovel.quartos}")
        print(f"Vagas: {self.imovel.vagas}")
        print(f"Aluguel-base: {dinheiro(self.imovel.aluguel_base)}")
        print(f"Adicional de quartos: {dinheiro(self.imovel.calcular_adicional_quartos())}")
        print(f"Adicional de garagem: {dinheiro(self.imovel.calcular_adicional_garagem())}")
        print(f"Subtotal antes do desconto: {dinheiro(self.calcular_subtotal())}")
        print(f"Desconto: {dinheiro(self.calcular_desconto())}")
        print(f"ALUGUEL MENSAL: {dinheiro(self.calcular_aluguel_final())}")
        print(f"Taxa contratual: {dinheiro(self.TAXA_CONTRATUAL)}")
        print(f"Parcelamento: {self.parcelas} vez(es)")
        for numero, valor in enumerate(self.calcular_valores_parcelas(), start=1):
            print(f"  Parcela {numero}: {dinheiro(valor)}")
        print("=========================================")


class Projecao:
    """Gera a previsão de pagamentos dos primeiros 12 meses."""

    def __init__(self, orcamento):
        self.orcamento = orcamento

    def exportar_csv(self, nome_arquivo="projecao_12_meses.csv"):
        aluguel = self.orcamento.calcular_aluguel_final()
        parcelas = self.orcamento.calcular_valores_parcelas()

        with open(nome_arquivo, "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow(["Mes", "Aluguel", "Parcela_taxa_contratual", "Total_previsto"])

            for mes in range(1, 13):
                taxa_mes = parcelas[mes - 1] if mes <= len(parcelas) else Decimal("0.00")
                total = aluguel + taxa_mes
                escritor.writerow([
                    mes,
                    f"{aluguel:.2f}",
                    f"{taxa_mes:.2f}",
                    f"{total:.2f}",
                ])

        print(f"\\nArquivo CSV gerado com sucesso: {nome_arquivo}")


def pedir_numero(mensagem, minimo, maximo):
    while True:
        try:
            numero = int(input(mensagem))
            if minimo <= numero <= maximo:
                return numero
            print(f"Digite um número entre {minimo} e {maximo}.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


def pedir_sim_nao(mensagem):
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        print("Resposta inválida. Digite S para sim ou N para não.")


def main():
    print("Bem-vindo ao RentSmart — Orçamento de Locação\\n")
    print("1 - Apartamento")
    print("2 - Casa")
    print("3 - Estúdio")
    opcao = pedir_numero("Escolha o tipo de imóvel: ", 1, 3)
    tipos = {1: "apartamento", 2: "casa", 3: "estudio"}
    tipo = tipos[opcao]

    if tipo == "estudio":
        quartos = 0
        vagas = pedir_numero("Quantidade de vagas no estúdio (mínimo 2): ", 2, 100)
    else:
        quartos = pedir_numero("Quantidade de quartos (1 ou 2): ", 1, 2)
        possui_garagem = pedir_sim_nao("Deseja uma vaga de garagem? (S/N): ")
        vagas = 1 if possui_garagem else 0

    if tipo == "apartamento":
        possui_criancas = pedir_sim_nao("Possui crianças? (S/N): ")
    else:
        possui_criancas = True  # A condição de desconto só se aplica a apartamentos.

    parcelas = pedir_numero("Em quantas vezes deseja pagar a taxa (1 a 5)? ", 1, 5)

    imovel = Imovel(tipo, quartos, vagas)
    orcamento = Orcamento(imovel, possui_criancas, parcelas)
    orcamento.gerar_resumo()

    projecao = Projecao(orcamento)
    projecao.exportar_csv()


if __name__ == "__main__":
    main()
