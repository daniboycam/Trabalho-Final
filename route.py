from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response


app = Bottle()
ctl = Application()


#-----------------------------------------------------------------------------
# Rotas:

@app.route('/pagina', methods=['GET'])
@app.route('/pagina/<username>', methods=['GET'])
def action_pagina(username=None):
    # Verifica o cookie de sessão
    session_id = request.get_cookie('session_id')
    
    # Verifica se a sessão existe e se o usuário corresponde ao nome no parâmetro
    if not session_id or username != ctl.get_authenticated_user(session_id):
        # Se não for o usuário autenticado, redireciona para o login
        return redirect('/portal')
    
    # Se autenticado, renderiza a página com o nome do usuário
    return ctl.render('pagina', username)


@app.route('/portal', method='GET')
def login():
    return ctl.render('portal')


@app.route('/portal', method='POST')
def action_portal():
    username = request.forms.get('username')
    password = request.forms.get('password')
    
    # Chama a função de autenticação para obter session_id
    session_id, username = ctl.authenticate_user(username, password)
    
    if session_id:
        # Se autenticado, cria o cookie de sessão e redireciona para a página do usuário
        response.set_cookie('session_id', session_id, httponly=True, secure=True, max_age=3600)
        redirect(f'/pagina/{username}')
    else:
        # Se falhar na autenticação, redireciona para o portal
        return redirect('/portal')


@app.route('/logout', method='POST')
def logout():
    ctl.logout_user()
    response.delete_cookie('session_id')
    redirect('/helper')

#-----------------------------------------------------------------------------


if __name__ == '__main__':

    run(app, host='localhost', port=8080, debug=True)
