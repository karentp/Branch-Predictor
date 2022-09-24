# Branch-Predictor
En este repositorio se presenta la implementación de cuatro predictores de saltos distintos: 

    1. Predictor bimodal
    2. Predictor global - GShared de dos niveles
    3. Predictor local - PShared de dos niveles
    4. Predictor Torneo


La implementación se realizo en el lenguaje de programación Python. Como datos para las pruebas se utilizó un archivo trace que contiene aproximadamente 16.000.000 de saltos condicionales, estos se obtuvieron ejecutando una aplicación del benchmark SPECInt 200, llamada GNU Compiler Collection. 

## Correr el programa

Para correr el programa se deben seguir los siguientes pasos:

1. Abra una consola de comandos en el directorio con los archivos
2. Asegurese que en el directorio se encuentra el archivo .gz
3. Corra: python branch_predictor.py  -s X  --bp X  --gh X --lh X
4. Debe sustituir X por un número según correspondan los parámetros

## Parámetros para correr el programa

1. --b corresponde al tipo de predictor:
    1. 0 : predictor bimodal
    2. 1 : predictor gshared
    3. 2 : predictor pshared
    4. 3 : predictor torneo
2. -s corresponde al número de bits menos significativos que se toman del PC para indexar la tabla
3. --gh corresponde al tamaño en bits del registro de historia global.
4. --lh corresponde al tamaño en bits del registro de historia global.

## Parámetros mínimos que necesitan los predictores:

Los predictores necesitan un mínimo de parámetros para ejecutar apropiadamente (si se dan parámetros adicionales a los mínimos requeridos por el predicto el programa correra adecuadamente).

1. Predictor bimodal: python branch_predictor.py  -s X  --bp 0 
2. Predictor gshared: python branch_predictor.py  -s X  --bp 1  --gh X
3. Predictor pshared: python branch_predictor.py  -s X  --bp 2  --lh X
4. Predictor torneo:  python branch_predictor.py  -s X  --bp 3  --gh X --lh X 
