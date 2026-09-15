import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import logging
import tkinter as tk
from tkinter import messagebox

logging.basicConfig(level=logging.INFO, format='%(message)s')

def ejecutar_simulacion():
    try:
        # 1. CAPTURAR DATOS DE LA INTERFAZ (Finanzas Duras)
        CAPEX = float(e_capex.get())
        C_TRAB = float(e_ctrab.get())
        OPEX = float(e_opex.get())
        DESECHO_PCT = float(e_desec.get())
        TASA = float(e_tasa.get())
        IMPUESTO = float(e_impto.get())
        ANOS = int(e_anos.get())
        
        # 2. CAPTURAR DATOS DE LA INTERFAZ (Mercado)
        P_MIN, P_PROB, P_MAX = float(ep_min.get()), float(ep_prob.get()), float(ep_max.get())
        C_MIN, C_PROB, C_MAX = float(ec_min.get()), float(ec_prob.get()), float(ec_max.get())
        D_MIN, D_PROB, D_MAX = float(ed_min.get()), float(ed_prob.get()), float(ed_max.get())
        
        ITERACIONES = 10000
        
        # Si todo se leyó bien, cerramos la ventana
        ventana.destroy() 
        
        # ========================================================
        # 3. MOTOR MONTE CARLO (TRIANGULAR + ESCUDO FISCAL + TIEMPO)
        # ========================================================
        logging.info("🚀 Simulando 10.000 realidades alternativas (Modo Investment Grade)...")
        
        # Flujo Año 0: Desembolso del CAPEX y el Capital de Trabajo
        van_simulado = np.full(ITERACIONES, -(CAPEX + C_TRAB), dtype=float)
        
        # Depreciación lineal (simplificada a cero al final del proyecto)
        depreciacion_anual = CAPEX / ANOS
        
        # Simulamos año a año (Permite que el año 1 sea malo y el 2 sea bueno, rompe la linealidad)
        for ano in range(1, ANOS + 1):
            # Usamos Distribución Triangular: Fuerza los resultados hacia tu escenario "Probable"
            precios = np.random.triangular(P_MIN, P_PROB, P_MAX, ITERACIONES)
            costos = np.random.triangular(C_MIN, C_PROB, C_MAX, ITERACIONES)
            demandas = np.random.triangular(D_MIN, D_PROB, D_MAX, ITERACIONES)
            
            ingresos = precios * demandas
            costos_var = costos * demandas
            
            # Estado de Resultados
            ebitda = ingresos - costos_var - OPEX
            ebit = ebitda - depreciacion_anual # Aquí aplicamos el Escudo Fiscal
            
            # Impuestos (Solo se pagan si hay utilidades operativas)
            impuestos = np.where(ebit > 0, ebit * IMPUESTO, 0)
            
            # Flujo de Caja Libre (Operativo)
            flujo_caja_libre = ebitda - impuestos
            
            # Flujos Terminales (Solo ocurren el último año)
            if ano == ANOS:
                ingreso_desecho = CAPEX * DESECHO_PCT
                impuesto_desecho = ingreso_desecho * IMPUESTO
                flujo_terminal = (ingreso_desecho - impuesto_desecho) + C_TRAB
                flujo_caja_libre += flujo_terminal
                
            # Traer al Valor Presente
            van_simulado += flujo_caja_libre / ((1 + TASA) ** ano)
            
        # ========================================================
        # 4. MÉTRICAS Y EXPORTACIÓN GERENCIAL
        # ========================================================
        prob_exito = (van_simulado > 0).mean() * 100
        van_promedio = van_simulado.mean()
        
        logging.info("💾 Exportando reporte Excel y Gráfico de Riesgo (B2B)...")
        
        df_resultados = pd.DataFrame({
            "Métrica Financiera Corporativa": [
                "VAN Promedio Esperado (Después de Impuestos)", 
                "Peor Escenario Posible", 
                "Mejor Escenario Posible", 
                "Probabilidad de Éxito Comercial (%)", 
                "Riesgo de Destrucción de Valor (%)"
            ],
            "Valor": [
                round(van_promedio, 0), 
                round(van_simulado.min(), 0), 
                round(van_simulado.max(), 0), 
                round(prob_exito, 2), 
                round(100 - prob_exito, 2)
            ]
        })
        df_resultados.to_excel("Reporte_MonteCarlo_PRO.xlsx", index=False)
        
        # GRÁFICO
        plt.figure(figsize=(10, 6))
        plt.hist(van_simulado, bins=50, color='#00a2ff', edgecolor='black', alpha=0.7)
        plt.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Línea Cero (VAN $0)')
        plt.axvline(x=van_promedio, color='green', linestyle='-', linewidth=2, label=f'VAN Promedio (${van_promedio:,.0f})')
        plt.title('Radiografía de Riesgo: Distribución de VAN (Con Escudo Fiscal y Capital de Trabajo)', fontweight='bold')
        plt.xlabel('Valor Actual Neto (VAN) en $')
        plt.ylabel('Frecuencia (Universos Simulados)')
        plt.legend()
        plt.grid(axis='y', alpha=0.5)
        plt.ticklabel_format(style='plain', axis='x')
        plt.savefig("Radiografia_Riesgo_PRO.png", dpi=300, bbox_inches='tight')
        logging.info("✅ PROCESO TERMINADO. Gráfico y Excel generados en tu carpeta.")
        plt.show()
        
    except ValueError:
        messagebox.showerror("Error de Formato", "Por favor, ingresa solo números (usa puntos para decimales, sin signos $).")

