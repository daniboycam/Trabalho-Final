from app.controllers.datarecord import DataRecord
from bottle import template, redirect, route

class Application():

    def __init__(self):
        # Definindo as páginas
        self.pages = {
            'pagina': self.pagina
        }

        # Composição do objeto DataRecord dentro de self.models
        self.models = DataRecord()

    def render(self, page, parameter=None):
        """Método para renderizar as páginas."""
        content = self.pages.get(page, self.helper)
        if not parameter:
            return content()
        else:
            return content(parameter)

    @route('/pagina/<parameter>')
    def pagina(self, parameter):
        """Método para processar a página e tratar os dados do modelo."""
        # Usando o modelo para obter os dados com o parâmetro da URL
        info = self.models.work_with_parameter(parameter)
        if not info:
            redirect('/pagina')  # Redireciona caso não encontre o usuário
        else:
            # Retornando a página com os dados do usuário
            return template('app/views/html/pagina', transfered=True, data=info)

    @route('/pagina')
    def pagina_sem_parametro(self):
        """Método para renderizar a página sem parâmetro, caso não seja fornecido."""
        return template('app/views/html/pagina', transfered=False)
