from opentrons import protocol_api
from opentrons.protocol_api import SINGLE
from opentrons.types import Point

# Metadatos del protocolo
metadata = {
    'protocolName': 'Sintesis Automatizada de Hidrogeles PEGDA-LAP (segundas 32-3 rep) optimizado (LHS Design)',
    'author': 'NicoPeña',
    'description': 'Preparacion de 96 muestras con gradientes de PEGDA y LAP usando Latin Hypercube Sampling.',
}

requirements = {"robotType": "Flex", "apiLevel": "2.21"}


def run(protocol: protocol_api.ProtocolContext):


    muestras = [
        ("A1", 56.53, 53.00, 90.47), ("A2", 76.28, 58.76, 64.96), ("A3", 83.68, 51.32, 65.00),
        ("A4", 82.70, 47.32, 69.98), ("A5", 44.50, 42.68, 112.83), ("A6", 49.57, 56.44, 93.99),
        ("A7", 97.77, 40.04, 62.19), ("A8", 53.76, 59.80, 86.44), ("A9", 71.04, 58.40, 70.56),
        ("A10", 37.89, 40.76, 121.35), ("A11", 92.32, 54.08, 53.60), ("A12", 52.32, 49.60, 98.08),
        ("B1", 40.41, 45.60, 113.99), ("B2", 86.32, 56.04, 57.64), ("B3", 63.65, 47.72, 88.63),
        ("B4", 96.08, 43.64, 60.28), ("B5", 33.87, 57.92, 108.21), ("B6", 76.90, 41.76, 81.34),
        ("B7", 46.75, 51.20, 102.05), ("B8", 61.08, 55.28, 83.64), ("B9", 93.00, 57.16, 49.84),
        ("B10", 70.32, 52.20, 77.48), ("B11", 34.95, 49.28, 115.77), ("B12", 79.28, 48.32, 72.40),
        ("C1", 98.27, 50.24, 51.49), ("C2", 89.66, 45.88, 64.46), ("C3", 54.45, 46.68, 98.87),
        ("C4", 74.22, 44.40, 81.38), ("C5", 62.17, 44.01, 93.79), ("C6", 68.08, 54.76, 77.16),
        ("C7", 39.72, 53.44, 106.84), ("C8", 73.33, 42.12, 84.55), ("C9", 53.76, 59.80, 86.44),
        ("C10", 83.68, 51.32, 65.00), ("C11", 44.50, 42.68, 112.83), ("C12", 97.77, 40.04, 62.19),
        ("D1", 76.28, 58.76, 64.96), ("D2", 82.70, 47.32, 69.98), ("D3", 49.57, 56.44, 93.99),
        ("D4", 56.53, 53.00, 90.47), ("D5", 71.04, 58.40, 70.56), ("D6", 37.89, 40.76, 121.35),
        ("D7", 92.32, 54.08, 53.60), ("D8", 52.32, 49.60, 98.08), ("D9", 40.41, 45.60, 113.99),
        ("D10", 86.32, 56.04, 57.64), ("D11", 63.65, 47.72, 88.63), ("D12", 96.08, 43.64, 60.28),
        ("E1", 33.87, 57.92, 108.21), ("E2", 76.90, 41.76, 81.34), ("E3", 46.75, 51.20, 102.05),
        ("E4", 61.08, 55.28, 83.64), ("E5", 93.00, 57.16, 49.84), ("E6", 70.32, 52.20, 77.48),
        ("E7", 34.95, 49.28, 115.77), ("E8", 79.28, 48.32, 72.40), ("E9", 98.27, 50.24, 51.49),
        ("E10", 89.66, 45.88, 64.46), ("E11", 54.45, 46.68, 98.87), ("E12", 74.22, 44.40, 81.38),
        ("F1", 62.17, 44.01, 93.79), ("F2", 68.08, 54.76, 77.16), ("F3", 39.72, 53.44, 106.84),
        ("F4", 73.33, 42.12, 84.55), ("F5", 53.76, 59.80, 86.44), ("F6", 83.68, 51.32, 65.00),
        ("F7", 44.50, 42.68, 112.83), ("F8", 97.77, 40.04, 62.19), ("F9", 76.28, 58.76, 64.96),
        ("F10", 82.70, 47.32, 69.98), ("F11", 49.57, 56.44, 93.99), ("F12", 56.53, 53.00, 90.47),
        ("G1", 71.04, 58.40, 70.56), ("G2", 37.89, 40.76, 121.35), ("G3", 92.32, 54.08, 53.60),
        ("G4", 52.32, 49.60, 98.08), ("G5", 40.41, 45.60, 113.99), ("G6", 86.32, 56.04, 57.64),
        ("G7", 63.65, 47.72, 88.63), ("G8", 96.08, 43.64, 60.28), ("G9", 33.87, 57.92, 108.21),
        ("G10", 76.90, 41.76, 81.34), ("G11", 46.75, 51.20, 102.05), ("G12", 61.08, 55.28, 83.64),
        ("H1", 93.00, 57.16, 49.84), ("H2", 70.32, 52.20, 77.48), ("H3", 34.95, 49.28, 115.77),
        ("H4", 79.28, 48.32, 72.40), ("H5", 98.27, 50.24, 51.49), ("H6", 89.66, 45.88, 64.46),
        ("H7", 54.45, 46.68, 98.87), ("H8", 74.22, 44.40, 81.38), ("H9", 62.17, 44.01, 93.79),
        ("H10", 68.08, 54.76, 77.16), ("H11", 39.72, 53.44, 106.84), ("H12", 73.33, 42.12, 84.55)
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