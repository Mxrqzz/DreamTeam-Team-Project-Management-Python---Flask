from app.database import create_connection, close_connection


class Tarefa:
    def __init__(self, nome, prazo, projeto_id):
        self.nome = nome
        self.prazo = prazo
        self.projeto_id = projeto_id

    def criar_tarefa(self):
        try:
            conexao = create_connection()
            if not conexao:
                raise Exception("Falha ao conectar com o banco de dados.")

            cursor = conexao.cursor()

            # Validação do nome da tarefa
            if not self.nome:
                raise ValueError("A tarefa precisa ter um nome válido.")

            # Inserir dados na tabela tarefas
            sql = """
                INSERT INTO tarefas (nome, prazo, projeto_id) 
                VALUES (%s, %s, %s)
            """
            values = (self.nome, self.prazo, self.projeto_id)
            cursor.execute(sql, values)
            conexao.commit()

            print(f"Tarefa '{self.nome}' criada com sucesso.")

        except Exception as e:
            print(f"Erro ao criar tarefa: {e}")
            raise

        finally:
            close_connection(conexao)

    @staticmethod
    def listar_tarefas(projeto_id):
        try:
            conexao = create_connection()
            if not conexao:
                raise Exception("Conexão ao banco de dados falhou.")

            cursor = conexao.cursor(dictionary=True)
            sql = """
                SELECT *
                FROM tarefas
                WHERE projeto_id = %s
                ORDER BY prazo ASC
            """
            cursor.execute(sql, (projeto_id,))
            tarefas = cursor.fetchall()
            return tarefas

        except Exception as e:
            print(f"Erro ao listar tarefas: {e}")
            return []
        finally:
            close_connection(conexao)
