# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import csv
import sys
from summa import summarizer
from PreProcessamento import PreProcesso
from ExtracaoSujeito import ExtracaoSujeito
from DBSCAN import Dbscan
reload(sys)
sys.setdefaultencoding('utf-8')

extrator = ExtracaoSujeito()
dataPath = 'C:/Users/Carlos/PycharmProjects/SumarizacaoGrafo/teste1.csv'
not_temas=['d','.','ok','10']
print '- - - - - - - - - - START - - - - - - - - - -'
reviews = []
print('========= Buscando Dados Treino =============')
p = PreProcesso()
d = Dbscan()
with open(dataPath, 'rb') as file:
    reader = csv.reader(file)
    for row in reader:
        #print(row)
        if len(row) == 2:
            if row[1] != "":
                frase = p.prePorcessar(row[0])
                #print (frase)
                reviews.append((frase,row[1],row[0]))
print('=========== DONE =============================')

print("DBSCAN")
print("Dados"+ str(len(reviews)))

#Chamando DBSCAN PASSANDO EPS=0.3 e MinPts= 5
clusters = d.dbScan(reviews,0.3,5)


print("FIM")
count = 0
topicos =[]
for cluster in clusters:
    count = count + 1

    c = 0
    comentario = ''
    for frase in cluster:
        comentario = comentario+frase[2]+" "

    topicos.append(comentario)
count = 0

#Juntando Cluster que possuem mesmo tema
print("=========== Resumo ================")
temas=[]
clusters =[]
for frase in topicos:
    try:
        tema = extrator.extrair(summarizer.summarize(frase,words=20,language='portuguese'))
        if tema not in temas:
            temas.append(tema)
            clusters.append(frase)
            print("Novo Tema: "+tema)
        else:
            ind = temas.index(tema)
            cluster = clusters[ind]
            clusters[ind] = cluster+" "+frase
    except:
        print("Sem Tema")

#IDENTIFICAÇÂO DE TEMA FINAL
print("========== TEMAS ===========")
for frase in clusters:

    try:
        tema = extrator.extrair(summarizer.summarize(frase, words=20, language='portuguese'))
        if tema not in not_temas:
            count += 1
            print("Cluster " + str(count))
            #print("Texto: "+frase)
            print("Tema: " + tema)
    except:
       print("Sem Tema")

print '- - - - - - - - - -  END  - - - - - - - - - -'