# ========================================================
# 5. INTERFAZ GRÁFICA AVANZADA (Layout de 2 Columnas - En Blanco)
# ========================================================
ventana = tk.Tk()
ventana.title("Simulador Financiero Monte Carlo (Grado de Inversión)")
ventana.geometry("520x560")
ventana.configure(padx=15, pady=15)

def crear_campo(padre, texto, fila, col):
    tk.Label(padre, text=texto).grid(row=fila, column=col, sticky="w", padx=5, pady=5)
    e = tk.Entry(padre, width=12)
    e.grid(row=fila, column=col+1, padx=5, pady=5)
    return e

# --- MARCO 1: ESTRUCTURA FINANCIERA ---
marco_base = tk.LabelFrame(ventana, text=" 1. Estructura Financiera y Tributaria ", font=("Arial", 10, "bold"), padx=10, pady=10)
marco_base.pack(fill="both", expand=True, pady=5)

e_capex = crear_campo(marco_base, "CAPEX (Inv. Inicial):", 0, 0)
e_ctrab = crear_campo(marco_base, "Capital de Trabajo:", 0, 2)
e_opex  = crear_campo(marco_base, "OPEX (Fijos Anuales):", 1, 0)
e_desec = crear_campo(marco_base, "Valor Desecho (%):", 1, 2)
e_tasa  = crear_campo(marco_base, "Tasa Descuento:", 2, 0)
e_impto = crear_campo(marco_base, "Tasa Impuesto (SII):", 2, 2)
e_anos  = crear_campo(marco_base, "Años de Proyecto:", 3, 0)

# --- MARCO 2: COMPORTAMIENTO DE MERCADO ---
marco_merc = tk.LabelFrame(ventana, text=" 2. Comportamiento de Mercado (Triangular) ", font=("Arial", 10, "bold"), padx=10, pady=10)
marco_merc.pack(fill="both", expand=True, pady=10)

tk.Label(marco_merc, text="Mínimo", font=("Arial", 9, "italic")).grid(row=0, column=1)
tk.Label(marco_merc, text="Probable", font=("Arial", 9, "italic")).grid(row=0, column=2)
tk.Label(marco_merc, text="Máximo", font=("Arial", 9, "italic")).grid(row=0, column=3)

def fila_mercado(texto, fila):
    tk.Label(marco_merc, text=texto, font=("Arial", 9, "bold")).grid(row=fila, column=0, sticky="w", pady=5)
    e1 = tk.Entry(marco_merc, width=10); e1.grid(row=fila, column=1, padx=3)
    e2 = tk.Entry(marco_merc, width=10); e2.grid(row=fila, column=2, padx=3)
    e3 = tk.Entry(marco_merc, width=10); e3.grid(row=fila, column=3, padx=3)
    return e1, e2, e3

ep_min, ep_prob, ep_max = fila_mercado("Precio ($):", 1)
ec_min, ec_prob, ec_max = fila_mercado("Costo Var ($):", 2)
ed_min, ed_prob, ed_max = fila_mercado("Demanda (Q):", 3)

tk.Button(ventana, text="🔥 Ejecutar Motor V5 (Grado de Inversión)", bg="#0047AB", fg="white", font=("Arial", 11, "bold"), command=ejecutar_simulacion).pack(pady=10)

ventana.mainloop()