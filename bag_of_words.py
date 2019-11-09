from textblob import TextBlob
from scipy import spatial
import pandas as pd
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

tags_ingore = ['CC', 'DT', 'NO', 'LS', 'POS', 'SYM', 'TO', 'UH', 'CD', 'IN', ',', '.', '(', ')']

# Retorna um vetor com todas as palavras importantes do texto
def extrair_palavras(lista_de_textos):
  relacao_de_palavras = []
  relacao_de_palavras_distintas = []
  resultado = []
  
  for text in lista_de_textos:
    texto = TextBlob(text)
    palavras = texto.tags

    for sub, subs in palavras:
      if (not str(subs) in tags_ingore):
        relacao_de_palavras.append(str(sub.encode('utf-8')))
    
    relacao_de_palavras_distintas = list(set(relacao_de_palavras))
    relacao_de_palavras_distintas.reverse()
    resultado.append(relacao_de_palavras_distintas)
    relacao_de_palavras = []

  return resultado 
 
# Retorna um vetor de palavras distintas, ou seja, remove palavras duplicadas
def gerar_vetor_principal(lista_de_vetores):
  vetor_principal = []

  for vetor in lista_de_vetores:
    for palavra in vetor:
      vetor_principal.append(palavra)

  
  vetor_principal = list(set(vetor_principal))

  return vetor_principal

# Metodo que conta a quantidade de palavras contidas
def conta_palavras(palavra, texto):
  cont = 0
  for word in texto.split():
    word2 = word.replace(',','')
    if palavra.upper() == word2.upper():
      cont += 1

  return cont

# Constroi vetor de relacao
def gerar_vetor_de_relacao(vetor_principal, texto):
  vetor_de_equivalencia = []
  for palavra in vetor_principal:
    vetor_de_equivalencia.append(conta_palavras(palavra, texto))
  
  return vetor_de_equivalencia


resultado_final = []
print("Os textos do dataset estao sendo processados ...")
documentos = pd.read_csv('movie.csv', encoding="utf-8")
titulos = documentos['title'].tolist()
vetor_de_vetores_dataset = extrair_palavras(titulos)
print("Textos processados com sucesso !")

if sys.version_info.major == 2:
    query = raw_input('Informe a query: ')
elif sys.version_info.major == 3:
    query = input('Informe a query: ')

print("")

vetor_da_query = extrair_palavras([query])[0]

for i, titulo in enumerate(titulos):
  #Gerando vetor principal entre a query e as linha do dataset
  vetor_principal_corrente = gerar_vetor_principal([ vetor_de_vetores_dataset[i] , vetor_da_query ])
  
  #gerando vetor de relacao entre titulo/linha corrente e o vetor principal
  vetor_de_relacao_do_titulo = gerar_vetor_de_relacao(vetor_principal_corrente, titulo)

  #gerando vetor de relacao entre query corrente e o vetor principal
  vetor_de_relacao_da_query = gerar_vetor_de_relacao(vetor_principal_corrente, query)


  #Evita erro de vetores zerados
  if sum(vetor_de_relacao_do_titulo) > 0 and sum(vetor_de_relacao_da_query) > 0:
    similaridade = 1 - spatial.distance.cosine(vetor_de_relacao_do_titulo, vetor_de_relacao_da_query)
  else:
    similaridade = 0

  if similaridade >= 0.80:
    resultado_final.append([titulo,similaridade])


resultado_ordenado = sorted(resultado_final, key = lambda x: x[1], reverse=True)

for result in resultado_ordenado:
  print('Filme: ' + result[0] + ' | Proximida: ' + str(round(result[1],3) * 100) + '%'  )
  print('')