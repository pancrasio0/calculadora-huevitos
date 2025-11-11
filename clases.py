import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
class Item:
    def __init__(self, name, price, prob_string):
        self.name = name
        self.price = price
        self.prob_string = prob_string
        self.probability = self._parse_prob(prob_string)
    
    @staticmethod
    def _parse_prob(s):
        s = s.strip().replace("%", "").replace(",", ".")
        return float(s) / 100
    
    def __repr__(self):
        return f"Item('{self.name}', {self.price:,}, {self.prob_string})"

class Huevito:
    def __init__(self, items):
        self.items = items
        self.prices = np.array([item.price for item in items])
        self.probs = np.array([item.probability for item in items])
        self._normalize_probs()
    
    def _normalize_probs(self):
        """Normaliza las probabilidades para que sumen 1"""
        self.probs /= self.probs.sum()
    
    def get_item_names(self):
        return [item.name for item in self.items]
    
    def simulate(self, n_buebitos, n_trials, buebito_price, seed): #Cambiar semilla si se quiere cambiar el rng
        """Ejecuta simulación Monte Carlo"""
        rng = np.random.default_rng(seed=seed)
        results = []
        
        for i in range(n_trials):
            draws = rng.choice(len(self.items), size=n_buebitos, p=self.probs)
            value = sum(self.prices[j] for j in draws)
            cost = n_buebitos * buebito_price
            net = value - cost
            results.append(net)
        
        return np.array(results)
    
    def print_statistics(self, results):
        mean_net = results.mean()
        median_net = np.median(results)
        std_net = results.std()
        prob_positive = np.mean(results > 0) * 100
        
        print(f"=== RESULTADOS ===")
        print(f"Media neta: {mean_net:,.0f}")
        print(f"Mediana neta: {median_net:,.0f}")
        print(f"Desvío estándar: {std_net:,.0f}")
        print(f"% de repeticiones con beneficio: {prob_positive:.2f}%")