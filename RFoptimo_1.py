from opentrons import protocol_api
from opentrons.protocol_api import SINGLE
from opentrons.types import Point

metadata = {
    "protocolName": "Sintesis Automatizada de Hidrogeles PEGDA-TEA-RF (primeras 32-3 rep) optimizado (LHS Design)",
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
  # Formato: ("Pozo", V_PEGDA, V_RF, V_AGUA)
    muestras = [
    ("A1", 55.23, 24.88, 81.95), ("A2", 70.52, 22.73, 84.07), ("A3", 79.30, 20.98, 67.05),
    ("A4", 51.99, 28.71, 93.27), ("A5", 70.82, 28.84, 53.14), ("A6", 64.15, 29.73, 66.30),
    ("A7", 76.53, 24.13, 63.26), ("A8", 53.99, 20.19, 94.64), ("A9", 69.40, 27.36, 70.30),
    ("A10", 80.81, 26.12, 54.88), ("A11", 56.09, 26.63, 88.91), ("A12", 73.71, 29.21, 50.75),
    ("B1", 50.92, 23.72, 81.37), ("B2", 86.64, 22.33, 52.78), ("B3", 81.73, 26.42, 44.35),
    ("B4", 57.44, 21.39, 64.40), ("B5", 72.17, 20.86, 75.81), ("B6", 83.07, 27.53, 41.59),
    ("B7", 65.02, 25.56, 83.83), ("B8", 86.08, 29.59, 41.86), ("B9", 67.06, 23.33, 72.46),
    ("B10", 66.17, 28.29, 64.01), ("B11", 74.01, 25.20, 65.87), ("B12", 63.89, 24.47, 77.09),
    ("C1", 70.52, 22.73, 84.07), ("C2", 51.50, 27.17, 77.02), ("C3", 60.25, 22.11, 68.89),
    ("C4", 77.05, 27.95, 60.11), ("C5", 58.33, 23.08, 73.40), ("C6", 84.32, 20.51, 47.65),
    ("C7", 82.60, 23.90, 67.08), ("C8", 53.99, 20.19, 94.64), ("C9", 76.53, 24.13, 63.26),
    ("C10", 62.55, 25.82, 62.91), ("C11", 69.40, 27.36, 70.30), ("C12", 80.81, 26.12, 54.88),
    ("D1", 56.09, 26.63, 88.91), ("D2", 70.82, 28.84, 53.14), ("D3", 51.99, 28.71, 93.27),
    ("D4", 73.71, 29.21, 50.75), ("D5", 50.92, 23.72, 81.37), ("D6", 79.30, 20.98, 67.05),
    ("D7", 86.64, 22.33, 52.78), ("D8", 81.73, 26.42, 44.35), ("D9", 57.44, 21.39, 64.40),
    ("D10", 72.17, 20.86, 75.81), ("D11", 83.07, 27.53, 41.59), ("D12", 55.23, 24.88, 81.95),
    ("E1", 65.02, 25.56, 83.83), ("E2", 86.08, 29.59, 41.86), ("E3", 67.06, 23.33, 72.46),
    ("E4", 66.17, 28.29, 64.01), ("E5", 74.01, 25.20, 65.87), ("E6", 63.89, 24.47, 77.09),
    ("E7", 70.52, 22.73, 84.07), ("E8", 51.50, 27.17, 77.02), ("E9", 60.25, 22.11, 68.89),
    ("E10", 77.05, 27.95, 60.11), ("E11", 58.33, 23.08, 73.40), ("E12", 84.32, 20.51, 47.65),
    ("F1", 82.60, 23.90, 67.08), ("F2", 53.99, 20.19, 94.64), ("F3", 76.53, 24.13, 63.26),
    ("F4", 62.55, 25.82, 62.91), ("F5", 69.40, 27.36, 70.30), ("F6", 80.81, 26.12, 54.88),
    ("F7", 56.09, 26.63, 88.91), ("F8", 70.82, 28.84, 53.14), ("F9", 51.99, 28.71, 93.27),
    ("F10", 73.71, 29.21, 50.75), ("F11", 50.92, 23.72, 81.37), ("F12", 79.30, 20.98, 67.05),
    ("G1", 86.64, 22.33, 52.78), ("G2", 81.73, 26.42, 44.35), ("G3", 57.44, 21.39, 64.40),
    ("G4", 72.17, 20.86, 75.81), ("G5", 83.07, 27.53, 41.59), ("G6", 55.23, 24.88, 81.95),
    ("G7", 65.02, 25.56, 83.83), ("G8", 86.08, 29.59, 41.86), ("G9", 67.06, 23.33, 72.46),
    ("G10", 66.17, 28.29, 64.01), ("G11", 74.01, 25.20, 65.87), ("G12", 63.89, 24.47, 77.09),
    ("H1", 70.52, 22.73, 84.07), ("H2", 51.50, 27.17, 77.02), ("H3", 60.25, 22.11, 68.89),
    ("H4", 77.05, 27.95, 60.11), ("H5", 58.33, 23.08, 73.40), ("H6", 84.32, 20.51, 47.65),
    ("H7", 82.60, 23.90, 67.08), ("H8", 53.99, 20.19, 94.64), ("H9", 76.53, 24.13, 63.26),
    ("H10", 62.55, 25.82, 62.91), ("H11", 69.40, 27.36, 70.30), ("H12", 80.81, 26.12, 54.88)
    ]
    
    m_tea_02 = [
    ("A4", 26.03), ("D3", 26.03), ("F9", 26.03),
    ("A3", 32.67), ("D6", 32.67), ("F12", 32.67)
    ]
    
    m_tea_05 = [
        ("B11", 34.92), ("E5", 34.92), ("G11", 34.92),
        ("B4", 56.77), ("D9", 56.77), ("G3", 56.77)
    ]
    
    m_tea_1 = [
        ("B12", 34.55), ("E6", 34.55), ("G12", 34.55),
        ("B10", 41.52), ("E4", 41.52), ("G10", 41.52),
        ("B8", 42.47), ("E2", 42.47), ("G8", 42.47),
        ("B3", 47.50), ("D8", 47.50), ("G2", 47.50)
    ]
    
    m_tea_3 = [
        ("A2", 22.69), ("C1", 22.69), ("E7", 22.69), ("H1", 22.69),
        ("B7", 25.59), ("E1", 25.59), ("G7", 25.59),
        ("C7", 26.42), ("F1", 26.42), ("H7", 26.42),
        ("A11", 28.37), ("D1", 28.37), ("F7", 28.37),
        ("A8", 31.18), ("C8", 31.18), ("F2", 31.18), ("H8", 31.18),
        ("C4", 34.89), ("E10", 34.89), ("H4", 34.89),
        ("B9", 37.15), ("E3", 37.15), ("G9", 37.15),
        ("B2", 38.26), ("D7", 38.26), ("G1", 38.26),
        ("B1", 43.98), ("D5", 43.98), ("F11", 43.98),
        ("A12", 46.32), ("D4", 46.32), ("F10", 46.32),
        ("B6", 47.81), ("D11", 47.81), ("G5", 47.81),
        ("C3", 48.75), ("E9", 48.75), ("H3", 48.75)
    ]
    
    m_tea_5 = [
        ("B5", 31.16), ("D10", 31.16), ("G4", 31.16),
        ("A9", 32.95), ("C11", 32.95), ("F5", 32.95), ("H11", 32.95),
        ("A7", 36.08), ("C9", 36.08), ("F3", 36.08), ("H9", 36.08),
        ("A1", 37.91), ("D12", 37.91), ("G6", 37.91),
        ("A10", 38.19), ("C12", 38.19), ("F6", 38.19), ("H12", 38.19),
        ("A6", 39.81),
        ("C2", 44.30), ("E8", 44.30), ("H2", 44.30),
        ("C5", 45.19), ("E11", 45.19), ("H5", 45.19),
        ("A5", 47.21), ("D2", 47.21), ("F8", 47.21),
        ("C6", 47.52), ("E12", 47.52), ("H6", 47.52),
        ("C10", 48.72), ("F4", 48.72), ("H10", 48.72)
    ]

    pasos_tea = [
        {'punta': 'B3', 'muestras': m_tea_02, 'fuente': tea_02},
        {'punta': 'B4', 'muestras': m_tea_05, 'fuente': tea_05},
        {'punta': 'B5', 'muestras': m_tea_1,  'fuente': tea_1},
        {'punta': 'B6', 'muestras': m_tea_3,  'fuente': tea_3},
        {'punta': 'B7', 'muestras': m_tea_5,  'fuente': tea_5},
    ]

    vol_max_p200 = 190

    # --- 6. EJECUCIÓN ---

    # PASO 1: AGUA
    protocol.comment("Distribuyendo Agua...")
    pipette.flow_rate.aspirate = 80
    pipette.flow_rate.dispense = 30
    pipette.flow_rate.blow_out = 60
    pipette.pick_up_tip(tipracks['B1'])
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
    pipette.pick_up_tip(tipracks['B2'])
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

    pipette.pick_up_tip(tipracks['B8'])
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