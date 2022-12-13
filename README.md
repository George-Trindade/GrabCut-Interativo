# GrabCut-Interativo
Implementação por meio do código base do GrabCut, fornecido pelo o OpenCV.
Com base em revisões bibliográficas e em testes realizados com as versões disponíveis do algoritmo GrabCut no OpenCV,  foram observadas limitações no funcionamento, tais como: não é possível segmentar vários objetos em uma imagem; o desenho do retângulo não é interativo, logo o usuário teria que informar o tamanho (coordenadas, largura e altura) manualmente; a segmentação só acontece na área limitada pelo o retângulo e o processo de desenho do mesmo só acontece uma vez; não possui interface interativa para o usuário retocar os detalhes e melhorar o resultado da segmentação. Esta implementação contribuiu para resolver estes problemas, melhorando o funcionamento do algoritmo e a experiência do usuário. Além disso, foram desenvolvidas novas funcionalidades, como o processo de corte do objeto na imagem e a possibilidade de salvar os resultados da segmentação.
# Uso
```
python grabcut-interativo.py imagem.extensão

```
**Exemplo:** python3 grabcut-interativo.py carros.jpg

# Execução
1. Use o botão direito do mouse para selecionar a área ou objeto de interesse, desenhando um retângulo em volta. Após a seleção, pressione a tecla "n' para realizar a segmentação. 
2. Para realizar as interações, utilize as teclas de atalho, para as funções de selecionar (teclas 0,1,2,3), use o botão esquerdo do mouse, como um espécie de pincel.
4. Após as interações, aperte "n" para atualizar o processo.
5. Teclas de Atalho:
    - Aperte '0' - Para selecionar áreas que são fundo óbvio do objeto
    - Aperte '1' - Para selecionar áreas que são partes óbvias do objeto
    - Aperte '2' - Para selecionar áreas que são prováveis de serem fundo do objeto
    - Aperte '3' - Para selecionar áreas que são prováveis de serem partes do objeto
    - Aperte 'n' - Para realizar e/ou atualizar a segmentação
    - Aperte 'f' - Para realizar o corte do objeto 
    - Aperte 'r' - Para desfazer todas as alterações
    - Aperte 's' - Para salvar os resultados da segmentação
    - Aperte 'Esc' - Para sair
