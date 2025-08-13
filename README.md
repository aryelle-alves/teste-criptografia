# Ferramenta de Criptografia de Texto

🔒 Uma ferramenta simples para criptografar e descriptografar textos usando criptografia simétrica Fernet.

## Funcionalidades

- ✨ Gerar chaves de criptografia seguras
- 🔐 Criptografar textos com proteção por senha
- 🔓 Descriptografar textos usando a chave correta
- 📁 Armazenamento automático em JSON dos textos criptografados
- 📋 Copiar chaves para a área de transferência automaticamente
- ⏳ Registro de data/hora para todas as operações

## ⚙️ Pré-requisitos
- Python 3.6 ou superior
- Bibliotecas: `cryptography`, `pyperclip` (opcional para Linux/Mac)

## Como Funciona

1. **Gerar Chave**: Cria uma chave de criptografia segura (de 128 bits)
2. **Criptografar Texto**:
   - Digite seu texto (separe palavras com `;`)
   - A ferramenta criptografa e armazena com um ID único
3. **Descriptografar Texto**:
   - Forneça a chave correta e o ID do texto
   - Receba seu texto original como uma lista numerada

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/aryelle-alves/teste-criptografia