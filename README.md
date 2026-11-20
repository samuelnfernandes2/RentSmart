# RentSmart — Sistema de Orçamento de Locação

Projeto acadêmico em Python para automatizar o cálculo de orçamentos de locação da imobiliária fictícia R.M Imóveis.

## Requisitos
- Python 3.9 ou superior
- Não utiliza bibliotecas externas; usa `csv` e `decimal`, que fazem parte da biblioteca padrão do Python.

## Como executar
1. Extraia a pasta `RentSmart`.
2. Abra a pasta no VS Code.
3. Abra o terminal integrado.
4. Execute:
   - Windows: `python main.py`
   - Linux/macOS: `python3 main.py`
5. Responda às perguntas apresentadas no terminal.
6. O programa exibirá o orçamento e criará `projecao_12_meses.csv` na mesma pasta.

## Regras implementadas
- Apartamento de 1 quarto: R$ 700,00.
- Casa de 1 quarto: R$ 900,00.
- Estúdio: R$ 1.200,00.
- Apartamento de 2 quartos: adicional de R$ 200,00.
- Casa de 2 quartos: adicional de R$ 250,00.
- Casa/apartamento com uma vaga: adicional de R$ 300,00.
- Estúdio: pacote inicial de 2 vagas por R$ 250,00; cada vaga acima das duas custa R$ 60,00.
- Apartamento sem crianças: desconto de 5% sobre o subtotal após os adicionais.
- Taxa contratual: R$ 2.000,00, parcelável de 1 a 5 vezes.
- A projeção mostra 12 meses; a taxa aparece apenas nos meses em que há parcela.

## Organização do código
O projeto começa em um único arquivo (`main.py`) para facilitar a execução:
- `Imovel`: guarda as características do imóvel e calcula adicionais.
- `Orcamento`: calcula subtotal, desconto, aluguel final e parcelas da taxa.
- `Projecao`: exporta o planejamento de 12 meses para CSV.
- `main()`: coleta os dados e coordena a execução.

## Decisões de interpretação
O enunciado informa as regras de um e dois quartos para casas e apartamentos; por isso, o programa aceita somente essas duas opções. Para estúdios, não há seleção de quartos. O enunciado descreve um pacote inicial de duas vagas e vagas adicionais; por isso, o sistema exige pelo menos duas vagas para estúdios. Para casas e apartamentos, foi interpretada a opção de garagem como zero ou uma vaga, pois o enunciado prevê uma vaga com adicional de R$ 300,00.

A condição de desconto por ausência de crianças é aplicada exclusivamente a apartamentos, conforme o enunciado. A taxa contratual é separada do aluguel mensal.

## Teste sugerido
Escolha apartamento, 2 quartos, garagem sim, crianças não e 5 parcelas:
- Aluguel-base: R$ 700,00
- Adicional de quarto: R$ 200,00
- Garagem: R$ 300,00
- Subtotal: R$ 1.200,00
- Desconto de 5%: R$ 60,00
- Aluguel mensal: R$ 1.140,00
- Taxa contratual: R$ 2.000,00 em 5 parcelas de R$ 400,00

## Entregas acadêmicas
O PDF `documentacao_teorica.pdf` é um modelo inicial da parte teórica. Revise os dados de identificação e confirme que a documentação corresponde à versão do código que você efetivamente entregar. O vídeo pitch de até 4 minutos e o repositório GitHub devem ser publicados pelo estudante e seus links incluídos na submissão.
