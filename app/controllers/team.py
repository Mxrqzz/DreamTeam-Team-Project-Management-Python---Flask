from app.database import create_connection, close_connection

class Team:
    def __init__(self, nome, descricao,criador_id):
        self.nome = nome
        self.descricao = descricao
        self.criador_id = criador_id

        
    def criar_equipe(self):
        conexao = create_connection()
        
        if conexao:
            cursor = conexao.cursor()
            try:
                #! Inserindo dados na Tabela equipes
                sql = "INSERT INTO equipes (nome, descricao, criador_id) VALUES (%s, %s, %s)"
                values = (self.nome, self.descricao, self.criador_id)
                cursor.execute(sql, values)
                conexao.commit()
                
                #*Obter Id da Equipe recem criada
                equipe_id = cursor.lastrowid
                
                #!Inserir o criador da equipe na tabela equipe_membros
                
                sql_membro = "INSERT INTO equipe_membros (equipe_id, user_id, cargo) VALUES (%s, %s, %s)"
                values_membro = (equipe_id, self.criador_id, "admin")
                cursor.execute(sql_membro, values_membro)
                conexao.commit()
                
                print(f"Equipe {self.nome} cadastrada com sucesso.")
                
            except Exception as e:
                print(f"Erro ao criar equipe: {e}")
            finally:
                cursor.close()
                close_connection(conexao)
                print("A Conexão com o banco de dados foi encerrada.")

    @staticmethod
    def listar_equipes(user_id):
        conexao = create_connection()

        if conexao:
            cursor = conexao.cursor()

            sql = """
                SELECT 
                    equipes.id, 
                    equipes.nome, 
                    equipes.descricao, 
                    equipes.criado,
                    (SELECT COUNT(*) FROM equipe_membros WHERE equipe_membros.equipe_id = equipes.id) AS qtd_membros,
                    equipe_membros.cargo
                FROM equipes
                JOIN equipe_membros ON equipes.id = equipe_membros.equipe_id
                WHERE equipe_membros.user_id = %s
                GROUP BY equipes.id, equipe_membros.cargo
            """

            try:
                cursor.execute(sql, (user_id,))
                equipes = cursor.fetchall()
                if equipes:
                    return equipes
                else:
                    return None
            except Exception as e:
                print(f"Erro ao listar equipes: {e}")
                return None
            finally:
                cursor.close()
                close_connection(conexao)