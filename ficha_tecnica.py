# -*- coding: utf-8 -*-
"""Datos de I+D del usuario, sin validación experimental, para panel BOM."""
from collections import OrderedDict

def entry(name, function, power='—', size='Por definir', maturity='Conceptual', risk='Integración por validar'):
    return dict(name=name,function=function,power=power,size=size,maturity=maturity,risk=risk)

TECH_DATA = {
    'brand': 'LATAMinds', 'product': 'MigraRing Bio', 'version': '3.0',
    'dimensions_mm': {'outer_diameter':22.0,'inner_diameter':19.0,'width':8.5,'radial_budget':1.5},
    'energy': {'voltage_V':3.7,'capacity_mAh_min':20,'capacity_mAh_max':25,
               'base_mW':[2,5],'advanced_mW':[4,8],'research_mW':[6,12],
               'operating_goal_hours':24,'desired_hours':[24,48]},
    'components': OrderedDict([
        ('shell',entry('Carcasa Ti grado 5','Protección y diseño del anillo; titanio grado 5 mecanizado.',size='Ø22 × 8,5 mm exterior',risk='Resistencia y tolerancias no verificadas.')),
        ('accent',entry('Aro estético azul','Ranura perimetral de identidad del producto.',size='Canal anular ilustrativo',risk='La emisión luminosa continua aumentaría consumo y complicaría sellado.')),
        ('fasteners',entry('Detalles y registros','Topes, referencias visuales y guías internas.',size='Submilimétricos (CAD conceptual)',risk='No son uniones mecánicas calculadas.')),
        ('branding',entry('Marca LATAMinds','Identidad del equipo en el visor y micrograbado lateral del anillo.',size='Texto tangente submilimétrico',risk='Marcado visual de presentación, pendiente decisión de fabricación.')),
        ('liner',entry('PEEK médico','Revestimiento de contacto y aislamiento eléctrico.',size='Ø19 mm interior nominal',risk='Validar biocompatibilidad, adhesivos y fabricación.')),
        ('seal',entry('Sistema de sellado','Juntas elastoméricas y elementos encapsulados contra humedad.',size='Dimensiones preliminares',risk='IP68 es objetivo, NO certificado ni ensayado.')),
        ('rfwindow',entry('Ventana RF aislante','Zona dieléctrica para permitir que funcione la antena BLE con carcasa metálica.',size='~3 × 1,5 mm ilustrativo',risk='Pendiente simulación de RF y ensayo de alcance.')),
        ('pcb',entry('PCB flexible poliimida','Conecta sensores, control, potencia, antena y memorias.',size='Anillo curvo / desarrollo ~57 mm conceptual',risk='No hay netlist, reglas DFM ni stack-up validado.')),
        ('copper',entry('Cobre: pistas y pads','Metalización, pads y vías de la PCB flexible.',size='~0,075–0,1 mm pistas ilustrativas',risk='El trazado no representa circuitos eléctricamente comprobados.')),
        ('passives',entry('Pasivos SMD','Desacoplo, filtrado, acondicionamiento analógico y protección.',size='0201/0402 conceptual',risk='No hay esquema, códigos comerciales ni PCB validada.')),
        ('battery',entry('Batería curva recargable','Almacena energía de una celda nominal 3,7 V.',size='20–25 mAh; referencia visual 14 × 6 × 2 mm',risk='Espesor de 2 mm NO entra en pared radial de 1,5 mm: volumen CAD es ilustrativo. Capacidad no demostrada.')),
        ('charge',entry('Carga y protección','Interfaz de recarga y protección contra sobrecarga, descarga y calor.',size='Contactos de base propuestos',risk='Elegir inductiva o contactos y certificar estanqueidad. Objetivo carga 60–90 min sin validar.')),
        ('mcu',entry('MCU ultra bajo consumo + BLE','Adquisición, sincronización Bluetooth Low Energy y lógica local.',power='MCU 0,2–2 mW; BLE 0,1–3 mW',size='Referencia visual 8 × 8 × 1,0 mm (conflicto de integración)',risk='Componente real no seleccionado; tamaño y RF se deben justificar.')),
        ('pmic',entry('PMIC / energía','Gestiona tensión, estado de batería y carga.',power='Pérdidas bajas, por cuantificar',size='Por definir',risk='No hay topología ni presupuesto de pérdidas medido.')),
        ('flash',entry('Memoria local','Registra datos antes del envío BLE por lotes.',power='<0,1 mW promedio (estimación)',size='Por definir',risk='Memoria real, capacidad de datos y retención por seleccionar.')),
        ('antenna',entry('Antena BLE integrada','Comunicación a 2,4 GHz mediante región dieléctrica.',power='Incluida en consumo BLE',size='Meandro flex (ilustrativo)',risk='Antena junto a titanio y piel: imprescindible simulación.')),
        ('ppg',entry('PPG multiespectral','Pulso, señales vasculares periféricas y proxies de variabilidad; LEDs verde, rojo e IR.',power='1–5 mW medio; picos 10–20 mW',size='Referencia 5 × 4 × 1,2 mm',risk='HRV derivada de pulsos no es ECG/HRV directa. Validar calidad óptica y movimiento.')),
        ('lightbaffle',entry('Separadores ópticos','Evitan acoplamiento directo entre LEDs y fotodetector.',size='Microbarreras alrededor del PPG',risk='Diseño óptico pendiente de simulación y prototipo.')),
        ('temp',entry('Temperatura cutánea','Seguimiento térmico de piel y variación circadiana.',power='0,01–0,1 mW',size='Referencia 1,5 × 1,5 × 0,6 mm',risk='No mide directamente la temperatura corporal central.')),
        ('mems',entry('Acelerómetro MEMS 3 ejes','Movimiento, actividad, descanso y descarte de artefactos.',power='0,02–0,2 mW',size='Referencia 2 × 2 × 0,95 mm',risk='Frecuencia de muestreo y consumo efectivo pendientes.')),
        ('eda',entry('Electrodos EDA / bioimpedancia','Respuesta electrodermal y características del contacto.',power='EDA 0,05–0,5 mW; bioimpedancia 0,1–1 mW',size='Dos contactos de piel propuestos',risk='Contacto/sudor/humedad introducen variabilidad considerable.')),
        ('pressure',entry('Presión flexible / grafeno I+D','Estima ajuste del anillo y posibles artefactos por presión.',power='0,01–0,2 mW',size='Referencia 5 × 2 × 0,2 mm',risk='Elemento piezorresistivo de grafeno hipotético; falta validación.')),
        ('fluid',entry('Microfluídica de sudor (I+D)','Capilares pasivos para muestras de sudor en el dedo.',power='~0 mW si pasiva',size='Referencia cartucho 10 × 3 × 1 mm',maturity='Experimental',risk='La cantidad de sudor, evaporación y microcanales no se han demostrado.')),
        ('biosensor',entry('Biosensor químico (I+D)','Detección electroquímica potencial de lactato, sodio y potasio.',power='0,2–2 mW',size='Por definir',maturity='Experimental',risk='Sensibilidad, selectividad, mantenimiento y valor predictivo sin validar.')),
        ('cgrp',entry('CGRP (hipótesis futura)','Investigación de detección no invasiva de CGRP relacionada con migraña.',power='0,5–5 mW, hipotético',size='Por definir; NO módulo comercial',maturity='Hipótesis I+D',risk='No existe solución validada integrada en este anillo. No afirmar que mide CGRP.')),
    ]),
    'notes': [
        'No hay predicción clínica ni algoritmo calibrado dentro del visor: solo modelo 3D y documentación.',
        'Los valores de consumo proceden de estimaciones conceptuales proporcionadas para presentación técnica.',
        'La batería de referencia de 2 mm es mayor que el espacio radial nominal de 1,5 mm.',
        'El modelo CAD está pensado para comunicación y diseño I+D, no para fabricación ni ensayos regulatorios.',
        'La carcasa IP68 y la autonomía 24–48h son objetivos a demostrar.'
    ]
}
