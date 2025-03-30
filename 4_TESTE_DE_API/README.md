# Joao Henrique Silva de Miranda

# Como Rodar e Testar

1. **Inicie a aplicação:**

   - Execute o arquivo `app.py`:
     
     ```bash
     python app.py
     ```

   - Isso iniciará o servidor na porta 5000 (por padrão).

2. **Testando a API:**

   - **No Navegador:**
     
     Digite a URL na barra de endereço, por exemplo:
     
     - Para buscar pela palavra **"OPERADORA"**:
     
       ```
       http://localhost:5000/search?query=OPERADORA
       ```
     
     - Para testar com outras palavras, substitua o valor de `query`:
     
       ```
       http://localhost:5000/search?query=DENTAL
       http://localhost:5000/search?query=ADMINISTRADORA
       ```

   - **No Postman:**

     1. Abra o Postman e crie uma requisição do tipo **GET**.
     2. Insira a URL de teste, por exemplo:
     
        ```
        http://localhost:5000/search?query=OPERADORA
        ```
     
     3. Clique em **Send** para enviar a requisição e visualizar a resposta.
