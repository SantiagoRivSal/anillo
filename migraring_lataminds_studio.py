#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LATAMinds · MigraRing Bio — Studio V3 · CAD paramétrico y visor de ingeniería.

Unidades de construcción: milímetros. Carcasa Ø22 exterior, Ø19 interior, ancho 8.5.
Estas piezas NO constituyen un diseño liberado para fabricación, ni garantizan
espacio libre, compatibilidad de batería, sellado IP68 o eficacia clínica.

Dependencias: cadquery>=2.4, numpy>=1.24, trimesh>=4.0.
Ejecutar: python migraring_cad_pro.py
"""
import cadquery as cq
import numpy as np
import trimesh
import math, json, base64, struct, gzip, io, argparse, os, webbrowser, zipfile, csv
from pathlib import Path
from dataclasses import dataclass
from ficha_tecnica import TECH_DATA

BASE = Path(__file__).resolve().parent
VERSION = '3.0'
BRAND = 'LATAMinds'
M = {}
PARTS = []
TAU = math.tau

MAT = {
 'titanium': ('Titanio grado 5 (propuesto)', '#b3bfcb', .84,.26,1.),
 'titanium_dark': ('Titanio satinado', '#586675', .78,.32,1.),
 'silver': ('Acero satinado', '#dbe6ec', .72,.24,1.),
 'blue': ('Canal óptico azul', '#39a5ff', .30,.18,.88),
 'peek': ('PEEK médico (propuesto)', '#1b2635', .11,.47,1.),
 'seal': ('Junta elastomérica', '#14212b', .03,.65,1.),
 'optical': ('Cristal óptico', '#182b37', .22,.11,.87),
 'glass': ('Recubrimiento cerámico', '#33475b', .17,.18,.98),
 'copper': ('Cobre', '#d69a47', .78,.30,1.),
 'gold': ('Oro, electrodos', '#ffd083', .82,.21,1.),
 'flex': ('Poliimida flexible', '#99541e', .10,.56,1.),
 'mask': ('Máscara electrónica', '#1f3640', .12,.49,1.),
 'chip': ('Encapsulado electrónico', '#101c29', .12,.42,1.),
 'chip_top': ('Encapsulado secundario', '#24364a', .17,.39,1.),
 'battery': ('Batería ilustrativa', '#bbc4cf', .58,.34,1.),
 'battery_label': ('Aislante batería', '#738698', .21,.59,1.),
 'sensor_blue': ('PPG LED azul', '#45a9ff', .16,.15,1.),
 'sensor_green': ('PPG LED verde', '#38e89e', .13,.15,1.),
 'sensor_red': ('PPG LED rojo', '#ff736c', .13,.15,1.),
 'temp': ('Indicador térmico', '#4ce8ba', .15,.20,1.),
 'orange': ('Acelerómetro', '#ffac63', .15,.27,1.),
 'pressure': ('Presión flexible', '#ff6b80', .18,.36,.95),
 'fluid': ('Microfluídica (I+D)', '#30cadb', .14,.20,.78),
 'experimental': ('Biosensor (I+D)', '#a18dff', .22,.28,1.),
 'cgrp': ('CGRP (I+D hipotético)', '#ff76cf', .2,.3,1.),
 'ceramic':('Cerámica óptica protectora', '#d8e9ee', .24,.14,1.),
 'blackmetal':('PVD antracita', '#273444', .73,.29,1.),
 'bond':('Adhesivo encapsulado', '#426177', .11,.45,.85),
 'silicon':('Silicio expuesto', '#202d39', .30,.19,1.),
 'microled':('Emisor IR', '#a17eff', .18,.16,1.),
 'teal':('Marca de servicio', '#49e8d4', .15,.22,1.),
}

META = {
 'shell':('Carcasa exterior de titanio','MECÁNICA','Carcasa con banda continua y coronas mecanizadas, con superficies suavizadas y canal ornamental.','Grado 5 y espesores ilustrativos; se deben calcular resistencia, unión y tolerancias.','Certeza: envolvente dimensional'),
 'accent':('Ranura perimetral luminosa','DISEÑO','Canal azul de señalización representado en la referencia original.','Un indicador óptico continuo consume energía, precisa difusión y sellado; implementación por definir.','Conceptual'),
 'seal':('Junta de estanqueidad','MECÁNICA','Representación de línea de sellado entre revestimiento y carcasa.','La clasificación IP68 depende de ensayos del conjunto final; aquí no está certificada.','Conceptual'),
 'liner':('Revestimiento interior de PEEK','MECÁNICA','Superficie interior aislante adaptada a la circunferencia del dedo con ventanas para mediciones.','PEEK y adhesivos requieren validación de biocompatibilidad y envejecimiento.','Conceptual'),
 'rfwindow':('Ventana dieléctrica RF','RADIO','Interrupción local de la pantalla de titanio para mejorar el acoplamiento de antena.','Sin simulación electromagnética ni certificación BLE.','Por evaluar'),
 'pcb':('PCB flexible de poliimida','CIRCUITO','Sustrato curvado de interconexión con pistas de cobre y contactos distribuidos.','Ruteo conceptual; falta diseño electrónico real, stack-up y reglas de fabricación.','Conceptual'),
 'copper':('Pistas y pads de cobre','CIRCUITO','Metalización y zonas de soldadura de la PCB flexible.','Trazado artístico, no corresponde a un netlist ni garantiza integridad de señal.','Ilustrativo'),
 'battery':('Celda curva recargable','ENERGÍA','Volumen reservado para un módulo de batería adaptado al perímetro.','La maqueta menciona una batería de 2 mm de espesor: NO cabe en los 1,5 mm radiales totales. La pieza CAD solo simula un volumen reducido.','Conflicto dimensional'),
 'mcu':('SoC BLE + microcontrolador','ELECTRÓNICA','Chip que integraría comunicación inalámbrica y adquisición de datos.','No es un encapsulado comercial seleccionado; verificar tamaño, energía y disipación.','Componente propuesto'),
 'pmic':('Gestión de alimentación','ELECTRÓNICA','Electrónica de regulación de tensión, protección y gestión de energía.','Falta elegir circuito y estrategia física de recarga.','Componente propuesto'),
 'flash':('Memoria Flash de bajo consumo','ELECTRÓNICA','Almacena las muestras para sincronización BLE por lotes.','Chip ilustrativo: no se ha seleccionado un PN ni se ha estimado el presupuesto de almacenamiento.','Componente propuesto'),
 'passives':('Pasivos SMD y filtros','CIRCUITO','Condensadores de desacoplo, resistores, filtros y pads de test representados en la placa.','El placement es conceptual y NO procede de un esquema eléctrico ni netlist.','Ilustrativo'),
 'charge':('Carga y protección','ENERGÍA','Contactos e interfaz de protección; opción de base de carga todavía por decidir.','La solución de carga y sellado del producto requiere ingeniería y ensayos.','Conceptual'),
 'lightbaffle':('Separador óptico PPG','SENSOR BASE','Barrera oscura entre emisores y fotodiodo para reducir el acoplamiento directo de luz.','Se necesita validación óptica y ensayos contra movimiento y luz ambiental.','Conceptual'),
 'fasteners':('Detalles de ensamblaje','MECÁNICA','Marcas de registro, topes, pequeños apoyos y recursos de montaje.','No son tornillos estructurales seleccionados ni tolerancias aprobadas.','Ilustrativo'),
 'branding':('Marcado LATAMinds','DISEÑO','Marcado físico microscópico LATAMinds sobre la carcasa curva, junto al logo completo de la plataforma.','La tinta/grabado real depende del proceso industrial; relieve 3D ilustrativo.','Conceptual'),
 'antenna':('Antena BLE','RADIO','Conductor serpenteante asociado a la ventana dieléctrica.','La carcasa metálica y el tejido humano degradan RF; imprescindible estudio de antena a 2,4 GHz.','Requiere simulación'),
 'ppg':('PPG multiespectral','SENSOR BASE','Conjunto de LEDs y fotodetector alineado con una ventana hacia la piel.','Debe verificarse calidad de señal, luz parásita, movimiento y compatibilidad mecánica.','Sensor propuesto'),
 'temp':('Temperatura cutánea','SENSOR BASE','Punto de lectura térmica en contacto próximo a la piel.','Mide temperatura de piel, no directamente temperatura corporal central.','Sensor propuesto'),
 'mems':('Acelerómetro MEMS de 3 ejes','SENSOR BASE','Circuito de detección de movimiento para ayudar a interpretar señales fisiológicas.','Debe seleccionarse sensor y configurar frecuencia de muestreo/consumo.','Sensor propuesto'),
 'eda':('Electrodos EDA / bioimpedancia','SENSOR BASE','Dos contactos conductores separados en la cara interior.','Señal muy sensible al contacto, humedad, polarización y posición.','Sensor propuesto'),
 'pressure':('Película de presión','SENSOR BASE','Sensor flexible de contacto interno para estimar ajuste y presión.','Propuesta experimental, sin solución de grafeno validada aquí.','A verificar'),
 'fluid':('Microfluídica de sudor','EXPERIMENTAL','Pequeño volumen y canales para recoger una muestra por contacto.','Rendimiento de sudor en el dedo, evaporación y bioensuciamiento no validados.','Investigación'),
 'biosensor':('Biosensor electroquímico','EXPERIMENTAL','Matriz de electrodos para una posible medición de analitos.','Los analitos detectables y su utilidad para predecir migraña están por investigar.','Investigación'),
 'cgrp':('Módulo CGRP conceptual','I+D','Volumen opcional de investigación para un biomarcador vinculado a migraña.','No es una tecnología no invasiva de medición de CGRP validada ni lista para un anillo.','Hipotético'),
}

@dataclass
class Part:
    name:str
    shape:object
    family:str
    material:str
    exploded:float=0
    view:str='ring'
    note:str=''


def add(name, shape, family, material, exploded=0, view='ring'):
    PARTS.append(Part(name,shape,family,material,exploded,view))
    return shape


def tube(ri,ro,z0,z1,fillet=0):
    obj=cq.Workplane('XY').circle(ro).circle(ri).extrude(z1-z0).translate((0,0,z0))
    if fillet:
        try:obj=obj.edges().fillet(fillet)
        except Exception: pass
    return obj.val()


def arc(ri,ro,z0,z1,theta0,theta1):
    # CQ sketch in XZ; angular revolve then rotate about world Z
    w=cq.Workplane('XZ').moveTo(ri,z0).lineTo(ro,z0).lineTo(ro,z1).lineTo(ri,z1).close()
    out=w.revolve(theta1-theta0,(0,0),(0,1)).val()
    return out.rotate((0,0,0),(0,0,1),theta0)


def cuboid_radial(angle,r,radial,tangential,zwidth,zcenter=0,fillet=0):
    wp=cq.Workplane('XY').box(radial,tangential,zwidth)
    if fillet:
        try:wp=wp.edges().fillet(fillet)
        except:pass
    return wp.val().translate((r,0,zcenter)).rotate((0,0,0),(0,0,1),angle)


def cylrad(angle,r,length,diameter,z=0):
    cylinder=cq.Solid.makeCylinder(diameter/2,length,cq.Vector(r-length/2,0,z),cq.Vector(1,0,0))
    return cylinder.rotate((0,0,0),(0,0,1),angle)


def planar(x,y,wx,wy,depth,z,fillet=0):
    wp=cq.Workplane('XY').box(wx,wy,depth).translate((x,y,z))
    if fillet:
        try:wp=wp.edges().fillet(fillet)
        except:pass
    return wp.val()


def build_ring():
    # Tres piezas de carcasa: banda de titanio y coronas mecanizadas. Geometría de mm nominales.
    core=tube(10.56,11.0,-3.49,3.49,.16)
    # Ventana RF atravesando parte de la banda (un recorte local)
    slot=cuboid_radial(168,10.85,1.0,3.1,1.75,0)
    try:core=core.cut(slot)
    except Exception:pass
    add('01 · Cuerpo mecanizado Ø22',core,'shell','titanium',12)
    add('02 · Corona superior',tube(9.91,10.97,3.60,4.25,.10),'shell','silver',17)
    add('03 · Corona inferior',tube(9.91,10.97,-4.25,-3.60,.10),'shell','silver',-13)
    add('04 · Faja superior cepillada',tube(10.88,10.99,3.32,3.49,.034),'shell','titanium_dark',12)
    add('05 · Faja inferior cepillada',tube(10.88,10.99,-3.49,-3.32,.034),'shell','titanium_dark',12)
    add('06 · Línea azul',tube(10.991,11.012,3.48,3.585,.012),'accent','blue',13)
    add('07 · Línea reflejada',tube(10.991,11.008,-3.585,-3.48,.012),'accent','blue',12)
    add('08 · Junta superior',tube(9.888,9.928,3.65,3.77),'seal','seal',3)
    add('09 · Junta inferior',tube(9.888,9.928,-3.77,-3.65),'seal','seal',-4)

    # PEEK con recortes radiales reales para ventanas sensoriales.
    liner=tube(9.5,9.90,-3.68,3.68,.15)
    for angle,tw,zw,zc in [(218,3.4,2.4,-.2),(306,1.5,1.6,0),(54,1.6,2.0,.2),(140,2.,2.,0),(345,1.8,1.8,0),(272,1.5,1.5,0),(18,1.7,1.8,0)]:
        try:liner=liner.cut(cuboid_radial(angle,9.7,1.1,tw,zw,zc))
        except Exception:pass
    add('10 · Camisa PEEK, ventanas mecanizadas',liner,'liner','peek',-7)
    add('11 · Ventana RF dieléctrica',cuboid_radial(168,10.75,.41,2.84,1.52,fillet=.11),'rfwindow','glass',12)

    # Flex doble capa simulado. 325° de desarrollo útil.
    add('12 · Flex poliimida circular',arc(9.98,10.068,-2.82,2.82,-80,244),'pcb','flex',0)
    # Fajas metálicas con trazado interrumpido y discretizado, guardando segmentos finos.
    for i,(z,t0,t1) in enumerate([(-2.31,-68,104),(-2.31,115,228),(-1.20,-72,52),(-1.20,67,236),(.05,-76,125),(.05,138,237),(1.17,-72,38),(1.17,48,236),(2.30,-75,114),(2.30,128,232)]):
        add(f'Pista {i+1:02d}',arc(10.074,10.104,z-.047,z+.047,t0,t1),'copper','copper',0)
    for a in range(-65,240,17):
        if a%2:
            for z in (-2.32,-.05,2.28):
                add(f'Vía {a} / {z}',cylrad(a,10.09,.09,.20,z),'copper','gold',0)
    # Batería curva: volumen artístico deliberadamente delgado.
    add('13 · Batería flexible encapsulada',arc(10.13,10.46,-2.63,2.63,-33,45),'battery','battery',3)
    add('14 · Adhesivo batería',arc(10.47,10.505,-2.30,2.30,-28,41),'battery','battery_label',3)
    for a in [-28,40]:
        add(f'Batería, terminal {a}',cuboid_radial(a,10.40,.10,.36,.9),'battery','gold',3)

    # MCU con soporte, dados y orificio de referencia.
    for family,angle,r,tw,zw,rd,zpos,expl,base_mat in [
      ('mcu',-154,10.18,3.05,2.85,.36,-.30,-1,'chip'),
      ('pmic',-109,10.19,1.52,1.69,.28,1.04,-1,'chip_top'),
      ('mems',48,10.16,1.3,1.25,.26,.62,-1,'chip'),
    ]:
        add(f'{family.upper()} · PCB solder pads',cuboid_radial(angle,10.095,.065,tw+.36,zw+.38,zpos,fillet=.024),family,'gold',0)
        add(f'{family.upper()} · encapsulado',cuboid_radial(angle,r,rd,tw,zw,zpos,fillet=.045),family,base_mat,0)
        add(f'{family.upper()} · marca',cuboid_radial(angle,r+.195,.028,.25,.25,zpos+.7 if zw>2 else zpos+.27),family, 'orange' if family=='mems' else 'silver',0)
        for offset in [-tw*.35,0,tw*.35]:
            add(f'{family.upper()} · contacto {offset}',cuboid_radial(angle,10.096,.05,.15,.26,zpos +(-zw/2+.2)),family,'copper',0)

    # Antena PCB serpentina en una zona de radio: tramos largos tangenciales con espacio entre pistas.
    for i in range(5):
        zi=-.68+i*.33
        length=2.2 if i in (0,4) else 2.60
        add(f'RF meandro {i}',cuboid_radial(168,10.20,.06,length,.065,zi),'antenna','gold',0)
        if i < 4:
            add(f'RF retorno {i}',cuboid_radial(168,10.20,.06,.072,.34,zi+.163),'antenna','gold',0)

    # PPG dual + fotodetector: ventana PEEK, marco oscuro, 2 leds y una célula óptica.
    a=218
    add('15 · Marco óptico PPG',cuboid_radial(a,9.54,.10,3.18,2.2,-.2,fillet=.13),'ppg','glass',-7)
    add('16 · Cristal PPG',cuboid_radial(a,9.474,.045,2.9,1.9,-.2,fillet=.12),'ppg','optical',-7)
    for lbl,off,mat in [('Fotodiodo',-.85,'chip'),('LED verde',.15,'sensor_green'),('LED rojo',.92,'sensor_red')]:
        shape=cuboid_radial(a,9.445,.025,.47,.54,-.2)
        # mueve una celda a lo largo de tangencial
        shape=shape.translate((-math.sin(math.radians(a))*off,math.cos(math.radians(a))*off,0))
        add('PPG · '+lbl,shape,'ppg',mat,-7)
    # Contacto termal interno.
    for a,name,mat,tw,zw in [(306,'17 · Termistor de piel','temp',1.08,1.10), (54,'18 · Presión / película','pressure',1.20,1.25)]:
        add(name+' · aislante',cuboid_radial(a,9.58,.09,tw+.22,zw+.2,fillet=.09), 'temp' if mat=='temp' else 'pressure','glass',-7)
        add(name,cuboid_radial(a,9.473,.052,tw,zw,fillet=.08),'temp' if mat=='temp' else 'pressure',mat,-7)
    # EDA: contactos dobles no se tocan entre sí.
    for i,a in enumerate([140,345]):
        add(f'19 · EDA electrodo {i+1}',cuboid_radial(a,9.482,.044,1.36,1.59,fillet=.16),'eda','gold',-7)
        add(f'20 · EDA arillo {i+1}',cuboid_radial(a,9.532,.05,1.56,1.79,fillet=.13),'eda','seal',-7)
    # Módulos exploratorios en ranuras sobre cara interior.
    for family,angle,tw,zw,mat,idx in [('fluid',272,1.32,1.25,'fluid','21'),('biosensor',18,1.32,1.25,'experimental','22')]:
        add(f'{idx} · {family}, cubierta',cuboid_radial(angle,9.54,.07,tw+.15,zw+.14,fillet=.07),family,'glass',-7)
        add(f'{idx} · {family}, ventana',cuboid_radial(angle,9.474,.045,tw,zw,fillet=.07),family,mat,-7)
        if family=='fluid':
            for iz in (-.30,0,.30):
                add(f'Microcanal {iz}',cuboid_radial(angle,9.441,.026,.85,.065,iz),'fluid','fluid',-7)
        else:
            for ii in range(3):
                add(f'Electrodo químico {ii}',cuboid_radial(angle,9.446,.020,.20,.48,ii*.30-.3),'biosensor','gold',-7)
    # Sensor CGRP NO se monta en la escena comercial: solo maqueta opcional experimental.
    add('23 · CGRP prototipo NO validado',cuboid_radial(-64,9.88,.22,1.27,1.36,fillet=.07),'cgrp','cgrp',-11)


def build_flat():
    """Desarrollo conceptual de 1 vuelta de flex. Orientación de cara X-Y +Z."""
    add('PCB flexible, capa dieléctrica',planar(0,0,57.4,6.18,.14,0,fillet=.24),'pcb','flex',view='flat')
    # Banda de cubierta oscura interna semitransparente? copper traces as individual CAD metal strips.
    for y in (-2.39,-1.36,0,1.36,2.39):
        for x0,x1 in [(-27.3,-11.2),(-10.2,8.6),(10.0,27.3)]:
            add(f'Pista {y}, {x0}',planar((x1+x0)*.5,y,x1-x0,.075,.025,.083),'copper','copper',view='flat')
    # Ortogonales entre rutas con diseño electrónico.
    for x in [-22,-18,-11,-5,3,11,17,23]:
        add(f'Interconexión {x}',planar(x,0,.07,4.5,.023,.083),'copper','gold',view='flat')
    for x in np.linspace(-26.4,26.4,38):
        for y in (-2.85,2.85):
            add(f'Pad borde {x:.1f}/{y}',planar(float(x),y,.29,.26,.035,.087),'copper','gold',view='flat')
    # paquete CIs.
    ic_list=[('mcu',-7.2,-.30,3.30,3.25,'chip'),('pmic',2.2,1.0,1.72,1.60,'chip_top'),('mems',13.0,-.45,1.62,1.62,'chip'),('temp',17.6,1.55,1.25,1.1,'temp'),('ppg',-19.4,-.20,2.7,2.0,'glass'),('pressure',22.7,-.5,1.55,1.6,'pressure'),('biosensor',25,1.5,1.15,1.05,'experimental')]
    for family,x,y,wx,wy,mat in ic_list:
        add(f'{family.upper()} · footprint',planar(x,y,wx+.3,wy+.30,.03,.104),'copper','gold',view='flat')
        add(f'{family.upper()} · package',planar(x,y,wx,wy,.44,.335,fillet=.07),family,mat,view='flat')
        for k in range(4):
            px=x-wx/2+(k+.55)*wx/4.5
            for off in (-1,1):
                add(f'{family.upper()} · pad {k}/{off}',planar(px,y+off*(wy/2+.12),.20,.15,.025,.12),family,'silver',view='flat')
    # Batería desplegada arriba de cinta: no encaja si se usa el espesor nominal de referencia.
    add('BAT · celda curva equivalente',planar(-.3,0,10.8,4.0,.55,.49,fillet=.16),'battery','battery',view='flat')
    add('BAT · aislamiento',planar(-.3,0,9.8,3.3,.025,.778,fillet=.16),'battery','battery_label',view='flat')
    for x in (-5.8,5.2):
        add('BAT · terminal',planar(x,.0,1.,.65,.03,.79),'battery','gold',view='flat')
    # Antena serpenteante izquierda a la derecha de placa.
    for iy in range(7):
        y=-1.85+iy*.60
        add(f'Antena meandro {iy}',planar(7.70,y,4.00,.100,.03,.14),'antenna','gold',view='flat')
        if iy<6:
            add(f'Antena curva {iy}',planar(7.70 + (2 if iy%2==0 else -2),y+.30,.10,.60,.03,.14),'antenna','gold',view='flat')
    # 2 electrodos táctiles EDA
    for i,x in enumerate([-25.45,-12.35]):
        add(f'EDA pad plano {i+1}',planar(x,-1.05,1.6,1.65,.06,.16,fillet=.15),'eda','gold',view='flat')
    # ventana óptica conteniendo emisores y fotodiodo
    for i,x in enumerate([-20.17,-19.35,-18.56]):
        add(f'PPG elemento {i}',planar(x,-.05,.32,.4,.035,.62),'ppg',['sensor_green','chip','sensor_red'][i],view='flat')
    # microfluídica de investigación en el extremo
    add('Lab · microfluídica desplegada',planar(26,0,1.54,1.35,.14,.24,fillet=.08),'fluid','fluid',view='flat')
    add('Lab · CGRP hipótesis',planar(24,-2.2,1.2,.80,.25,.35,fillet=.07),'cgrp','cgrp',view='flat')



def add_pro_detail():
    """Microdetalle CAD industrial: ingeniería conceptual, no ruteado electrónico verificable."""
    # Perfilería lateral con relieves anodizados y anillo espaciador en el bisel.
    for z,r1,r2,mat in [(3.15,10.978,10.991,'blackmetal'),(-3.15,10.978,10.991,'blackmetal'),
                       (2.89,10.996,11.001,'silver'),(-2.89,10.996,11.001,'silver'),
                       (3.86,10.965,10.972,'titanium_dark'),(-3.86,10.965,10.972,'titanium_dark')]:
        add(f'Microanillo de precisión z={z}',tube(r1,r2,z-.028,z+.028),'fasteners',mat,10 if z>0 else -10)
    # Dos marcas de orientación tipo reloj (micrograbado visual con sólidos finos).
    for ai in [6,174,274]:
        add(f'Grabado de referencia {ai}°',cuboid_radial(ai,10.998,.012,.24,.36,2.17,fillet=.018),'fasteners','blackmetal',10)
    # Pares de microguías internas para soportes de sensores y canales de sellado.
    for ai in [218,306,54,140,345,272,18]:
        for z in (-1.20,1.20):
            add(f'Guía PEEK {ai}° · {z}',cuboid_radial(ai,9.506,.050,.13,.33,z,fillet=.022),'liner','ceramic',-7)
    # Conjunto PPG multispectral: LED infrarrojo adicional, separadores ópticos y micro ventanas.
    ai=218
    for off,z,w,mat,name in [(-.9,-.52,.55,'blackmetal','Separador fotodetector'),(.09,-.51,.50,'blackmetal','Separador emisor'),(.88,-.52,.40,'blackmetal','Separador rojo')]:
        sh=cuboid_radial(ai,9.457,.036,w,.072,z,fillet=.015)
        sh=sh.translate((-math.sin(math.radians(ai))*off, math.cos(math.radians(ai))*off, 0))
        add('PPG · '+name,sh,'lightbaffle',mat,-7)
    for off,mat,label in [(-.6,'sensor_green','Verde 530nm ~'),(.19,'sensor_red','Rojo 660nm ~'),(.72,'microled','IR 940nm ~')]:
        sh=cuboid_radial(ai,9.419,.018,.24,.22,.34,fillet=.02)
        sh=sh.translate((-math.sin(math.radians(ai))*off, math.cos(math.radians(ai))*off, 0))
        add(f'PPG · dado {label}',sh,'ppg',mat,-7)
    # Pistas auxiliares / antena y masa escalonada.
    for i,a in enumerate(range(80,156,9)):
        add(f'Masa PCB · {i}',arc(10.080,10.108,-1.88,-1.81,a,a+6),'copper','copper',0)
    for ai in [68,76,84,94,104,112,121,130,138,146,156]:
        add(f'Microvía {ai}',cylrad(ai,10.094,.031,.12,1.72),'passives','gold',0)
    # Elementos SMD para balance visual de la PCB (capacitancias, ESD, resistencias de paso).
    for idx,ai in enumerate(range(-55,235,12)):
        if ai in (-151,-115,53,218):continue
        zr=[-2.07,-1.63,1.87,2.27][idx%4]
        width=.42 if idx%3 else .60
        add(f'SMD 0201/0402 · {idx:02d} · terminal A',cuboid_radial(ai-1.2,10.11,.065,.12,.20,zr),'passives','silver',0)
        add(f'SMD 0201/0402 · {idx:02d} · cuerpo',cuboid_radial(ai,10.152,.095,width,.26,zr,fillet=.022),'passives','chip_top',0)
        add(f'SMD 0201/0402 · {idx:02d} · terminal B',cuboid_radial(ai+1.2,10.11,.065,.12,.20,zr),'passives','silver',0)
    # Memoria externa, oscilador simbólico y controlador de protección cerca del BLE.
    for name,family,ai,z,wx,wy in [('Flash NOR','flash',-127,-1.88,1.02,.81),('RTC / referencia','passives',-122,1.41,.80,.63),('Protección ESD','charge',-102,-1.84,.66,.58)]:
        add(f'{name} · pads',cuboid_radial(ai,10.093,.027,wx+.20,wy+.19,z,fillet=.02),family,'gold',0)
        add(f'{name} · encapsulado',cuboid_radial(ai,10.196,.19,wx,wy,z,fillet=.032),family,'chip',0)
        add(f'{name} · pin 1',cuboid_radial(ai,10.313,.009,.12,.12,z+.18),family,'ceramic',0)
    # Indicios de adhesivado, juntas ópticas y empaquetado de electroquímica.
    for ai,fam in [(218,'ppg'),(306,'temp'),(54,'pressure'),(272,'fluid'),(18,'biosensor')]:
        add(f'Sellado modular {fam}',cuboid_radial(ai,9.520,.028,1.62,1.80,fillet=.08),'seal','bond',-7)
    # Contactos de recarga representados como dos terminales externos aislados (riesgo estanqueidad).
    for k,z in enumerate([1.17,-1.17]):
        add(f'Pin de base de carga {k+1}',cuboid_radial(0,10.999,.012,.56,.48,z,fillet=.08),'charge','gold',11)
        add(f'Aislante de carga {k+1}',cuboid_radial(0,10.977,.018,.71,.62,z,fillet=.10),'charge','blackmetal',10)
    # Módulo de sudor demostrativo con cámara capilar y zonas de lectura (no validado).
    for ai in [270,272,274]:
        add(f'Capilar de sudor {ai}',cuboid_radial(ai,9.423,.014,.20,.58,fillet=.026),'fluid','fluid',-7)
    for i,z in enumerate([-.38,0,.38]):
        add(f'Biosensor: microelectrodo {i+1}',cuboid_radial(18,9.420,.016,.10,.25,z),'biosensor','gold',-7)
    # Matriz de etiquetas físicas mediante facetas discretas, no letras de texto trazadas.
    for ai in [256,258,260]:
        add(f'Marca de identificación {ai}',cuboid_radial(ai,10.997,.009,.11,.46,0,fillet=.008),'fasteners','blackmetal',10)



def add_branding():
    """Microtipografía tangencial sobre la carcasa: marca de diseñador a escala CAD."""
    brand='LATAMinds'
    start=-67.0
    for i,ch in enumerate(brand):
        angle=start+i*5.3
        try:
            # Cada letra es un sólido, tangente a la superficie Ø22 mm.
            shape=(cq.Workplane('YZ')
                      .text(ch,.87,.012,font='DejaVu Sans',kind='bold',halign='center',valign='center')
                      .val().translate((10.994,0,-.20))
                      .rotate((0,0,0),(0,0,1),angle))
            add(f'LATAMinds · grabado {ch}{i}',shape,'branding','blackmetal',11)
        except Exception as ex:
            print('WARN tipografía lateral:',ch,str(ex))
    # Firma óptica sin ilustrar una luz real.
    for ang in [-72,-70,-68]:
        add(f'LATAMinds · triple marca {ang}',cuboid_radial(ang,10.998,.014,.15,.10,-1.11),'branding','teal',11)

def add_flat_detail():
    # Resistores/capacitores y vías en la PCB plana, con huellas visuales de proceso.
    for i in range(28):
        x=-26.0+(i%14)*3.74; y=(-1.84 if i<14 else 1.83)
        add(f'FLEX SMD {i:02d} A',planar(x-.29,y,.20,.22,.03,.104),'passives','gold',view='flat')
        add(f'FLEX SMD {i:02d} B',planar(x+.29,y,.20,.22,.03,.104),'passives','gold',view='flat')
        add(f'FLEX SMD {i:02d} cuerpo',planar(x,y,.40,.26,.22,.240,fillet=.035),'passives','chip_top',view='flat')
    for i,x in enumerate(np.linspace(-26.3,26.3,34)):
        for y in [-2.05,2.05]:
            add(f'FLEX Microvía {i},{y}',planar(float(x),y,.12,.12,.025,.100),'copper','gold',view='flat')
    for i,y in enumerate([-.58,.0,.58]):
        add(f'FLEX canales microfluídicos {i}',planar(25.8,y,1.24,.09,.04,.345),'fluid','fluid',view='flat')
    # Marcas de fotodiodo / matriz LED rojo verde IR sobre la placa
    for i,x in enumerate([-20.7,-19.9,-19.1,-18.3]):
        add(f'FLEX PPG celda {i}',planar(x,-.10,.29,.52,.13,.68),'ppg',['silicon','sensor_green','sensor_red','microled'][i],view='flat')

def tri_from_shape(shape):
    vectors,faces=shape.tessellate(0.065,0.25)
    if len(faces)==0:raise ValueError('sin caras')
    v=np.array([[e.x,e.y,e.z] for e in vectors],dtype=np.float32)
    f=np.array(faces,dtype=np.uint32)
    mesh=trimesh.Trimesh(vertices=v,faces=f,process=False)
    mesh.fix_normals()
    return mesh


def export_files(folder):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    print(f'[1/5] Convirtiendo {len(PARTS)} piezas CAD a mallas…',flush=True)
    records=[]
    ring_scene=trimesh.Scene();flat_scene=trimesh.Scene()
    assembly=cq.Assembly(name='MigraRing_Bio_Pro_ConceptCAD')
    assembly_flat=cq.Assembly(name='PCB_desplegada_conceptual')
    failures=[]
    for k,p in enumerate(PARTS):
        try:
            mesh=tri_from_shape(p.shape)
            col=MAT[p.material][1]
            rgb=tuple(int(col[h:h+2],16) for h in (1,3,5))
            mesh.visual=trimesh.visual.TextureVisuals(material=trimesh.visual.material.PBRMaterial(name=p.material,baseColorFactor=[*rgb,255],metallicFactor=MAT[p.material][2],roughnessFactor=MAT[p.material][3]))
            (ring_scene if p.view=='ring' else flat_scene).add_geometry(mesh,geom_name=f'{k:03d}_{p.family}',node_name=f'{k:03d}_{p.name}',transform=np.diag([.001,.001,.001,1.]))
            (assembly if p.view=='ring' else assembly_flat).add(p.shape,name=f'part_{k:03d}',color=cq.Color(*[x/255 for x in rgb]))
            # compress geometry: vertices and triangle indices raw little endian as base64.
            verts=mesh.vertices.astype('<f4'); norms=mesh.vertex_normals.astype('<f4');indices=mesh.faces.astype('<u4')
            records.append({'id':k,'n':p.name,'f':p.family,'m':p.material,'e':p.exploded,'v':p.view,
                'pos':base64.b64encode(verts.tobytes()).decode('ascii'),
                'norm':base64.b64encode(norms.tobytes()).decode('ascii'),
                'idx':base64.b64encode(indices.tobytes()).decode('ascii'),
                'count':len(mesh.faces),'center':np.asarray(mesh.centroid,dtype=float).round(3).tolist()})
        except Exception as ex:
            failures.append((p.name,str(ex)))
        if k%45==0:print(f'   {k+1}/{len(PARTS)}',flush=True)
    if failures:print('WARN tessellation failures',failures[:20])
    print('[2/5] Exportando GLB de presentación…',flush=True)
    ring_scene.export(folder/'LATAMinds_MigraRing_ensamblaje.glb')
    flat_scene.export(folder/'LATAMinds_MigraRing_electronica.glb')
    print('[3/5] Exportando CAD STEP editable…',flush=True)
    assembly.save(str(folder/'LATAMinds_MigraRing_ensamblaje.step'))
    assembly_flat.save(str(folder/'LATAMinds_MigraRing_electronica.step'))
    print('[4/5] Construyendo visor local interactivo…',flush=True)
    template=(BASE/'visor_template.html').read_text(encoding='utf-8')
    data={'parts':records,'materials':{k:{'name':v[0],'color':v[1],'metallic':v[2],'roughness':v[3],'opacity':v[4]} for k,v in MAT.items()},
          'meta':{k:{'title':v[0],'group':v[1],'description':v[2],'warning':v[3],'status':v[4]} for k,v in META.items()}}
    logo64=base64.b64encode((BASE/'LATAMinds_logo_transparente.png').read_bytes()).decode('ascii')
    html=(template.replace('/*__BRAND_LOGO__*/',logo64)
          .replace('/*__TECH_DATA__*/','const TECH_DATA = '+json.dumps(TECH_DATA,separators=(',',':'),ensure_ascii=False)+';')
          .replace('/*__SCENE_DATA__*/', 'const SCENE_DATA = '+json.dumps(data,separators=(',',':'),ensure_ascii=False)+';'))
    (folder/'LATAMinds_MigraRing_Studio_v3.html').write_text(html,encoding='utf-8')
    with (folder/'BOM_LATAMinds_MigraRing.csv').open('w',encoding='utf-8-sig',newline='') as fh:
        writer=csv.writer(fh);writer.writerow(['Componente','Función','Consumo estimado','Tamaño de referencia','Madurez','Riesgo técnico'])
        for rec in TECH_DATA['components'].values():
            writer.writerow([rec['name'],rec['function'],rec['power'],rec['size'],rec['maturity'],rec['risk']])
    (folder/'Parametros_de_ingenieria.json').write_text(json.dumps(TECH_DATA,indent=2,ensure_ascii=False),encoding='utf-8')
    print('[5/5] Documentación y paquete…',flush=True)
    readme=(BASE/'LEEME_LATAMinds.md').read_text(encoding='utf-8')
    (folder/'LEEME_LATAMinds.md').write_text(readme,encoding='utf-8')
    for fn in ['migraring_lataminds_studio.py','visor_template.html','ficha_tecnica.py','LATAMinds_logo_transparente.png','lataminds_original.png','prepare_logo.py','requirements.txt']:
        src=BASE/fn
        dst=folder/fn
        if src.resolve()!=dst.resolve():dst.write_bytes(src.read_bytes())
    # ZIP generado desde una carpeta de salida para un paquete autónomo.
    archive=folder.parent/'LATAMinds_MigraRing_Studio_v3.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for path in sorted(folder.iterdir()):
            if path.is_file():z.write(path,arcname=path.name)
    print(f'OK: {len(records)} mallas, {len(failures)} errores, visor {len(html)/1e6:.1f}MB',flush=True)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--carpeta',default=str(BASE/'GENERADOS'))
    ap.add_argument('--abrir',action='store_true')
    args=ap.parse_args()
    build_ring();add_pro_detail();add_branding();build_flat();add_flat_detail();export_files(args.carpeta)
    if args.abrir:webbrowser.open((Path(args.carpeta)/'LATAMinds_MigraRing_Studio_v3.html').resolve().as_uri())
if __name__=='__main__':main()
