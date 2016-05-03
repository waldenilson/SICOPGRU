from django.views.static import serve
from django.contrib.auth.decorators import permission_required

@permission_required('project.processo_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def download(request, path, document_root):
    return serve(request, path, document_root)
