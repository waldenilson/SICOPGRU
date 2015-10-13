# -- coding: utf-8 --

def read_exemple_return_siafi():
	pass

def iniciar_calculo( dados, data_requerimento, nossa_escola ):
    print 'INICIANDO CALCULO'
    print data_requerimento
    print nossa_escola
    print dados

def carregar_parcelas( dados ):
    pass



def calcular( dados, data_requerimento, nossa_escola ):

	#principal_corrigido_multa = 0
	#instance = get_object_or_404(Tbextrato, id=id)
	modulos = instance.tamanho_modulos_fiscais
	vencimento = instance.data_vencimento_primeira_prestacao
	#municipio = Tbmunicipio.objects.all()
	#hoje = date.today()
	prestacao = float(instance.valor_imovel)/17.0
	#data_titulacao = vencimento.replace(vencimento.year - 3)
	#area = instance.area_medida
	#instance.valor_imovel.quantize(Decimal('1.00'))
	#dtrequerimento = None
    #icorrecao = 3.7779 #mudar para indice correto
    
    imulta = 1.0

	ijuros = 0.0
    #definicao de qual taxa de juros vai utilizar    
	if dados['modulo_fiscal'] > 4:
		ijuros = 6.75
	else:
		if dados['valor_imovel'] <= 40000:
			ijuros = 1.0
		else: 
			if dados['valor_imovel'] > 40000 and dados['valor_imovel'] <= 100000:
				ijuros = 2.0
			else: 
				if dados['valor_imovel'] > 100000:
					ijuros = 4.0

	#for i in range(1,18):            
		#verifica = verificavencimento(request,dtrequerimento,vencimento,ijuros,prestacao,titulado,None,i,imulta,stNossaEscola,instance)

def verificavencimento(request,
	data_requerimento,
	ijuros,
	prestacao,
	numero_parcela,
	imulta,
	nossa_escola,
	dados):

    correcao = 0
    principal = 0 
    principal_juros_correcao = 0
    multa = 0
    desconto = 0
    principal_corrigido_desconto = 0
    principal_corrigido_multa = 0
    dtgeracao = None
    stgerada =False
    data = None
    
    if dtrequerimento < dtvencimento: # nao vencido
        print "nao vencido"
        if (dtvencimento - dtrequerimento).days < 30:
            #incide juros de emissao titulo ateh vencimento parcela
            dias_juros = (dtvencimento - titulado).days
            dtvencGRU = dtvencimento
            print "dias_juros ",(dias_juros)
            juros = float(prestacao)*((float(dias_juros)/360.)*(ijuros/100.0))
            prestacao_juros = prestacao + juros
            principal_corrigido = prestacao_juros
            imprime(prestacao_juros,"prestacao_juros")
            
        else:
            if (dtvencimento - dtrequerimento).days > 30:
                print "nao vencido - mais de 30 dias"   
                #incide juros de emissao titulo ate dtrequerimento + 30 dias
                dias_juros = (dtrequerimento - titulado).days + 30
                dtvencGRU = dtrequerimento + timedelta(30)
                juros = float(prestacao)*((float(dias_juros)/360.)*(ijuros/100.0))
                prestacao_juros = prestacao + juros
                principal_corrigido = prestacao_juros
                
                imprime(prestacao_juros,"prestacao_juros")
                print "dias_juros " ,dias_juros,"prestacao ",prestacao," ijuros ",ijuros
                print "juros ",juros            
    else:
        if dtrequerimento > dtvencimento: # vencido
            print"vencido "
            print"prestacao" ,prestacao
            #incide multa,correcao (a partir do dtVencParcela ) e juros (apartir de dtEmissaoTitulo)
            # juros de emissao ateh dtrequerimento + 30 dias - incidencia aa
            dias_juros = (dtrequerimento - titulado).days + 30
            dtvencGRU = dtrequerimento + timedelta(30)
            juros = float(prestacao)*((float(dias_juros)/360.)*(ijuros/100.0))
            print "juros ",juros
            prestacao_juros = prestacao + juros
            print "prestacao_juros",prestacao_juros            

            # correcao de vencimento ate dtrequerimento + 30 dias
            # falta obter a correcao correta a ser aplicada de acordo com tabela do governo
            dias_correcao = (dtrequerimento - dtvencimento).days + 30
            
            #calcular a correcao: TbtrMensal
            icorrecao = calculo_tr()

            correcao = prestacao_juros*((icorrecao/100.0))
            print"correcao",correcao
            print "icorrecao",icorrecao
            principal_juros_correcao = prestacao_juros + correcao
            

            # multa de vencimento ateh dtrequerimento + 30 dias
            multa = ((float(dias_correcao))/30)*float(imulta)/100*float(principal_juros_correcao)  
            principal_corrigido = principal_juros_correcao + multa
            
            print "principal_corrigido ", principal_corrigido
            print "dtvencGRU ",dtvencGRU
            print "multa",multa
    referencia = str(instance.numero_processo[0:5])+str(instance.id_req[2:6])+str(numero_parcela)+str(0) #mudar qdo titulo vier do sisterleg
    if stNossaEscola:
        desconto = principal_corrigido / 2
        principal_corrigido = desconto

    #copiei para gerarGRU
    if obj is not None:
        if request.POST.get(str(obj.id)+'-parcela', False):
                #a parcela que forem marcadas devem ser geradas GRU caso nao tenham sido pagas 
                print "parcela"+ str(obj.parcela)+" marcou. Pago = " + str(obj.stpaga)
                dtgeracao = datetime.date.today()
                stgerada = True
                #cria um json para passar para o template que vai exibir a GRU
                data = {}
                data['recolhimento'] = "28874-8"
                data['prestacao'] = "{0:.2f}".format(prestacao)
                data['cpf'] = instance.cpf_req
                data['cdug'] = obj.cdug
                data['nome'] = instance.nome_req
                data['vencimento'] = dtvencimento
                data['referencia'] = referencia
                data['desconto'] = "{0:.2f}".format(desconto)
                data['multa'] = "{0:.2f}".format(multa)
                data['juros'] = "{0:.2f}".format(juros)
                data['total'] = "{0:.2f}".format(principal_corrigido)
                data['gerada'] = stgerada
                #messages.add_message(request,messages.WARNING,'GRU GERADA')
        else:
            #parcelas nao marcadas
            print "parcela"+ str(obj.parcela)+" nao marcou. Pago = " + str(obj.stpaga)

    #ateh aqui
    return locals()
   