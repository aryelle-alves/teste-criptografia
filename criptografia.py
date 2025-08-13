from cryptography.fernet import Fernet, InvalidToken
import platform
import subprocess
import json
import os
from datetime import datetime
from time import sleep

class SistemaCriptografia:
    def __init__(self):
        self.arquivo_dados = "dados_criptografados.json"
        self.dados = self.carregar_dados()

    def carregar_dados(self):
        """Carrega todos os dados do arquivo JSON"""
        if os.path.exists(self.arquivo_dados):
            try:
                with open(self.arquivo_dados, 'r') as f:
                    return json.load(f)
            except:
                return {"textos": {}}
        return {"textos": {}}

    def salvar_dados(self):
        """Salva todos os dados no arquivo JSON"""
        with open(self.arquivo_dados, 'w') as f:
            json.dump(self.dados, f, indent=4)

    def copiar_para_area_transferencia(self, texto):
        """Copia texto para a área de transferência"""
        try:
            if platform.system() == "Windows":
                subprocess.run("clip", input=texto.encode("utf-16"), check=True, shell=True)
            else:  # Linux
                subprocess.run("xclip -selection clipboard", input=texto.encode(), check=True, shell=True)
            return True
        except:
            return False

    def gerar_chave(self):
        """Gera uma chave Fernet e copia para clipboard"""
        chave = Fernet.generate_key().decode()
        if self.copiar_para_area_transferencia(chave):
            print("\n🔑 Chave copiada para a área de transferência! (Cole com Ctrl+V)")
            print("⚠️ ANOTE esta chave. Ela NÃO será armazenada no programa.")
        else:
            print("\n⚠️ Falha ao copiar. Chave abaixo (ANOTE-A):")
            print(f"\n{chave}\n")
        sleep(2)
        return chave

    def criptografar(self, chave, texto, identificador=None):
        """Criptografa e armazena o texto com um ID único"""
        try:
            # Verifica se o texto contém ; para separação
            if ";" not in texto:
                print("\n⚠️ AVISO: Separe as palavras com ';' (ex: palavra1;palavra2;palavra3)")
                print("Deseja continuar mesmo assim? (s/n)")
                if input("→ ").strip().lower() != 's':
                    return False
            
            fernet = Fernet(chave.encode())
            texto_cripto = fernet.encrypt(texto.encode()).decode()
            
            id_texto = identificador if identificador else f"texto_{len(self.dados['textos']) + 1}"
            self.dados['textos'][id_texto] = {
                "texto_criptografado": texto_cripto,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.salvar_dados()
            
            print(f"\n✅ Texto '{id_texto}' criptografado e salvo!")
            print(f"⚠️ ANOTE SUA CHAVE: {chave}")  # Aviso reforçado
            return True
        except Exception as e:
            print(f"\n❌ Erro: {e}")
            return False

    def descriptografar(self, chave, id_texto):
        """Descriptografa um texto específico"""
        if id_texto not in self.dados['textos']:
            print("\n❌ ID não encontrado!")
            return None
        
        try:
            fernet = Fernet(chave.encode())
            texto_cripto = self.dados['textos'][id_texto]["texto_criptografado"]
            texto_decifrado = fernet.decrypt(texto_cripto.encode()).decode()
            
            # Separa as palavras por ; e remove espaços extras
            palavras = [palavra.strip() for palavra in texto_decifrado.split(';') if palavra.strip()]
            
            print("\n🔓 Texto descriptografado:")
            for i, palavra in enumerate(palavras, 1):
                print(f"{i}. {palavra}")
            return palavras
        except InvalidToken:
            print("\n❌ CHAVE INVÁLIDA! Use a chave correta para este texto.")
            return None

def menu_principal():
    sistema = SistemaCriptografia()
    
    while True:
        print("\n" + "="*56)
        print(" CRIPTOGRAFIA ".center(56, '='))
        print("="*56)
        print("1. Gerar e copiar chave")
        print("2. Criptografar")
        print("3. Descriptografar")
        print("4. Listar salvos")
        print("5. Sair")
        print("="*56)
        print("ℹ️  INSTRUÇÕES:")
        print("- Separe as palavras com ';' (EX.: palavra1;palavra2)")
        print("- Chaves NÃO são armazenadas - ANOTE!")
        print("="*56)
        
        opcao = input("→ Escolha: ").strip()
        
        if opcao == "1":
            sistema.gerar_chave()
        elif opcao == "2":
            chave = input("\nDigite a chave: ").strip()
            texto = input("Texto a criptografar (separe com ;): ").strip()
            id_texto = input("ID (opcional): ").strip()
            sistema.criptografar(chave, texto, id_texto if id_texto else None)
        elif opcao == "3":
            if not sistema.dados['textos']:
                print("\nℹ️ Nenhum texto salvo.")
            else:
                print("\n📋 Textos disponíveis:")
                for id_texto in sistema.dados['textos']:
                    print(f"- {id_texto}")
                id_escolhido = input("\nDigite o ID do texto: ").strip()
                chave = input("Digite a chave: ").strip()
                sistema.descriptografar(chave, id_escolhido)
        elif opcao == "4":
            print("\n📝 Textos armazenados:")
            for id_texto, dados in sistema.dados['textos'].items():
                print(f"\nID: {id_texto}")
                print(f"Data: {dados['timestamp']}")
        elif opcao == "5":
            print("\n🔒 Programa encerrado. Dados mantidos em 'dados_criptografados.json'.")
            break
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    menu_principal()