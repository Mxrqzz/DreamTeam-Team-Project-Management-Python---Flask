from app.database import create_connection, close_connection


class Projects:
    def __init__(self, nome, descricao, data_inicio, data_fim, equipe_id, criado_id):
        self.nome = nome
        self.descricao = descricao
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.equipe_id = equipe_id
        self.criado_id = criado_id
        
    def criar_projeto(self):
        try:
            conexao = create_connection()
            if conexao:
                cursor = conexao.cursor()

                # Inserir dados na Tabela projetos
                sql = """
                INSERT INTO projetos (nome, descricao, data_inicio, data_fim, equipe_id, criador_id) 
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                values = (
                    self.nome,
                    self.descricao,
                    self.data_inicio,
                    self.data_fim,
                    self.equipe_id,
                    self.criado_id,
                )
                cursor.execute(sql, values)
                conexao.commit()

                print(f"Projeto {self.nome} cadastrado com sucesso.")

        except Exception as e:
            print(f"Erro ao criar projeto: {e}")
            raise  # Re-raise the exception for the controller to handle

        finally:
            if cursor:
                cursor.close()
            close_connection(conexao)
            print("Conexão com o banco de dados encerrada.")

    @staticmethod
    def listar_projetos(user_id):
        conexao = create_connection()

        if conexao:
            cursor = conexao.cursor()

            sql = """
                SELECT p.id, p.nome, p.descricao, p.data_inicio, p.data_fim, p.status, p.equipe_id, p.criado_em
                FROM projetos p
                JOIN equipe_membros em ON p.equipe_id = em.equipe_id
                WHERE em.user_id = %s
                ORDER BY p.criado_em DESC  -- Exemplo de ordenação
            """

            try:
                cursor.execute(sql, (user_id,))
                projetos = cursor.fetchall()
                if projetos:
                    return projetos
                else:
                    return None
            except Exception as e:
                print(f"Erro ao listar projetos: {e}")
                return None
            finally:
                cursor.close()
                close_connection(conexao)