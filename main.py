import streamlit as st
import math
import random
import re
from collections import Counter
import PyPDF2


st.set_page_config(page_title = 'Avaliação BackEnd', layout = 'centered')

st.title("Avaliações de Desenvolvimento BackEnd")

random.seed()
# Funções para cada tipo de loteria
def mega_sena():
    return random.sample(range(1, 61), 6)  # Mega Sena (6 números entre 1 e 60)

def quina():
    return random.sample(range(1, 81), 5)  # Quina (5 números entre 1 e 80)

def lotofacil():
    return random.sample(range(1, 26), 15)  # Lotofácil (15 números entre 1 e 25)

# Função para comparar os números gerados com os números informados pelo usuário
def comparar_numeros(numeros_sorteados, numeros_usuario):
    acertos = set(numeros_sorteados).intersection(set(numeros_usuario))
    return len(acertos), acertos



# Função para extrair texto de um arquivo PDF
def extrair_texto_pdf(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        texto = ""
        for pagina in pdf_reader.pages:
            texto += pagina.extract_text()
        return texto
    except Exception as e:
        st.error(f"Erro ao processar o PDF: {e}")
        return ""

# Função para analisar o texto
def analisar_texto(texto):
    palavras = re.findall(r'\b\w+\b', texto.lower())  # Usando regex para pegar palavras
    num_palavras = len(palavras)

    # Contar o número de frases (baseado em pontuação final como . ? !)
    frases = re.split(r'[.!?]', texto)
    num_frases = len([frase for frase in frases if frase.strip()])

    frequencia_palavras = Counter(palavras)

    palavra_mais_frequente, frequencia_mais_alta = frequencia_palavras.most_common(1)[0]

    caracteres = {
        'letras': len(re.findall(r'[a-zA-Z]', texto)),
        'numeros': len(re.findall(r'\d', texto)),
        'pontuacao': len(re.findall(r'[^\w\s]', texto)), 
        'espacos': texto.count(' ')
    }

    return {
        'num_palavras': num_palavras,
        'num_frases': num_frases,
        'frequencia_palavras': frequencia_palavras,
        'palavra_mais_frequente': palavra_mais_frequente,
        'frequencia_mais_alta': frequencia_mais_alta,
        'caracteres': caracteres
    }


tabs = st.tabs(["Calculadora trigonometrica", "Simulador de Loteria", "Analisador de Texto"])
with tabs[0]:
    st.header("Avaliação 1: Calculadora Trigonométrica em Python")
    st.header("Insira os valores do triângulo retângulo")
    tipo_entrada = st.radio("Escolha o tipo de entrada:", ["Dois lados", "Um lado e um ângulo"])
    
    if tipo_entrada == "Dois lados":
        lado_a = st.number_input("Insira o comprimento do primeiro lado (a):", min_value=0.0, format="%.2f")
        lado_b = st.number_input("Insira o comprimento do segundo lado (b):", min_value=0.0, format="%.2f")
        
        if st.button("Calcular"):
            if lado_a > 0 and lado_b > 0:
                # cálculo da hipotenusa
                hipotenusa = math.sqrt(lado_a**2 + lado_b**2)
                
                # Cálculo dos ângulos
                angulo_a = math.degrees(math.atan(lado_a / lado_b))
                angulo_b = 90 - angulo_a
                
                st.subheader("Resultados:")
                st.write(f"Hipotenusa (c): {hipotenusa:.2f}")
                st.write(f"Ângulo A: {angulo_a:.2f}°")
                st.write(f"Ângulo B: {angulo_b:.2f}°")
            else:
                st.error("Os lados devem ser maiores que zero.")
    elif tipo_entrada == "Um lado e um ângulo":
        # Entrada para um lado e um ângulo
        lado = st.number_input("Insira o comprimento do lado conhecido (a ou b):", min_value=0.0, format="%.2f")
        angulo = st.number_input("Insira o ângulo em graus (exceto 90°):", min_value=0.0, max_value=90.0, format="%.2f")
        
        if st.button("Calcular"):
            if lado > 0 and 0 < angulo < 90:
                angle_rad = math.radians(angulo)
                
                lado_adj = lado * math.tan(angle_rad)
                hipotenusa = lado / math.sin(angle_rad)
                
                angle_b = 90 - angulo
                
                st.subheader("Resultados:")
                st.write(f"Hipotenusa (c): {hipotenusa:.2f}")
                st.write(f"Lado oposto: {lado_adj:.2f}")
                st.write(f"Ângulo B: {angle_b:.2f}°")
            else:
                st.error("O lado deve ser maior que zero e o ângulo deve estar entre 0° e 90° (não inclusivo).")
with tabs[1]:
    st.header("Avaliação 2:  Simulador de Loteria em Python")
    tipo_loteria = st.radio("Escolha o tipo de Loteria:", ["Mega Sena", "Quina", "Lotofácil"])

    # Definindo as funções de sorteio com base na escolha
    if tipo_loteria == "Mega Sena":
        sorteio_func = mega_sena
        num_sorteados = 6
        intervalo = (1, 60)
    elif tipo_loteria == "Quina":
        sorteio_func = quina
        num_sorteados = 5
        intervalo = (1, 80)
    elif tipo_loteria == "Lotofácil":
        sorteio_func = lotofacil
        num_sorteados = 15
        intervalo = (1, 25)

    numeros_sorteados = sorteio_func()

    st.header("Digite seus números da sorte")
    numeros_usuario = st.multiselect(
        "Escolha os seus números",
        list(range(intervalo[0], intervalo[1] + 1)),
        max_selections=num_sorteados
    )

    if len(numeros_usuario) == num_sorteados:
        acertos, acertos_set = comparar_numeros(numeros_sorteados, numeros_usuario)

        st.subheader("Resultados:")
        st.write(f"Números sorteados: {numeros_sorteados}")
        st.write(f"Seus números: {numeros_usuario}")
        st.write(f"Você acertou {acertos} número(s)!")

        if acertos == num_sorteados:
            st.success("Parabéns! Você acertou todos os números!")
        elif acertos > 0:
            st.success(f"Você acertou {acertos} número(s)!")
        else:
            st.warning("Não acertou nenhum número. Tente novamente!")
    
    else:
        st.error(f"Por favor, escolha exatamente {num_sorteados} números entre {intervalo[0]} e {intervalo[1]}.")
    
with tabs[2]:
    st.header("Avaliação 3: Analisador de Texto em Python")
    tipo_entrada = st.radio("Escolha o tipo de entrada:", ["Texto Digitado", "Texto de Arquivo"])

    texto = ""
    if tipo_entrada == "Texto Digitado":
        texto = st.text_area("Digite o texto para análise:", height=300)
    elif tipo_entrada == "Texto de Arquivo":
        pdf_file = st.file_uploader("Faça upload de um arquivo PDF", type="pdf")
        if pdf_file:
            texto = extrair_texto_pdf(pdf_file)

    if texto:
        resultados = analisar_texto(texto)

        st.subheader("Estatísticas do Texto:")

        st.write(f"**Número de palavras:** {resultados['num_palavras']}")
        st.write(f"**Número de frases:** {resultados['num_frases']}")

        st.write(f"**Palavra mais frequente:** '{resultados['palavra_mais_frequente']}' com {resultados['frequencia_mais_alta']} ocorrências.")

        st.write("**Contagem de tipos de caracteres:**")
        st.write(f"Letras: {resultados['caracteres']['letras']}")
        st.write(f"Números: {resultados['caracteres']['numeros']}")
        st.write(f"Pontuação: {resultados['caracteres']['pontuacao']}")
        st.write(f"Espaços: {resultados['caracteres']['espacos']}")