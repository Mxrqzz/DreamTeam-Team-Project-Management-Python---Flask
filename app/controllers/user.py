from app.database import create_connection, close_connection

class User:
    def __init__(self, nome, username, email, senha):
        self.nome = nome
        self.username = username
        self.email = email
        self.senha = senha
        
    def salvar_dados(self):
        conexao = create_connection()
        
        if conexao:
            cursor = conexao.cursor()
            sql = "INSERT INTO usuarios (nome, username, email, senha) VALUES (%s, %s, %s, %s)"
            values = (self.nome, self.username, self.email, self.senha)
            
            try:
                cursor.execute(sql, values)
                conexao.commit()
                print(f"Usuario: {self.username} cadastrado com sucesso.")
            except Exception as e:
                print(f"Erro ao tentar Cadastro o usuario: {e}.")
            finally:
                cursor.close()
                close_connection(conexao)
                print("A Conexão com o banco de dados foi encerrada")
