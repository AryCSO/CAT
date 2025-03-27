import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import speech_recognition as sr
from datetime import datetime

def selecionar_arquivo():
    caminho = filedialog.askopenfilename(
        title="Selecione o arquivo de áudio",
        filetypes=[("Arquivos de Áudio", "*.wav *.mp3")]
    )
    entrada_caminho.config(state='normal')
    entrada_caminho.delete(0, tk.END)
    entrada_caminho.insert(0, caminho)
    entrada_caminho.config(state='disabled')

def converter_audio_para_texto():
    caminho_arquivo_audio = entrada_caminho.get()
    idioma = idioma_var.get()

    if not caminho_arquivo_audio:
        messagebox.showwarning("Aviso", "Por favor, selecione um arquivo de áudio.")
        return

    if not os.path.exists(caminho_arquivo_audio):
        messagebox.showerror("Erro", "Arquivo não encontrado.")
        return

    try:
        r = sr.Recognizer()
        with sr.AudioFile(caminho_arquivo_audio) as source:
            audio = r.record(source)

        texto = r.recognize_google(audio, language=idioma)
        resultado_texto.config(state='normal')
        resultado_texto.delete(1.0, tk.END)
        resultado_texto.insert(tk.END, texto)
        resultado_texto.config(state='disabled')
        salvar_texto_em_arquivo(texto)
    except sr.UnknownValueError:
        messagebox.showerror("Erro", "Não foi possível entender a fala do áudio.")
    except sr.RequestError:
        messagebox.showerror("Erro", "Não foi possível solicitar resultados do servidor.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

def salvar_texto_em_arquivo(texto, pasta="Transcricoes"):
    if not os.path.exists(pasta):
        os.makedirs(pasta)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = os.path.join(pasta, f"transcricao_{timestamp}.txt")
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(texto)
    messagebox.showinfo("Sucesso", f"Texto salvo com sucesso em {nome_arquivo}")

# Criação da janela
janela = tk.Tk()
janela.title("CAT - Conversor de Áudio para Texto")

# Define as dimensões da janela
largura_janela = 600
altura_janela = 400

# Obtém as dimensões da tela principal do usuário (monitor principal)
largura_tela = 1920
altura_tela = 1080

# Posição fixa no monitor principal (tentando manualmente)
pos_x = 660
pos_y = 340

# Impede o redimensionamento da janela
janela.resizable(False, False)

# Widgets
tk.Label(janela, text="Arquivo de Áudio:").pack(pady=5)
entrada_caminho = tk.Entry(janela, width=50, state='disabled')
entrada_caminho.pack(pady=5)
tk.Button(janela, text="Selecionar Arquivo", command=selecionar_arquivo).pack(pady=5)

tk.Label(janela, text="Idioma:").pack(pady=5)
idioma_var = tk.StringVar(value="pt-BR")
opcoes_idioma = ["pt-BR", "en-US"]
tk.OptionMenu(janela, idioma_var, *opcoes_idioma).pack(pady=5)

tk.Button(janela, text="Converter para Texto", command=converter_audio_para_texto).pack(pady=10)

tk.Label(janela, text="Texto Convertido:").pack(pady=5)
resultado_texto = scrolledtext.ScrolledText(janela, width=70, height=10, state='disabled')
resultado_texto.pack(pady=5)

janela.mainloop()
