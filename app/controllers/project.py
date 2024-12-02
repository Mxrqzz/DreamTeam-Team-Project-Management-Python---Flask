from app.database import create_connection, close_connection


class Projects:
    def __init__(self, nome, descricao, equipe_id, criador_id):
        self.nome = nome
        self.descricao = descricao
        self.equipe_id = equipe_id
        self.criador_id = criador_id

    def criar_projeto(self):
        try:
            conexao = create_connection()
            if not conexao:
                raise Exception("Falha ao conectar com o banco de dados.")

            cursor = conexao.cursor()

            # Validação do nome do projeto
            if not self.nome:
                raise ValueError("O projeto precisa ter um nome válido.")

            # Verificar se o projeto já existe
            cursor.execute("SELECT * FROM projetos WHERE nome=%s", (self.nome,))
            existing_project = cursor.fetchone()

            if existing_project:
                raise ValueError("Já existe um projeto com esse nome.")

            # Inserir dados na tabela projetos
            sql = """
                INSERT INTO projetos (nome, descricao, equipe_id, criador_id) 
                VALUES (%s, %s, %s, %s)
            """
            values = (self.nome, self.descricao, self.equipe_id, self.criador_id)
            cursor.execute(sql, values)
            conexao.commit()

            print(f"Projeto '{self.nome}' cadastrado com sucesso.")

        except Exception as e:
            print(f"Erro ao criar projeto: {e}")
            raise  # Re-lançar a exceção para que o controlador lide com ela

        finally:
            # Certifique-se de que os recursos sejam liberados corretamente
            if 'cursor' in locals():
                cursor.close()
            close_connection(conexao)
            print("Conexão com o banco de dados encerrada.")

    @staticmethod
    def listar_projetos(equipe_id=None):
        try:
            conexao = create_connection()
            if not conexao:
                raise Exception("Falha ao conectar com o banco de dados.")

            cursor = conexao.cursor()

            if equipe_id:
                # Consultar projetos específicos de uma equipe
                sql = """
                    SELECT id, nome, descricao, status, criado_em 
                    FROM projetos 
                    WHERE equipe_id = %s
                """
                cursor.execute(sql, (equipe_id,))
            else:
                # Consultar todos os projetos
                sql = """
                    SELECT id, nome, descricao, status, criado_em 
                    FROM projetos
                """
                cursor.execute(sql)

            projetos = cursor.fetchall()
            return projetos

        except Exception as e:
            print(f"Erro ao listar projetos: {e}")
            return None

        finally:
            close_connection(conexao)
            print("Conexão com o banco de dados encerrada.")