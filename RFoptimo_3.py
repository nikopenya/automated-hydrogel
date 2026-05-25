from opentrons import protocol_api
from opentrons.protocol_api import SINGLE
from opentrons.types import Point

metadata = {
    "protocolName": "Sintesis Automatizada de Hidrogeles PEGDA-TEA-RF (terceras 32-3 rep) optimizado (LHS Design)",
    "author": "NicolasPeña",
    "description": "Sintesis de los intervalos de composicion que gelifican a los 10 minutos (puntos dulces)",
}

requirements = {"robotType": "Flex", "apiLevel": "2.21"}

def run(protocol: protocol_api.ProtocolContext):

    # --- 1. CARGA DE LABWARE ---
    trash = protocol.load_trash_bin("A3")
    tipracks = protocol.load_labware("opentrons_flex_96_tiprack_200ul", "D3")
    res = protocol.load_labware("custom_4_reservoir_90000ul", "D2")
    res_2 = protocol.load_labware("19mlglass_15_tuberack_19000ul", "C3")
    res_3 = protocol.load_labware("custom_24_tuberack_6000ul", "B2")
    
    h_s = protocol.load_module('heaterShakerModuleV1', 'C1') 
    plate = h_s.load_labware("corning_96_wellplate_360ul_flat")

    # --- 2. CARGA DE INSTRUMENTOS ---
    pipette = protocol.load_instrument("flex_8channel_1000", mount="left", tip_racks=[tipracks])
    pipette.configure_nozzle_layout(style=SINGLE, start="H1")

    # --- 3. SEGURIDAD HEATER-SHAKER ---
    if h_s.labware_latch_status != 'closed':
        h_s.close_labware_latch()

    # --- 4. DEFINICIÓN DE FUENTES ---
    rf_002 = res_3['A1']
    pegda_80 = res_2['B1']
    agua = res['A1']
    tea_02 = res_3['B1']
    tea_05 = res_3['B2']
    tea_1= res_3['B3']
    tea_3 = res_3['B4']
    tea_5 = res_3['B5']

    # --- 5. DATOS DE DISPENSACIÓN ---
  # --- LISTA MUESTRAS: (POZO, V_PEGDA, V_RF, V_AGUA) ---
    # --- LISTA PRINCIPAL (Pozo, V_PEGDA, V_RF, V_AGUA) ---
