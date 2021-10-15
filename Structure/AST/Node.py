

class Node():

    def __init__(self, token:str, lexema :str) -> None:
        self.token = token
        self.lexema = lexema
        self.hijos = []

    def AddHijo(self, node):
        self.hijos.append(node)

    def getToken(self):
        return self.token

    def GraficarSintactico(self):
        grafica = 'digraph {\n\n' + self.GraficarNodos(self, "0") + '} \n\n}'
        return grafica;

    def GraficarNodos(self,nodo, i: str):
        k = 0;
        r = "";
        nodoTerm : str = nodo.token;
        r = 'node' +i +'[label = \"' + nodoTerm + '\"];\n'

        
        for j in range(0, len(nodo.hijos)):
            r = r + 'node' + i + ' -> node'+ i + str(k) + '\n'
            r = r + self.GraficarNodos(nodo.hijos[j], ""+i+str(k));
            k = k + 1;
        
        """
        if not (nodo.lexema.match('')) or  not(nodo.lexema.match("")):
            nodoToken = nodo.lexema;
            nodoToken = nodoToken.replace("\"","");
            r = r + 'node'+i + 'c[label = \"'+ nodoToken + '\"];\n'
            r = r + 'node' + i + ' -> node' + i + 'c\n'
        """
        return r;
    
    