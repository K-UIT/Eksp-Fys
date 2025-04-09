

def calc(a1,a2,n, f, m):
    M = m/1000
    T = 25+273
    R = 8.3144
    
    # Frekvens
    en = sum(a1)/(len(a1)*100)
    to = sum(a2)/(len(a2)*100)
    l = 2*(en-to)/(n+1)
    v = l*f
    
    # Adiabat
    gamma = (v**2*M)/(R*T)
    
    fri =(2/(gamma-1))
    
    print("Bølge lengde: ",l, " meter")
    print("Bølge hastighet: ", v, "m/s")
    print("Adiabatkonstant: ",gamma)
    print("Frihetsgrad: ", fri)


print("Luft:")
luft = 28.8
print("-"*40)

print("f = 546")
# f=546
# min = 2, node = 0
calc((55.6,55.8,55.8,56,55.7), (24,23.9,23.8,23.9,23.9),0, 546, luft)

print("\n\nf = 669")
# f=669
# min = 3, node = 1
calc((66.5,66.5,66.7,66.6,66.7), (15.9,15.3,15.5,15.6,15.4),1,669, luft)

print("\n\nf = 750")
# f=750
# min = 4, node = 2
calc((80.2,80,80.5,80.3,80.4), (11.2,11.1,11.3,11,11.1),2,750, luft)

print("-"*40)
print("\n\nArgon:")
argon = 40
print("-"*40)

print("f = 608")
# f=608
# min =3, node = 1
calc((68.9,69.4,69.5,68.4,69.1),(17,16.3,16.2,15.9,16.1),1,608,argon)

print("\n\nf = 760")
# f=760
# min =4, node = 2
calc((71.2,71.4,72.7,72.4,72.3),(8.6,7.7,7.6,7,7.5),2,760,argon)

print("\n\nf = 1410")
# f=1410
# min =7, node = 5
calc((73.1,73.7,73.8,73.6,73.7),(5.7,5.2,5.3,5.2,5.4),5,1410,argon)


