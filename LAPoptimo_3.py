from opentrons import protocol_api
from opentrons.protocol_api import SINGLE
from opentrons.types import Point

# Metadatos del protocolo
metadata = {
    'protocolName': 'Sintesis Automatizada de Hidrogeles PEGDA-LAP (terceras 32-3 rep) optimizado (LHS Design)',
    'author': 'NicoPeña',
    'description': 'Preparacion de 96 muestras con gradientes de PEGDA y LAP usando Latin Hypercube Sampling.',
}

requirements = {"robotType": "Flex", "apiLevel": "2.21"}

def run(protocol: protocol_api.ProtocolContext):
    muestras = [
        ("A1", 82.48, 63.80, 53.72), ("A2", 69.70, 65.72, 64.58), ("A3", 35.78, 74.36, 89.86),
        ("A4", 99.44, 64.80, 35.76), ("A5", 50.73, 71.48, 77.79), ("A6", 72.85, 70.04, 57.11),
        ("A7", 64.31, 61.08, 74.61), ("A8", 88.83, 66.72, 44.45), ("A9", 37.41, 67.20, 95.39),
        ("A10", 46.36, 79.24, 74.40), ("A11", 79.07, 60.56, 60.37), ("A12", 90.53, 74.40, 35.07),
        ("B1", 47.63, 68.32, 84.05), ("B2", 93.75, 72.96, 33.29), ("B3", 61.29, 78.32, 60.39),
        ("B4", 77.58, 77.56, 44.86), ("B5", 38.58, 63.56, 97.86), ("B6", 59.54, 72.28, 68.18),
        ("B7", 84.90, 79.92, 35.18), ("B8", 41.13, 76.96, 81.91), ("B9", 80.81, 70.68, 48.51),
        ("B10", 43.71, 69.96, 86.33), ("B11", 55.68, 75.60, 68.72), ("B12", 66.74, 76.20, 57.07),
        ("C1", 87.38, 69.20, 43.42), ("C2", 96.76, 76.80, 26.44), ("C3", 43.00, 61.28, 95.72),
        ("C4", 58.33, 65.28, 76.39), ("C5", 65.64, 67.76, 66.60), ("C6", 94.84, 61.92, 43.24),
        ("C7", 52.84, 63.12, 84.04), ("C8", 74.36, 73.56, 52.09), ("C9", 35.78, 74.36, 89.86),
        ("C10", 69.70, 65.72, 64.58), ("C11", 82.48, 63.80, 53.72), ("C12", 37.41, 67.20, 95.39),
        ("D1", 72.85, 70.04, 57.11), ("D2", 64.31, 61.08, 74.61), ("D3", 99.44, 64.80, 35.76),
        ("D4", 88.83, 66.72, 44.45), ("D5", 50.73, 71.48, 77.79), ("D6", 79.07, 60.56, 60.37),
        ("D7", 90.53, 74.40, 35.07), ("D8", 46.36, 79.24, 74.40), ("D9", 47.63, 68.32, 84.05),
        ("D10", 38.58, 63.56, 97.86), ("D11", 93.75, 72.96, 33.29), ("D12", 61.29, 78.32, 60.39),
        ("E1", 77.58, 77.56, 44.86), ("E2", 59.54, 72.28, 68.18), ("E3", 84.90, 79.92, 35.18),
        ("E4", 41.13, 76.96, 81.91), ("E5", 80.81, 70.68, 48.51), ("E6", 43.71, 69.96, 86.33),
        ("E7", 55.68, 75.60, 68.72), ("E8", 66.74, 76.20, 57.07), ("E9", 87.38, 69.20, 43.42),
        ("E10", 96.76, 76.80, 26.44), ("E11", 43.00, 61.28, 95.72), ("E12", 58.33, 65.28, 76.39),
        ("F1", 65.64, 67.76, 66.60), ("F2", 94.84, 61.92, 43.24), ("F3", 52.84, 63.12, 84.04),
        ("F4", 74.36, 73.56, 52.09), ("F5", 82.48, 63.80, 53.72), ("F6", 35.78, 74.36, 89.86),
        ("F7", 69.70, 65.72, 64.58), ("F8", 37.41, 67.20, 95.39), ("F9", 99.44, 64.80, 35.76),
        ("F10", 72.85, 70.04, 57.11), ("F11", 88.83, 66.72, 44.45), ("F12", 50.73, 71.48, 77.79),
        ("G1", 64.31, 61.08, 74.61), ("G2", 79.07, 60.56, 60.37), ("G3", 90.53, 74.40, 35.07),
        ("G4", 46.36, 79.24, 74.40), ("G5", 47.63, 68.32, 84.05), ("G6", 93.75, 72.96, 33.29),
        ("G7", 38.58, 63.56, 97.86), ("G8", 61.29, 78.32, 60.39), ("G9", 77.58, 77.56, 44.86),
        ("G10", 59.54, 72.28, 68.18), ("G11", 84.90, 79.92, 35.18), ("G12", 41.13, 76.96, 81.91),
        ("H1", 80.81, 70.68, 48.51), ("H2", 43.71, 69.96, 86.33), ("H3", 55.68, 75.60, 68.72),
        ("H4", 66.74, 76.20, 57.07), ("H5", 87.38, 69.20, 43.42), ("H6", 96.76, 76.80, 26.44),
        ("H7", 43.00, 61.28, 95.72), ("H8", 58.33, 65.28, 76.39), ("H9", 65.64, 67.76, 66.60),
        ("H10", 94.84, 61.92, 43.24), ("H11", 52.84, 63.12, 84.04), ("H12", 74.36, 73.56, 52.09)
    ]
    # --- 1. CARGA DE LABWARE ---
    trash = protocol.load_trash_bin("A3")
    tipracks = protocol.load_labware("opentrons_flex_96_tiprack_200ul", "D3")
    res = protocol.load_labware("custom_4_reservoir_90000ul", "D2")
    res_lapeg = protocol.load_labware("19mlglass_15_tuberack_19000ul", "B2")
    h_s = protocol.load_module('heaterShakerModuleV1', 'C1') 
    plate = h_s.load_labware("corning_96_wellplate_360ul_flat")

    # --- 2. PIPETTE ---
    pipette = protocol.load_instrument("flex_8channel_1000", mount="left", tip_racks=[tipracks])
    pipette.configure_nozzle_layout(style=SINGLE, start="H1")

    # --- 3. SEGURIDAD: CERRAR LATCH ---
    # Esto habilita el movimiento sobre el módulo Heater-Shaker
    h_s.close_labware_latch()

    # --- 4. REACTIVOS ---
    pegda_60 = res_lapeg['C2']
    agua = res['A1']
    lap_05 = res_lapeg['A2']

    vol_max_p200 = 190

    # --- LOGICA DE EJECUCION ---

    # PASO 1: AGUA
    protocol.comment("Distribuyendo Agua...")
    pipette.flow_rate.aspirate = 80
    pipette.flow_rate.dispense = 30
    pipette.flow_rate.blow_out = 60
    
    pipette.pick_up_tip(tipracks['A1'])
    for well, v_peg, v_lap, v_agua in muestras:
        pipette.aspirate(v_agua, agua.bottom(z=3))
        pipette.dispense(v_agua, plate[well].top(z=2))
        dest_pared = plate[well].top(z=-2).move(Point(x=0, y=-2.5, z=0))
        pipette.move_to(dest_pared, speed=10) 
        pipette.blow_out(dest_pared)
        pipette.move_to(plate[well].top(z=10))
        protocol.delay(seconds=1)
    pipette.drop_tip(trash)

    # PASO 2: PEGDA
    protocol.comment("Distribuyendo Pegda...")
    pipette.flow_rate.aspirate = 30
    pipette.flow_rate.dispense = 30
    pipette.flow_rate.blow_out = 40
    
    pipette.pick_up_tip(tipracks['A2'])
    for well, v_peg, v_lap, v_agua in muestras:
        pipette.aspirate(v_peg, pegda_60.bottom(z=8))
        protocol.delay(seconds=3) 
        pipette.move_to(pegda_60.top(z=5),speed=10)
        pipette.dispense(v_peg, plate[well].top(z=2))
        dest_pared = plate[well].top(z=-2).move(Point(x=0, y=-2.5, z=0))
        pipette.move_to(dest_pared, speed=10) 
        pipette.blow_out(dest_pared)
        pipette.move_to(plate[well].top(z=10))
        protocol.delay(seconds=1)
    pipette.drop_tip(trash)

    # PASO 3: LAP
    protocol.comment("Distribuyendo LAP...")
    pipette.flow_rate.aspirate = 80
    pipette.flow_rate.dispense = 40
    
    pipette.pick_up_tip(tipracks['A3'])
    liquido_en_punta = 0
    for well, v_peg, v_lap, v_agua in muestras:
        if liquido_en_punta < (v_lap + 10):
            espacio_libre = vol_max_p200 - liquido_en_punta
            pipette.aspirate(espacio_libre, lap_05.bottom(z=8))
            liquido_en_punta = vol_max_p200
        pipette.dispense(v_lap, plate[well].top(z=2))
        pipette.touch_tip(v_offset=-3, speed=5)#demasiado fuerte lol cambiar
        protocol.delay(seconds=2)
        liquido_en_punta -= v_lap
    pipette.drop_tip(trash)

     # --- 7. FINALIZACIÓN ---
    protocol.comment("Iniciando agitación...")
    h_s.set_and_wait_for_shake_speed(1000)
    protocol.delay(minutes=2)
    h_s.deactivate_shaker()
    h_s.open_labware_latch()
    protocol.comment("Protocolo terminado.")