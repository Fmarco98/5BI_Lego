'''
ID dei comandi.

Classi:
 - IDs
'''

class IDs:
    '''
    ID dei comandi.
    
    Settori:
     - Cingoli
     - Pistoni
     - Scarico
     - Scava
     - Torre
     - Lego
    '''
    class Cingoli:
        '''
        ID di categoria "Cingoli":
         - AVANTI
         - INDIETRO
         - DESTRA
         - SINISTRA
         - STOP
        '''
        AVANTI = 1
        INDIETRO = 2
        DESTRA = 3
        SINISTRA = 4
        STOP = 5
        
    class Pistoni:
        '''
        ID di categoria "Pistoni":
         - SU
         - GIU
         - STOP
        '''
        SU = 6
        GIU = 7
        STOP = 8
    
    class Scarico:
        '''
        ID di categoria "Scarico":
         - DESTRA
         - SINISTRA
         - STOP
        '''
        DESTRA = 9
        SINISTRA = 10
        STOP = 11
    
    class Scava:
        '''
        ID di categoria "Scava":
         - START
         - STOP
        '''
        START = 12
        STOP = 13
    
    class Torre:
        '''
        ID di categoria "Torre":
         - DESTRA
         - SINISTRA
         - STOP
        '''
        DESTRA = 14
        SINISTRA = 15
        STOP = 16
    
    class Lego:
        '''
        ID di categoria "Lego":
         - ON
         - OFF
        '''
        ON = 17
        OFF = 18
