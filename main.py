import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from clases import Huevito, Item


#Se usan tuplas para mejor lectura en usuario común
#El órden es ("NOMBRE", precio, "PROBABILIDAD%")

buebito_price = 1_000_000   # Precio por buebito
n_boxes = 100               # buebitos por simulación
n_trials = 1000             # Cantidad de simulaciones
rng = 1                     # Semilla de RNG

item_data = [
    ("Armor +13 Refine Ticket", 700_000_000, "0,0250%"),
    ("Weapon +13 Refine Ticket", 700_000_000, "0,0300%"),
    ("Boots Modifying Cube", 400_000_000, "0,0350%"),
    ("Low Refining Envelope", 100_000_000, "0,0500%"),
    ("Scythe of Evil [1]", 130_000_000, "0,0600%"),
    ("Ancient Hero Boots [1]", 850_000, "0,3500%"),
    ("Reinforced Narcis Bow Cube", 4_000_000, "0,3500%"),
    ("Reinforced Exorcist's Bible Cube", 2_500_000, "0,3500%"),
    ("Reinforced Meteor Striker Cube", 2_000_000, "0,3500%"),
    ("Reinforced Light Blade Cube", 2_000_000, "0,3500%"),
    ("Consultation Cape", 4_400_000, "0,4000%"),
    ("Agenda Cape", 10_000_000, "0,4000%"),
    ("Hat Collection", 11_000_000, "1,0000%"),
    ("Sprout of World Tree Egg", 10_000_000, "1,0000%"),
    ("Powerful Headgear Box", 0, "1,0000%"),
    ("Common Ancestral Box", 4_950_000, "1,0000%"),
    ("Uncommon Ancestral Box", 5_000_000, "1,0000%"),
    ("Expanded Ancestral Box", 1_400_000, "1,0000%"),
    ("Clever Combiner", 2_000_000, "1,5000%"),
    ("Durable Combiner", 2_000_000, "1,5000%"),
    ("Shadow Enchanter", 15_000_000, "2,0000%"),
    ("Shadow Synthesis Box", 800_000, "2,0000%"),
    ("Greed Shadow Box", 2_000_000, "2,0000%"),
    ("Rigid Combiner", 0, "2,0000%"),
    ("Athena Combiner", 0, "2,0000%"),
    ("Physical and Magical Combiner", 0, "2,0000%"),
    ("Shadow Material Cube 3", 15_000_000, "2,5000%"),
    ("Blacksmith Blessing", 3_000_000, "3,0000%"),
    ("Cx. Cat Paw Card (1 day)", 0, "3,0000%"),
    ("Stats Soul Potion Box", 300_000, "3,0000%"),
    ("Pump of Spirit", 400_000, "3,0000%"),
    ("Dark Refining Hammer", 1_700_000, "3,0000%"),
    ("[Event] Manual & Gum", 0, "4,7500%"),
    ("[Event] Small Mana Potion", 0, "4,7500%"),
    ("[Scroll] Small Life Potion", 0, "4,7500%"),
    ("New Insurance", 0, "4,7500%"),
    ("[Limited] Token of Siegfried", 0, "4,7500%"),
    ("Passport", 0, "7,0000%"),
    ("[Event] Blessing Of Tyr", 0, "7,0000%"),
    ("Golden Potion", 0, "7,0000%"),
    ("[Event] Regenerate Potion", 0, "7,0000%"),
    ("[Scroll] Mental Potion", 0, "7,0000%")
]

items = [Item(name, price, prob) for name, price, prob in item_data]

buebito = Huevito(items)
results = buebito.simulate(n_boxes, n_trials, buebito_price, rng)

buebito.print_statistics(results)

threshold_high = 600_000_000 #Limite superior para agrupar

negative = results[results < 0] #Para ver probabilidad de no ganar
middle = results[(results >= 0) & (results <= threshold_high)]
high = results[results > threshold_high]

bin_edges = [results.min(), 0]  # Bin para negativos
bin_edges.extend(np.linspace(0, threshold_high, 11)[1:])  # 10 bins entre 0-600M
bin_edges.append(results.max() + 1)  # Bin para >600M

binned_results = np.digitize(results, bin_edges) - 1
counts = np.bincount(binned_results, minlength=len(bin_edges)-1)

labels = [f"<0M"]
for i in range(1, len(bin_edges)-2):
    labels.append(f"{bin_edges[i]/1e6:.0f}-{bin_edges[i+1]/1e6:.0f}M")
labels.append(f">{threshold_high/1e6:.0f}M")

# Graficar
plt.figure(figsize=(14,6))
bars = plt.bar(range(len(counts)), counts, edgecolor='black')

bars[0].set_color('crimson')  # Pérdidas en rojo
bars[0].set_alpha(0.7)
bars[-1].set_color('gold')  # >threshold_high en dorado
bars[-1].set_edgecolor('darkorange')
bars[-1].set_linewidth(2)

total = len(results)
for i, (bar, count) in enumerate(zip(bars, counts)):
    height = bar.get_height()
    percentage = (count / total) * 100
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{percentage:.1f}%',
             ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.xticks(range(len(labels)), labels, rotation=45, ha='right')
plt.axvline(0.5, color='red', linestyle='--', linewidth=2, label='Punto de equilibrio (0)')
plt.title("Distribución del beneficio neto (100 cajas x 1000 repeticiones)")
plt.xlabel("Rango de beneficio neto (zeny)")
plt.ylabel("Frecuencia")
plt.legend()
plt.tight_layout()
plt.show()