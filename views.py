from utils import *

def index():
    note_template = load_template('components.html')
    
    # Gerar o HTML para cada anotação
    notes_html = ''
    for dados in load_data():
        notes_html += '\n' + note_template.format(
            title=dados['titulo'],
            text=dados['detalhes'],
            dataid=f"'{dados['titulo']}'"
        )
    
    # Carregar o template principal e inserir as anotações
    body = load_template('index.html').format(notes=notes_html)
    
    # Utilizar buildResponse para criar a resposta
    response = buildResponse(body=body, code=200, reason='OK', headers='Content-Type: text/html\r\n')
    return response
def postResponses(request):
    if request.split('\n')[0][5:12].strip() == '/delete': 
        deleteNote(request)  # Supondo que essa função cria uma nova nota
    elif 'titulo=' in request and 'detalhes=' in request:
        createNote(request)
    return buildResponse(code=303, reason='See Other', headers='Location: /')