# Datos aleatorizados basados en la placa morada/blanca
    muestras = [
        ("A1", 77.90, 43.31, 54.60), ("A2", 68.44, 45.96, 51.55), ("A3", 86.79, 40.72, 49.87),
        ("A4", 61.74, 42.69, 59.84), ("A5", 83.63, 47.78, 33.39), ("A6", 64.79, 48.38, 41.06),
        ("A7", 57.23, 47.84, 58.46), ("A8", 51.94, 49.61, 57.27), ("A9", 75.31, 41.64, 52.90),
        ("A10", 78.97, 41.18, 33.72), ("A11", 73.75, 44.38, 31.88), ("A12", 69.82, 42.30, 54.16),
        ("B1", 84.71, 48.89, 45.40), ("B2", 66.61, 47.49, 33.04), ("B3", 79.95, 46.43, 37.85),
        ("B4", 55.50, 40.30, 61.35), ("B5", 56.33, 42.10, 60.42), ("B6", 65.41, 41.51, 52.40),
        ("B7", 84.88, 45.56, 38.86), ("B8", 77.47, 49.23, 43.66), ("B9", 82.38, 44.01, 25.55),
        ("B10", 71.19, 47.15, 34.11), ("B11", 50.48, 44.22, 80.37), ("B12", 57.87, 45.87, 51.18),
        ("C1", 61.53, 43.52, 94.95), ("C2", 74.85, 49.74, 33.13), ("C3", 60.86, 48.45, 45.07),
        ("C4", 54.56, 46.72, 56.65), ("C5", 70.03, 40.59, 49.88), ("C6", 65.79, 42.90, 54.12),
        ("C7", 72.72, 44.52, 53.29), ("C8", 58.18, 45.06, 64.59), ("C9", 55.50, 40.30, 61.35),
        ("C10", 86.79, 40.72, 49.87), ("C11", 61.74, 42.69, 59.84), ("C12", 83.63, 47.78, 33.39),
        ("D1", 64.79, 48.38, 41.06), ("D2", 57.23, 47.84, 58.46), ("D3", 51.94, 49.61, 57.27),
        ("D4", 75.31, 41.64, 52.90), ("D5", 78.97, 41.18, 33.72), ("D6", 73.75, 44.38, 31.88),
        ("D7", 69.82, 42.30, 54.16), ("D8", 84.71, 48.89, 45.40), ("D9", 66.61, 47.49, 33.04),
        ("D10", 79.95, 46.43, 37.85), ("D11", 68.44, 45.96, 51.55), ("D12", 56.33, 42.10, 60.42),
        ("E1", 65.41, 41.51, 52.40), ("E2", 84.88, 45.56, 38.86), ("E3", 77.47, 49.23, 43.66),
        ("E4", 82.38, 44.01, 25.55), ("E5", 71.19, 47.15, 34.11), ("E6", 50.48, 44.22, 80.37),
        ("E7", 57.87, 45.87, 51.18), ("E8", 61.53, 43.52, 94.95), ("E9", 74.85, 49.74, 33.13),
        ("E10", 60.86, 48.45, 45.07), ("E11", 54.56, 46.72, 56.65), ("E12", 70.03, 40.59, 49.88),
        ("F1", 65.79, 42.90, 54.12), ("F2", 77.90, 43.31, 54.60), ("F3", 72.72, 44.52, 53.29),
        ("F4", 58.18, 45.06, 64.59), ("F5", 55.50, 40.30, 61.35), ("F6", 86.79, 40.72, 49.87),
        ("F7", 61.74, 42.69, 59.84), ("F8", 83.63, 47.78, 33.39), ("F9", 64.79, 48.38, 41.06),
        ("F10", 57.23, 47.84, 58.46), ("F11", 51.94, 49.61, 57.27), ("F12", 75.31, 41.64, 52.90),
        ("G1", 78.97, 41.18, 33.72), ("G2", 73.75, 44.38, 31.88), ("G3", 69.82, 42.30, 54.16),
        ("G4", 84.71, 48.89, 45.40), ("G5", 66.61, 47.49, 33.04), ("G6", 79.95, 46.43, 37.85),
        ("G7", 68.44, 45.96, 51.55), ("G8", 56.33, 42.10, 60.42), ("G9", 65.41, 41.51, 52.40),
        ("G10", 84.88, 45.56, 38.86), ("G11", 77.47, 49.23, 43.66), ("G12", 82.38, 44.01, 25.55),
        ("H1", 71.19, 47.15, 34.11), ("H2", 50.48, 44.22, 80.37), ("H3", 57.87, 45.87, 51.18),
        ("H4", 61.53, 43.52, 94.95), ("H5", 74.85, 49.74, 33.13), ("H6", 60.86, 48.45, 45.07),
        ("H7", 54.56, 46.72, 56.65), ("H8", 70.03, 40.59, 49.88), ("H9", 65.79, 42.90, 54.12),
        ("H10", 77.90, 43.31, 54.60), ("H11", 72.72, 44.52, 53.29), ("H12", 58.18, 45.06, 64.59)
    ]
    
    # --- LISTAS TEA (Ordenadas por volumen para facilitar pipeteo) ---
    m_tea_0 = [
    ('C1', 0.0), ('E8', 0.0), ('H4', 0.0),  # Vol: 0.0
    ]
    
    m_tea_02 = [] # Sin coincidencias para 26.03, 32.67 o 44.30
    
    m_tea_05 = [
        ('A3', 22.62), ('C10', 22.62), ('F6', 22.62),  # Vol: 22.62
        ('A7', 36.47), ('D2', 36.47), ('F10', 36.47),  # Vol: 36.47
    ]
    
    m_tea_1 = [
        ('B8', 29.64), ('E3', 29.64), ('G11', 29.64),  # Vol: 29.64
        ('A12', 33.72), ('D7', 33.72), ('G3', 33.72),  # Vol: 33.72
        ('B12', 45.08), ('E7', 45.08), ('H3', 45.08),  # Vol: 45.08
        ('B2', 52.86), ('D9', 52.86), ('G5', 52.86),  # Vol: 52.86
    ]
    
    m_tea_3 = [
        ('B1', 21.0), ('D8', 21.0), ('G4', 21.0),  # Vol: 21.0
        ('A1', 24.19), ('F2', 24.19), ('H10', 24.19),  # Vol: 24.19
        ('B11', 24.93), ('E6', 24.93), ('H2', 24.93),  # Vol: 24.93
        ('A9', 30.15), ('D4', 30.15), ('F12', 30.15),  # Vol: 30.15
        ('C8', 32.17), ('F4', 32.17), ('H12', 32.17),  # Vol: 32.17
        ('B3', 35.77), ('D10', 35.77), ('G6', 35.77),  # Vol: 35.77
        ('C5', 39.5), ('E12', 39.5), ('H8', 39.5),     # Vol: 39.5
        ('B6', 40.68), ('E1', 40.68), ('G9', 40.68),  # Vol: 40.68
        ('A8', 41.18), ('D3', 41.18), ('F11', 41.18),  # Vol: 41.18
        ('B4', 42.85), ('C9', 42.85), ('F5', 42.85),  # Vol: 42.85
        ('A6', 45.77), ('D1', 45.77), ('F9', 45.77),  # Vol: 45.77
        ('B10', 47.55), ('E5', 47.55), ('H1', 47.55),  # Vol: 47.55
    ]
    
    m_tea_5 = [
        ('B7', 30.7), ('E2', 30.7), ('G10', 30.7),     # Vol: 30.7
        ('A2', 34.05), ('D11', 34.05), ('G7', 34.05),  # Vol: 34.05
        ('A5', 35.2), ('C12', 35.2), ('F8', 35.2),     # Vol: 35.2
        ('A4', 35.73), ('C11', 35.73), ('F7', 35.73),  # Vol: 35.73
        ('C6', 37.19), ('F1', 37.19), ('H9', 37.19),  # Vol: 37.19
        ('B5', 41.15), ('D12', 41.15), ('G8', 41.15),  # Vol: 41.15
        ('C4', 42.07), ('E11', 42.07), ('H7', 42.07),  # Vol: 42.07
        ('C2', 42.28), ('E9', 42.28), ('H5', 42.28),  # Vol: 42.28
        ('C3', 45.62), ('E10', 45.62), ('H6', 45.62),  # Vol: 45.62
        ('A10', 46.13), ('D5', 46.13), ('G1', 46.13),  # Vol: 46.13
        ('B9', 48.06), ('E4', 48.06), ('G12', 48.06),  # Vol: 48.06
        ('A11', 49.99), ('D6', 49.99), ('G2', 49.99),  # Vol: 49.99
    ]
    pasos_tea = [
        {'punta': 'A3', 'muestras': m_tea_02, 'fuente': tea_02},
        {'punta': 'A4', 'muestras': m_tea_05, 'fuente': tea_05},
        {'punta': 'A5', 'muestras': m_tea_1,  'fuente': tea_1},
        {'punta': 'A6', 'muestras': m_tea_3,  'fuente': tea_3},
        {'punta': 'A7', 'muestras': m_tea_5,  'fuente': tea_5},
    ]

    vol_max_p200 = 190

    # --- 6. EJECUCIÓN ---

    # PASO 1: AGUA
    protocol.comment("Distribuyendo Agua...")
    pipette.flow_rate.aspirate = 80
    pipette.flow_rate.dispense = 30
    pipette.flow_rate.blow_out = 60
    pipette.pick_up_tip(tipracks['A1'])
    for well, v_peg, v_rf, v_agua in muestras:
        pipette.aspirate(v_agua, agua.bottom(z=3))
        pipette.dispense(v_agua, plate[well].top(z=2))
        dest_pared = plate[well].top(z=-2).move(Point(x=0, y=-2.5, z=0))
        pipette.move_to(dest_pared, speed=10) 
        pipette.blow_out(dest_pared)
        pipette.move_to(plate[well].top(z=10))
        protocol.delay(seconds=1)
    pipette.drop_tip(trash)
    
    # PASO 2: PEGDA
    protocol.comment("Distribuyendo PEGDA...")
    pipette.flow_rate.aspirate = 30
    pipette.flow_rate.dispense = 30
    pipette.pick_up_tip(tipracks['A2'])
    for well, v_peg, v_rf, v_agua in muestras:
        pipette.aspirate(v_peg, pegda_80.bottom(z=7))
        protocol.delay(seconds=2) 
        pipette.move_to(pegda_80.top(z=5),speed=10)
        pipette.dispense(v_peg, plate[well].top(z=2))
        dest_pared = plate[well].top(z=-2).move(Point(x=0, y=-2.5, z=0))
        pipette.move_to(dest_pared, speed=10) 
        pipette.blow_out(dest_pared)
    pipette.drop_tip(trash)

    # PASO 3: TEA
    protocol.comment("Distribuyendo TEA...")
    pipette.flow_rate.aspirate = 80
    pipette.flow_rate.dispense = 30
    pipette.flow_rate.blow_out = 60

    for paso in pasos_tea:
        pipette.pick_up_tip(tipracks[paso['punta']])
        for well, v_tea in paso['muestras']:
            # Solo aspiramos si el volumen es mayor a 0 para evitar errores
            if v_tea > 0:
                pipette.aspirate(v_tea, paso['fuente'].bottom(z=10))
                protocol.delay(seconds=1)
                pipette.dispense(v_tea, plate[well].top(z=2))
                dest_pared = plate[well].top(z=-2).move(Point(x=0, y=-2.5, z=0))
                pipette.move_to(dest_pared, speed=10) 
                pipette.blow_out(dest_pared)
                
        pipette.drop_tip(trash)

    # PASO 4: RF (Inicio forzado en A5)
    protocol.comment("Distribuyendo RF...")
    pipette.flow_rate.aspirate = 80
    pipette.flow_rate.dispense = 30
    pipette.flow_rate.blow_out = 60

    pipette.pick_up_tip(tipracks['A8'])
    liquido_en_punta = 0
    for well, v_peg, v_rf, v_agua in muestras:
        if liquido_en_punta < (v_rf + 10):
            espacio_libre = vol_max_p200 - liquido_en_punta
            pipette.aspirate(espacio_libre, rf_002.bottom(z=15))
            liquido_en_punta = vol_max_p200
        pipette.dispense(v_rf, plate[well].top(z=2))
        pipette.touch_tip(v_offset=-3, speed=5)
        protocol.delay(seconds=2)
        liquido_en_punta -= v_rf
    pipette.drop_tip(trash)

    # --- 7. FINALIZACIÓN ---
    protocol.comment("Iniciando agitación...")
    h_s.set_and_wait_for_shake_speed(1000)
    protocol.delay(minutes=2)
    h_s.deactivate_shaker()
    h_s.open_labware_latch()
    protocol.comment("Protocolo completado con éxito.")