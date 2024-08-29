from dataclasses import dataclass
from rafacrud import Database
from urllib.parse import parse_qs, unquote_plus, unquote

db = Database('notes')

@dataclass
class note:
    titulo: str = "STRING"
    detalhes: str = 'STRING'
db.use(note)
def extract_route(request):
    route = request.split('\n')[0].split(' ')[1][1:].strip()
    return route
def read_file(path):
    with open(path, 'r+b') as f:
        return f.read()
def load_data():
    return db.get_all()
def load_template(path):
    with open('templates/'+path) as f:
        return f.read()
def deleteNote(request):
    titulo = unquote(request.split(' ')[1][7:])
    condition = f"titulo = '{titulo}'"
    print('.'+titulo+'.')
    db.delete(condition)
    db.commit()
def createNote(request):
    query_string = request.split('\n')[-1]
    parsed_query = parse_qs(query_string)
    titulo = unquote_plus(parsed_query.get("titulo", [""])[0])
    detalhes = unquote_plus(parsed_query.get("detalhes", [""])[0])
    db.add(note(titulo.strip(), detalhes))
    db.commit()
def buildResponse(body='', code=200, reason='OK', headers=''):
    response = f"HTTP/1.1 {code} {reason}\n"
    if headers:
        response += headers + "\n"
    response += f"\n{body}"
    return response.encode()

