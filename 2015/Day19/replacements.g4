grammar replacements;

e   : h f
    | n al
    | o mg
;

h   : c rn al ar
    | c rn f y f y f ar
    | c rn f y mg ar
    | c rn mg y f ar
    | h ca
    | n rn f y f ar
    | n rn mg ar
    | n th
    | o b
    | o rn f ar
    | H
;

al  : th f
    | th rn f ar
    | AL
;

ca  : ca ca
    | p b
    | p rn f ar
    | si rn f y f ar
    | si rn mg ar
    | si th
    | CA
;

f   : ca f
    | p mg
    | si al
    | F
;

mg  : b f
    | ti mg
    | MG
;

n   : c rn f ar
    | h si
    | N
;

o   : c rn f y f ar
    | c rn mg ar
    | h p
    | n rn f ar
    | o ti
    | O
;

p   : ca p
    | p ti
    | si rn f ar
    | P
;

si  : ca si
    | SI
;

th  : th ca
    | TH
;

b   : b ca
    | ti b
    | ti rn f ar
    | B
;
ti  : b p
    | ti ti
    | TI
;

// Missing parser/lexer correspondings.

c : C ;
y : Y ;
rn: RN;
ar: AR;






H : 'H' ;
AL: 'Al';
B : 'B' ;
CA: 'Ca';
F : 'F' ;
MG: 'Mg';
N : 'N' ;
O : 'O' ;
P : 'P' ;
SI: 'Si';
TH: 'Th';
TI: 'Ti';
RN: 'Rn';
AR: 'Ar';
C : 'C' ;
Y : 'Y' ;
