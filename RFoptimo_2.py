from opentrons import protocol_api
from opentrons.protocol_api import SINGLE
from opentrons.types import Point

metadata = {
    "protocolName": "Sintesis Automatizada de Hidrogeles PEGDA-TEA-RF (segundas 32-3 rep) optimizado (LHS Design)",
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
    muestras = [
        ("A1", 60.00, 39.81, 44.13), ("A2", 75.91, 32.91, 33.65), ("A3", 56.82, 35.81, 57.87),
        ("A4", 53.51, 37.74, 59.43), ("A5", 80.45, 37.23, 40.45), ("A6", 63.47, 38.69, 54.01),
        ("A7", 50.30, 38.78, 78.13), ("A8", 59.25, 30.09, 73.31), ("A9", 67.95, 30.61, 60.64),
        ("A10", 78.58, 36.30, 40.14), ("A11", 85.66, 38.43, 33.18), ("A12", 63.04, 33.60, 52.36),
        ("B1", 52.43, 31.64, 78.96), ("B2", 71.68, 31.88, 48.70), ("B3", 58.67, 32.26, 77.76),
        ("B4", 62.28, 36.68, 66.73), ("B5", 85.21, 31.42, 41.25), ("B6", 78.36, 33.42, 47.63),
        ("B7", 83.36, 34.27, 50.87), ("B8", 69.06, 38.06, 48.58), ("B9", 55.00, 35.56, 87.39),
        ("B10", 61.14, 30.93, 87.91), ("B11", 74.23, 35.18, 57.47), ("B12", 67.33, 32.77, 53.23),
        ("C1", 59.42, 34.68, 71.36), ("C2", 81.43, 31.16, 55.47), ("C3", 87.32, 34.82, 38.49),
        ("C4", 53.84, 33.86, 83.28), ("C5", 72.57, 35.95, 52.74), ("C6", 81.12, 39.36, 41.79),
        ("C7", 67.98, 36.95, 67.70), ("C8", 76.88, 39.57, 49.77), ("C9", 60.00, 39.81, 44.13),
        ("C10", 75.91, 32.91, 33.65), ("C11", 56.82, 35.81, 57.87), ("C12", 53.51, 37.74, 59.43),
        ("D1", 80.45, 37.23, 40.45), ("D2", 63.47, 38.69, 54.01), ("D3", 50.30, 38.78, 78.13),
        ("D4", 59.25, 30.09, 73.31), ("D5", 67.95, 30.61, 60.64), ("D6", 78.58, 36.30, 40.14),
        ("D7", 85.66, 38.43, 33.18), ("D8", 63.04, 33.60, 52.36), ("D9", 52.43, 31.64, 78.96),
        ("D10", 71.68, 31.88, 48.70), ("D11", 58.67, 32.26, 77.76), ("D12", 62.28, 36.68, 66.73),
        ("E1", 85.21, 31.42, 41.25), ("E2", 78.36, 33.42, 47.63), ("E3", 83.36, 34.27, 50.87),
        ("E4", 69.06, 38.06, 48.58), ("E5", 55.00, 35.56, 87.39), ("E6", 61.14, 30.93, 87.91),
        ("E7", 74.23, 35.18, 57.47), ("E8", 67.33, 32.77, 53.23), ("E9", 59.42, 34.68, 71.36),
        ("E10", 81.43, 31.16, 55.47), ("E11", 87.32, 34.82, 38.49), ("E12", 53.84, 33.86, 83.28),
        ("F1", 72.57, 35.95, 52.74), ("F2", 81.12, 39.36, 41.79), ("F3", 67.98, 36.95, 67.70),
        ("F4", 76.88, 39.57, 49.77), ("F5", 60.00, 39.81, 44.13), ("F6", 75.91, 32.91, 33.65),
        ("F7", 56.82, 35.81, 57.87), ("F8", 53.51, 37.74, 59.43), ("F9", 80.45, 37.23, 40.45),
        ("F10", 63.47, 38.69, 54.01), ("F11", 50.30, 38.78, 78.13), ("F12", 59.25, 30.09, 73.31),
        ("G1", 67.95, 30.61, 60.64), ("G2", 78.58, 36.30, 40.14), ("G3", 85.66, 38.43, 33.18),
        ("G4", 63.04, 33.60, 52.36), ("G5", 52.43, 31.64, 78.96), ("G6", 71.68, 31.88, 48.70),
        ("G7", 58.67, 32.26, 77.76), ("G8", 62.28, 36.68, 66.73), ("G9", 85.21, 31.42, 41.25),
        ("G10", 78.36, 33.42, 47.63), ("G11", 83.36, 34.27, 50.87), ("G12", 69.06, 38.06, 48.58),
        ("H1", 55.00, 35.56, 87.39), ("H2", 61.14, 30.93, 87.91), ("H3", 74.23, 35.18, 57.47),
        ("H4", 67.33, 32.77, 53.23), ("H5", 59.42, 34.68, 71.36), ("H6", 81.43, 31.16, 55.47),
        ("H7", 87.32, 34.82, 38.49), ("H8", 53.84, 33.86, 83.28), ("H9", 72.57, 35.95, 52.74),
        ("H10", 81.12, 39.36, 41.79), ("H11", 67.98, 36.95, 67.70), ("H12", 76.88, 39.57, 49.77)
    ]

    # --- LISTAS TEA ---
    
    m_tea_02 = [
        ("B8", 44.30), ("E4", 44.30), ("G12", 44.30)
    ]
    
    m_tea_05 = [
        ("C4", 29.02), ("E12", 29.02), ("H8", 29.02), # %TEA 0.07
        ("A5", 41.86), ("D1", 41.86), ("F9", 41.86), # %TEA 0.10
        ("B2", 47.75), ("D10", 47.75), ("G6", 47.75)  # %TEA 0.12
    ]
    
    m_tea_1 = [
        ("C6", 37.73), ("F2", 37.73), ("H10", 37.73), # %TEA 0.19
        ("A12", 51.00), ("D8", 51.00), ("G4", 51.00), # %TEA 0.25
        ("A1", 56.06), ("C9", 56.06), ("F5", 56.06),  # %TEA 0.28
        ("A2", 57.53), ("C10", 57.53), ("F6", 57.53)  # %TEA 0.29
    ]
    
    m_tea_3 = [
        ("B10", 20.02), ("E6", 20.02), ("H2", 20.02), # %TEA 0.30
        ("B9", 22.04), ("E5", 22.04), ("H1", 22.04),  # %TEA 0.33
        ("C7", 27.37), ("F3", 27.37), ("H11", 27.37), # %TEA 0.41
        ("B7", 31.50), ("E3", 31.50), ("G11", 31.50), # %TEA 0.47
        ("B11", 33.12), ("E7", 33.12), ("H3", 33.12), # %TEA 0.50
        ("B4", 34.30), ("D12", 34.30), ("G8", 34.30), # %TEA 0.51
        ("A8", 37.35), ("D4", 37.35), ("F12", 37.35), # %TEA 0.56
        ("B5", 42.12), ("E1", 42.12), ("G9", 42.12), # %TEA 0.63
        ("A10", 44.97), ("D6", 44.97), ("G2", 44.97), # %TEA 0.67
        ("A3", 49.51), ("C11", 49.51), ("F7", 49.51)  # %TEA 0.74
    ]
    
    m_tea_5 = [
        ("B3", 31.31), ("D11", 31.31), ("G7", 31.31), # %TEA 0.78
        ("C2", 31.94), ("E10", 31.94), ("H6", 31.94), # %TEA 0.80
        ("A7", 32.79), ("D3", 32.79), ("F11", 32.79), # %TEA 0.82
        ("C8", 33.78), ("F4", 33.78), ("H12", 33.78), # %TEA 0.84
        ("C1", 34.54), ("E9", 34.54), ("H5", 34.54),  # %TEA 0.86
        ("B1", 36.97), ("D9", 36.97), ("G5", 36.97),  # %TEA 0.92
        ("C5", 38.74), ("F1", 38.74), ("H9", 38.74),  # %TEA 0.97
        ("C3", 39.36), ("E11", 39.36), ("H7", 39.36), # %TEA 0.98
        ("B6", 40.59), ("E2", 40.59), ("G10", 40.59), # %TEA 1.01
        ("A9", 40.80), ("D5", 40.80), ("G1", 40.80),  # %TEA 1.02
        ("A11", 42.74), ("D7", 42.74), ("G3", 42.74), # %TEA 1.07
        ("A6", 43.83), ("D2", 43.83), ("F10", 43.83), # %TEA 1.10
        ("B12", 46.68), ("E8", 46.68), ("H4", 46.68), # %TEA 1.17
        ("A4", 49.32), ("C12", 49.32), ("F8", 49.32) # %TEA 1.23
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