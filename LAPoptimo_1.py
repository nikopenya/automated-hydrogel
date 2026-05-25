from opentrons import protocol_api
from opentrons.protocol_api import SINGLE
from opentrons.types import Point

# Metadatos del protocolo
metadata = {
    'protocolName': 'Sintesis Automatizada de Hidrogeles PEGDA-LAP (primeras 32-3 rep) optimizado (LHS Design)',
    'author': 'NicoPeña',
    'description': 'Preparacion de 96 muestras con gradientes de PEGDA y LAP usando Latin Hypercube Sampling.',
}

requirements = {"robotType": "Flex", "apiLevel": "2.21"}

def run(protocol: protocol_api.ProtocolContext):
    muestras = [
    ("A1", 80.51, 20.16, 99.32), ("A2", 80.51, 20.16, 99.32), ("A3", 80.51, 20.16, 99.32),
    ("A4", 41.87, 21.22, 136.91), ("A5", 41.87, 21.22, 136.91), ("A6", 41.87, 21.22, 136.91),
    ("A7", 69.15, 21.47, 109.38), ("A8", 69.15, 21.47, 109.38), ("A9", 69.15, 21.47, 109.38),
    ("A10", 95.57, 21.90, 82.53), ("A11", 95.57, 21.90, 82.53), ("A12", 95.57, 21.90, 82.53),
    ("B1", 52.00, 22.92, 125.09), ("B2", 52.00, 22.92, 125.09), ("B3", 52.00, 22.92, 125.09),
    ("B4", 62.65, 23.31, 114.05), ("B5", 62.65, 23.31, 114.05), ("B6", 62.65, 23.31, 114.05),
    ("B7", 86.10, 24.07, 89.83), ("B8", 86.10, 24.07, 89.83), ("B9", 86.10, 24.07, 89.83),
    ("B10", 36.80, 24.48, 138.71), ("B11", 36.80, 24.48, 138.71), ("B12", 36.80, 24.48, 138.71),
    ("C1", 75.14, 25.57, 99.29), ("C2", 75.14, 25.57, 99.29), ("C3", 75.14, 25.57, 99.29),
    ("C4", 55.43, 25.96, 118.61), ("C5", 55.43, 25.96, 118.61), ("C6", 55.43, 25.96, 118.61),
    ("C7", 93.06, 26.31, 80.63), ("C8", 93.06, 26.31, 80.63), ("C9", 93.06, 26.31, 80.63),
    ("C10", 71.98, 27.22, 100.80), ("C11", 71.98, 27.22, 100.80), ("C12", 71.98, 27.22, 100.80),
    ("D1", 39.15, 27.78, 133.06), ("D2", 39.15, 27.78, 133.06), ("D3", 39.15, 27.78, 133.06),
    ("D4", 59.99, 28.19, 111.83), ("D5", 59.99, 28.19, 111.83), ("D6", 59.99, 28.19, 111.83),
    ("D7", 89.12, 29.22, 81.66), ("D8", 89.12, 29.22, 81.66), ("D9", 89.12, 29.22, 81.66),
    ("D10", 48.03, 29.89, 122.08), ("D11", 48.03, 29.89, 122.08), ("D12", 48.03, 29.89, 122.08),
    ("E1", 77.98, 30.14, 91.88), ("E2", 77.98, 30.14, 91.88), ("E3", 77.98, 30.14, 91.88),
    ("E4", 50.69, 31.09, 118.21), ("E5", 50.69, 31.09, 118.21), ("E6", 50.69, 31.09, 118.21),
    ("E7", 81.47, 31.68, 86.84), ("E8", 81.47, 31.68, 86.84), ("E9", 81.47, 31.68, 86.84),
    ("E10", 98.94, 32.49, 68.57), ("E11", 98.94, 32.49, 68.57), ("E12", 98.94, 32.49, 68.57),
    ("F1", 45.38, 32.81, 121.81), ("F2", 45.38, 32.81, 121.81), ("F3", 45.38, 32.81, 121.81),
    ("F4", 66.48, 33.14, 100.38), ("F5", 66.48, 33.14, 100.38), ("F6", 66.48, 33.14, 100.38),
    ("F7", 64.83, 34.10, 101.07), ("F8", 64.83, 34.10, 101.07), ("F9", 64.83, 34.10, 101.07),
    ("F10", 34.68, 34.47, 130.85), ("F11", 34.68, 34.47, 130.85), ("F12", 34.68, 34.47, 130.85),
    ("G1", 87.66, 35.10, 77.24), ("G2", 87.66, 35.10, 77.24), ("G3", 87.66, 35.10, 77.24),
    ("G4", 56.97, 36.02, 107.01), ("G5", 56.97, 36.02, 107.01), ("G6", 56.97, 36.02, 107.01),
    ("G7", 84.05, 36.32, 79.63), ("G8", 84.05, 36.32, 79.63), ("G9", 84.05, 36.32, 79.63),
    ("G10", 44.08, 37.01, 118.91), ("G11", 44.08, 37.01, 118.91), ("G12", 44.08, 37.01, 118.91),
    ("H1", 67.82, 38.01, 94.17), ("H2", 67.82, 38.01, 94.17), ("H3", 67.82, 38.01, 94.17),
    ("H4", 91.61, 38.22, 70.17), ("H5", 91.61, 38.22, 70.17), ("H6", 91.61, 38.22, 70.17),
    ("H7", 58.57, 38.78, 102.65), ("H8", 58.57, 38.78, 102.65), ("H9", 58.57, 38.78, 102.65),
    ("H10", 48.91, 39.66, 111.43), ("H11", 48.91, 39.66, 111.43), ("H12", 48.91, 39.66, 111.43)
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