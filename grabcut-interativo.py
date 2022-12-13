
'''
===============================================================================
Segmentação através do OpenCV com GrabCut.

Use o botão direito do mouse para selecionar a área ou objeto de interesse, desenhando um retângulo em volta:

Teclas de Atalho:
    Aperte '0' - Para selecionar áreas que são fundo óbvio do objeto
    Aperte '1' - Para selecionar áreas que são partes óbvias do objeto
    Aperte '2' - Para selecionar áreas que são prováveis de serem fundo do objeto
    Aperte '3' - Para selecionar áreas que são prováveis de serem partes do objeto
    Aperte 'n' - Para realizar e/ou atualizar a segmentação
    Aperte 'f' - Para realizar o corte do objeto 
    Aperte 'r' - Para desfazer todas as alterações
    Aperte 's' - Para salvar os resultados da segmentação
    Aperte 'Esc' - Para sair
===============================================================================
'''

from __future__ import print_function

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import sys
from PIL import Image
class App():
    #Cores dos indicadores do mouse
    BLUE = [255,0,0]        # Cor do retângulo
    RED = [0,0,255]         # Cor do fundo provavel
    GREEN = [0,255,0]       # Cor das partes provaveis do objeto
    BLACK = [0,0,0]         # Cor do fundo obvio
    WHITE = [255,255,255]   # Cor das partes obvias do objeto

    #Adicionando as cores as ações de cada tecla
    DRAW_BG = {'color' : BLACK, 'val' : 0}     #Fundo
    DRAW_FG = {'color' : WHITE, 'val' : 1}     #Objeto
    DRAW_PR_BG = {'color' : RED, 'val' : 2}    #Fundo Provavel
    DRAW_PR_FG = {'color' : GREEN, 'val' : 3}  #Parte do objeto Provavel

    #Manipuladores das Condicionais
    rect = (0,0,1,1)
    drawing = False         # Retoques do objeto
    rectangle = False       # Retangulo da área selecionada
    rect_over = False       # Verificar se o retângulo foi desenhado
    rect_or_mask = 100      # Controlar a Mascara dentro do retangulo
    value = DRAW_FG         # Limites do objeto selecionado(pega o ponto inicial)
    thickness = 3           # Tamanho do pincel de retoque

    def onmouse(self, event, x, y, flags, param):
        # Desenhar retângulo
        if event == cv.EVENT_RBUTTONDOWN:
            self.rectangle = True
            self.ix, self.iy = x,y

        elif event == cv.EVENT_MOUSEMOVE:
            if self.rectangle == True:
                self.img = self.img2.copy()
                cv.rectangle(self.img, (self.ix, self.iy), (x, y), self.BLUE, 2)
                self.rect = (min(self.ix, x), min(self.iy, y), abs(self.ix - x), abs(self.iy - y))
                self.rect_or_mask = 0

        elif event == cv.EVENT_RBUTTONUP:
            self.rectangle = False
            self.rect_over = True
            cv.rectangle(self.img, (self.ix, self.iy), (x, y), self.BLUE, 2)
            self.rect = (min(self.ix, x), min(self.iy, y), abs(self.ix - x), abs(self.iy - y))
            self.rect_or_mask = 0
            print(" Agora pressione a tecla 'n' para realizar a segmentação.  \n")

        # Realizar os retoques finais

        if event == cv.EVENT_LBUTTONDOWN:
            if self.rect_over == False:
                print("Desenhe um retângulo para selecionar a área ou objeto de interesse \n")
            else:
                self.drawing = True
                cv.circle(self.img, (x,y), self.thickness, self.value['color'], -1)
                cv.circle(self.mask, (x,y), self.thickness, self.value['val'], -1)

        elif event == cv.EVENT_MOUSEMOVE:
            if self.drawing == True:
                cv.circle(self.img, (x, y), self.thickness, self.value['color'], -1)
                cv.circle(self.mask, (x, y), self.thickness, self.value['val'], -1)

        elif event == cv.EVENT_LBUTTONUP:
            if self.drawing == True:
                self.drawing = False
                cv.circle(self.img, (x, y), self.thickness, self.value['color'], -1)
                cv.circle(self.mask, (x, y), self.thickness, self.value['val'], -1)

    def run(self):
        i=0
        # Carregar a imagem
        if len(sys.argv) == 2:
            filename = sys.argv[1] # Pega o segundo (img) parâmetro de entrada -> [0-'codigo.py',1-'img.png']
        else:
            print("Nenhuma imagem de entrada foi fornecida, com isso, carregando uma imagem padrão de exemplo, exemplo.png \n")
            print("Uso correto: python <algoritmo.py> <Nomeimagem.extensão> \n")
            filename = 'exemplo.png'

        self.img = cv.imread(cv.samples.findFile(filename))
        self.imgOriginal = cv.imread(cv.samples.findFile(filename))
        self.img2 = self.img.copy()                                
        self.mask = np.zeros(self.img.shape[:2], dtype = np.uint8) # Mascara de 0-1 das dimensões da imagem
        self.output = np.zeros(self.img.shape, np.uint8)           # imagem de saida, inicialmente toda "preta"(0)
        self.saidaImagem=self.imgOriginal.copy()
        self.saidaInversa = np.zeros(self.img.shape, np.uint8)     # imagem de saida inversa, inicialmente toda "preta"(0)
        # Entrada e Saída das Janelas do Prompt(Windows)
        cv.namedWindow('Saida')
        cv.namedWindow('Entrada')
        cv.setMouseCallback('Entrada', self.onmouse)
        cv.moveWindow('Saida', self.img.shape[1]+10,90)

        print(" Desenhe um retângulo ao redor do objeto usando o botão direito do mouse \n")

        while(1):

            cv.imshow('Saida', self.output)
            cv.imshow('Entrada', self.img)
            k = cv.waitKey(1)

            # Condição das teclas de atalho
            if k == 27:         # Tecla Esc para Sair
                break
            elif k == ord('0'): # Para selecionar áreas que são fundo óbvio do objeto
                print(" Marque regiões de fundo com o botão esquerdo do mouse \n")
                self.value = self.DRAW_BG
            elif k == ord('1'): # Para selecionar áreas que são partes óbvias do objeto
                print(" Marque regiões do objeto com o botão esquerdo do mouse \n")
                self.value = self.DRAW_FG
            elif k == ord('2'): # Para selecionar áreas que são prováveis de serem fundo do objeto
                self.value = self.DRAW_PR_BG
            elif k == ord('3'): # Para selecionar áreas que são prováveis de serem partes do objeto
                self.value = self.DRAW_PR_FG
            elif k == ord('s'): # Salvar os resultados em imagem  
                #bar = np.zeros((self.img.shape[0], 5, 3), np.uint8)
                #res = np.hstack((self.img2, bar, self.img, bar, self.output))
                #corte = self.img2-self.output
                
                cv.imwrite('Imagem_Cortada.png',self.img2)
                cv.imwrite('Objetos_Segmentados.png',self.saidaInversa)

                #cv.destroyWindow('Entrada')
                #cv.destroyWindow('Saida')
                cv.destroyAllWindows()
                #Imagem Original
                #cv.imshow('Imagem Original',self.imgOriginal)
                plt.subplots(1)
                plt.imshow(cv.cvtColor (self.imgOriginal, cv.COLOR_BGR2RGB))
                plt.title('Imagem Original')
            
                #Imagem sem os Objetos
                #cv.imshow('grabcut_Final',self.img2)
                plt.subplots(1)
                plt.imshow(cv.cvtColor (self.img2, cv.COLOR_BGR2RGB))
                plt.title('Imagem com os objetos cortados')
                

                #Imagem dos objetos sem o fundo
                #cv.imshow('Imagem Inversa',self.saidaInversa)
                plt.subplots(1)
                plt.imshow(cv.cvtColor (self.saidaInversa, cv.COLOR_BGR2RGB))
                plt.title('Imagem dos objetos sem o fundo')
                plt.show()
                
                
                print(" Resultados salvos em Imagem! \n")
                
            elif k == ord('f'):
                i+=1
                corte = self.img2-self.output #Realiza o corte do objeto na imagem
                cv.imwrite('grabcut_output'+str(i)+'.png', self.output)
                cv.imshow('grabcut_output'+str(i), self.output)
                self.img=corte  #Atualiza a imagem para a nova versão cortada
                self.img2=corte #Atualiza a imagem da entrada para a nova versão cortada
                self.saidaInversa=self.saidaInversa+self.output
            elif k == ord('r'): # Desfazer alterações
                print("Desfazendo alterações... \n")
                self.rect = (0,0,1,1)
                self.drawing = False
                self.rectangle = False
                self.rect_or_mask = 100
                self.rect_over = False
                self.value = self.DRAW_FG
                self.img = self.imgOriginal.copy()
                self.img2= self.imgOriginal.copy()
                self.mask = np.zeros(self.img.shape[:2], dtype = np.uint8) # Mascara de 0-1 das dimensões da imagem
                self.output = np.zeros(self.img.shape, np.uint8)           # imagem de saida, inicialmente toda "preta"(0)
            elif k == ord('n'): # Processo de segmentação
                print(""" Para fazer retoques finais de forma manual, use as teclas de atalho [0,1,2,3]. 
                \n Depois aperte 'n' para atualizar a segmentação: \n""")
                try:
                    bgdmodel = np.zeros((1, 65), np.float64)
                    fgdmodel = np.zeros((1, 65), np.float64)
                    if (self.rect_or_mask == 0):         # retangulo
                        cv.grabCut(self.img2, self.mask, self.rect, bgdmodel, fgdmodel, 1, cv.GC_INIT_WITH_RECT)
                        self.rect_or_mask = 1
                    elif (self.rect_or_mask == 1):       # mascara do objeto
                        cv.grabCut(self.img2, self.mask, self.rect, bgdmodel, fgdmodel, 1, cv.GC_INIT_WITH_MASK)
                except:
                    import traceback
                    traceback.print_exc()

            mask2 = np.where((self.mask==1) + (self.mask==3), 255, 0).astype('uint8') #máscara 0 ao redor do objeto
            #Mantém o objeto na posição original da imagem, tornando tudo que é fundo com máscara 0
            self.output = cv.bitwise_and(self.img2, self.img2, mask=mask2)  
            
        print('Sucesso!')


if __name__ == '__main__':
    print(__doc__) #Mostrar as instruções 
    App().run()    #Executar e  abrir as janelas 
    cv.destroyAllWindows() #Fechar as janelas após a interrupção