from textblob import TextBlob
from scipy import spatial

tags_ingore = ['CC', 'DT', 'NO', 'LS', 'POS', 'SYM', 'TO', 'UH']

def extrair_palavras(lista_de_textos):
  
  relacao_de_palavras = []
  
  for text in lista_de_textos:
    texto = TextBlob(text)
    palavras = texto.tags

    for sub, subs in palavras:
      if (not str(subs) in tags_ingore):
        relacao_de_palavras.append(str(sub))
  
  return relacao_de_palavras # retorna um vetor com todas as palavras contidas nos textos

 
def gerar_vetor_principal(lista_de_vetores): 
  vetor_principal = []

  for vetor in lista_de_vetores:
    for palavra in vetor:
      vetor_principal.append(palavra)

  
  vetor_principal = list(set(vetor_principal)) # gera lista de elementos distintos

  return vetor_principal # retorna vetor de elementos distintos


def gerar_vetor_de_relacao(vetor_principal, texto):
  vetor_de_equivalencia = []
  for palavra in vetor_principal:
    vetor_de_equivalencia.append(texto.count(palavra))
  
  return vetor_de_equivalencia



#Extract noun
frase1 = "It can be tedious to repeatedly pass taggers, NP extractors, sentiment tedious analyzers, classifiers, and tedious tokenizers to tedious multiple TextBlobs. To keep your code DRY, you can use the Blobber class to create TextBlobs that share the same models."

# frase2 = "It can be tedious to repeatedly pass taggers, NP extractors."

frase2 = "It can be tedious to repeatedly pass taggers, NP extractors, sentiment tedious analyzers, classifiers, and tedious tokenizers to tedious multiple TextBlobs."


total_de_palavras = extrair_palavras([frase1,frase2])

vetor_principal = gerar_vetor_principal([total_de_palavras])

vetor_de_equivalencia1 = gerar_vetor_de_relacao(vetor_principal, frase1)

print(vetor_de_equivalencia1)

vetor_de_equivalencia2 = gerar_vetor_de_relacao(vetor_principal, frase2)

print(vetor_de_equivalencia2)

result = 1 - spatial.distance.cosine(vetor_de_equivalencia1, vetor_de_equivalencia2)

print(result)