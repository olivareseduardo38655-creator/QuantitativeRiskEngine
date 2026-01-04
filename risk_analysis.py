import pandas as pd
import matplotlib.pyplot as plt

# 1. CARGA DE DATOS
print("🐍 Python: Leyendo datos generados por Java...")
try:
    # Leemos el CSV generado por el motor Java
    df = pd.read_csv('simulacion_riesgo.csv')
    print(f"✅ Datos cargados correctamente: {len(df)} simulaciones.")
except FileNotFoundError:
    print("❌ Error: No se encuentra 'simulacion_riesgo.csv'. Asegúrate de ejecutar primero el motor Java.")
    exit()

# 2. CÁLCULO DE MÉTICAS (AUDITORÍA)
# Vamos a recalcular el VaR aquí para ver si coincide con Java
# VaR 95% = El valor en el percentil 5
var_95 = df['final_price'].quantile(0.05)
mean_price = df['final_price'].mean()

print(f"📊 Precio Promedio: ${mean_price:,.2f}")
print(f"⚠️ VaR (95%) calculado en Python: ${var_95:,.2f}")

# 3. VISUALIZACIÓN PROFESIONAL
plt.figure(figsize=(12, 6))

# Histograma de frecuencia (Distribución de precios futuros)
plt.hist(df['final_price'], bins=100, color='#2c3e50', alpha=0.7, edgecolor='black', label='Distribución de Escenarios')

# Línea vertical del VaR (El límite del riesgo)
plt.axvline(var_95, color='red', linestyle='dashed', linewidth=2, label=f'VaR 95%: ${var_95:.2f}')

# Línea vertical del Precio Promedio
plt.axvline(mean_price, color='green', linestyle='dashed', linewidth=2, label=f'Media: ${mean_price:.2f}')

# Decoración del gráfico
plt.title('Simulación de Montecarlo: Distribución de Precios Futuros (1M Escenarios)', fontsize=14)
plt.xlabel('Precio Final del Activo ($)', fontsize=12)
plt.ylabel('Frecuencia (Cantidad de Escenarios)', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)

# Mostrar gráfico
print("📈 Generando gráfico...")
plt.show()
