# Comparação Experimental de Algoritmos de Ordenação

Este projeto implementa e analisa o desempenho dos algoritmos de ordenação **Insertion Sort**, **Merge Sort** e **Quick Sort** (iterativo com pivô aleatório) para vetores de tamanhos de $1.000$, $10.000$ e $100.000$ elementos.

## Como Executar no macOS

Siga os passos abaixo para configurar o ambiente virtual e executar os benchmarks no macOS.

### 1. Clonar ou Acessar a Pasta do Projeto
Abra o terminal na pasta raiz deste projeto:
```bash
cd /caminho/para/lista10
```

### 2. Criar o Ambiente Virtual (`venv`)
Crie um ambiente virtual chamado `venv` com Python 3:
```bash
python3 -m venv venv
```

### 3. Ativar o Ambiente Virtual
Ative o ambiente virtual criado:
```bash
source venv/bin/activate
```

### 4. Instalar as Dependências
Instale a biblioteca `matplotlib` necessária para gerar os gráficos:
```bash
pip install --upgrade pip
pip install matplotlib
```

### 5. Executar o Script
Rode o script principal para executar os benchmarks, exportar os resultados em CSV e gerar os gráficos:
```bash
python main.py
```

Os resultados serão gerados em:
- `resultados_benchmark.csv`: Dados detalhados das execuções e tempo médio.
- `graficos/`: Pasta com imagens PNG exibindo curvas de tempo e comparações de desempenho.