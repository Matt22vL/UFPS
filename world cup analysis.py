import matplotlib.pyplot as plt
import numpy as np
"""
#datos
paises = ["Brasil", "Alemania", "Italia", "Argentina", "Francia", "Uruguay", "Inglaterra", "España", "Países Bajos", "Hungría", "Checoslovaquia", "Suecia", "Croacia"]
campeones = [5, 4, 4, 3, 2, 2, 1, 1, 0, 0, 0, 0, 0]
subcampeones = [2, 4, 2, 3, 1, 0, 0, 0, 3, 2, 2, 1, 1]
Anfitrion = [2, 2, 2, 1, 2, 1, 1, 1, 0, 0, 0, 1, 0]


x = np.arange(len(paises))

fig, ax = plt.subplots(figsize=(10, 6))


ax.bar(x - 0.4/2, campeones, 0.4, label="Campeón", color="gold")
ax.bar(x + 0.4/2, subcampeones, 0.4, label="Subcampeón", color="silver")

ax.bar(x,Anfitrion, 0.3,label="Anfitrion")

ax.set_xlabel("País")
ax.set_ylabel("Número de veces")
ax.set_title("campeones, subcampeones y anfitriones por país en la Copa del Mundo")
ax.set_xticks(x)
ax.set_xticklabels(paises, rotation=45, ha="right")
ax.legend()
plt.tight_layout()
plt.show()
"""

años_colombia = [1962, 1990, 1994, 1998, 2014, 2018]  
posiciones_colombia = [14, 14, 19, 21, 5, 9 ]  

x = np.arange(len(años_colombia))
y= np.arange(1,22)
fig, ax = plt.subplots(figsize=(10, 6))

print(y)

ax.bar(x,posiciones_colombia, 0.5,label="posicion")

ax.set_xlabel("año")
ax.set_ylabel("posicion")
ax.set_title("posicion de colombia en la Copa del Mundo")
ax.set_xticks(x)
ax.set_yticks(y)
ax.set_xticklabels(años_colombia)
plt.grid(axis="y", linestyle="--", alpha=0.7)  
ax.legend()
plt.tight_layout()
plt.show()
