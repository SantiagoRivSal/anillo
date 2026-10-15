# LATAMinds · MigraRing Bio — CAD Studio V3

**Prototipo conceptual de diseño industrial e I+D**, basado en la maqueta de MigraRing Bio y la ficha técnica del proyecto. Los cuerpos 3D son sólidos CAD con volumen, pero no se trata de un producto validado para producción ni de una PCB electrónica funcional.

## Abrir el modelo

1. Abrí `LATAMinds_MigraRing_Studio_v3.html` en Chrome, Edge o Firefox con WebGL2 habilitado. No necesita internet.
2. Rotá con el mouse, zoom con la rueda y hacé clic en una pieza para inspeccionarla.
3. Explorá `Producto`, `Despiece CAD`, `Electrónica` y `Sección`, más `Rayos X`, `Sensores de I+D` y `Etiquetas`.
4. En el inspector elegí `Pieza`, `BOM` o `Energía`. El último permite modificar capacidad, consumo y energía utilizable para estimar horas teóricas.
5. Usá el ícono de cámara para guardar una vista PNG.

La sección es un **recorte visual por shader de los triángulos**, no genera planos de cierre de sección. Para secciones exactas usá los archivos STEP en un CAD.

## Programar y editar (Python)

Necesitás Python 3.11/3.12 de 64 bits recomendado. En una carpeta con los archivos:

```bash
python -m pip install cadquery numpy trimesh Pillow
python migraring_lataminds_studio.py --abrir
```

El programa genera en `GENERADOS/` el visor HTML, los STEP, GLB, el CSV BOM y los datos JSON. El proyecto utiliza el kernel geométrico OpenCascade a través de CadQuery, no aproximaciones geométricas exclusivamente dibujadas a mano. Las dimensiones están escritas en la fuente como **modelo paramétrico conceptual**, no hay optimizador automático de encaje.

## Archivos

- `LATAMinds_MigraRing_Studio_v3.html`: interfaz offline con logo y menú de componentes.
- `LATAMinds_MigraRing_ensamblaje.step`: conjunto de sólidos CAD (milímetros).
- `LATAMinds_MigraRing_electronica.step`: placa desplegada (milímetros).
- `LATAMinds_MigraRing_ensamblaje.glb`, `LATAMinds_MigraRing_electronica.glb`: mallas para Blender (metros, tamaño Ø 0,022 m).
- `migraring_lataminds_studio.py`: generador de escenas y formatos.
- `ficha_tecnica.py`, `BOM_LATAMinds_MigraRing.csv`, `Parametros_de_ingenieria.json`: inventario editable, consumo y riesgos.
- `visor_template.html`: código de interfaz WebGL2 autocontenido.
- `LATAMinds_logo_transparente.png`, `lataminds_original.png`: identidad gráfica proporcionada por el equipo, incluida en el visor.

## Ingeniería conceptual y objetivos

- **Medidas de referencia:** Ø22 mm exterior, Ø19 mm interior, ancho axial 8,5 mm.
- **Estructura:** carcasa titanio grado 5; revestimiento PEEK médico; PCB poliimida flex; juntas; ventanas ópticas; antena con región dieléctrica.
- **Sensores base:** PPG multiespectral verde/rojo/IR, sensor térmico cutáneo, acelerómetro MEMS 3 ejes, EDA/bioimpedancia, película de presión.
- **Sensores de I+D:** microfluídica de sudor, biosensor lactato/Na/K, CGRP hipotético sin validación.
- **Control:** SoC MCU/BLE, memoria, PMIC, pasivos SMD, carga por base/contactos en exploración.
- **Autonomía estimada desde datos proporcionados:** celda objetivo 20–25 mAh nominal 3,7 V; modo base 2–5 mW; avanzado 4–8 mW; investigación 6–12 mW.
- **Objetivo de producto:** >=24 h, deseable 24–48 h con adquisición por ventanas, condicionado a rediseño y ensayos.

### Limitación geométrica crítica

`(22 − 19) / 2 = 1,5 mm` de pared radial nominal para TODO el paquete. Una batería de la referencia de 2 mm de grosor **NO cabe**. La celda presente en el CAD es un volumen ilustrativo más pequeño, que NO implica tener una capacidad energética real de 20–25 mAh. También deben comprobarse los tamaños visuales de chips y cartuchos (por ejemplo referencia MCU 8 × 8 × 1 mm).

**No** están validados: compatibilidad entre piezas, grosor efectivo del stack-up, patrón real de PCB, diseño de RF, biocompatibilidad, vida de batería, protección térmica, IP68, capacidad de leer CGRP, ni precisión de predicción de migrañas. La función médica del anillo es un objetivo futuro de investigación, no una prestación implementada aquí.

## Siguientes pasos para un prototipo físico

1. Elegir chips, fotodiodos, LEDs, MEMS y batería con número de parte y CAD de fabricante.
2. Hacer un cálculo de volumen y análisis de interferencias; revisar envolvente y tolerancias.
3. Diseñar esquemático + PCB flex y antena 2,4 GHz; analizar RF y óptica PPG.
4. Decidir estrategia de carga, sellado IP68 y biocompatibilidad y comprobar mediante ensayos.
5. Probar adquisición de datos, construir dataset longitudinal y validar de forma prospectiva cualquier modelo predictivo.

LATAMinds © Concepto de I+D · MigraRing Bio · v3.
