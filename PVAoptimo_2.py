from opentrons import protocol_api
from opentrons.protocol_api import SINGLE
from opentrons.types import Point

metadata = {
    'protocolName': 'Sintesis Automatizada de Hidrogeles PVA-PEGDA-LAP (segundas 32-3 rep) optimizado (LHS Design)',
    'author': 'NicoPeña',
    'description': 'Preparacion de 96 muestras con gradientes de PEGDA, PVA y LAP usando Latin Hypercube Sampling.',
}

requirements = {"robotType": "Flex", "apiLevel": "2.21"}

def run(protocol: protocol_api.ProtocolContext):
    
    muestras = [
        ("A1", 39.33, 50.0), ("A2", 133.5, 22.5), ("A3", 121.0, 55.0), ("A4", 93.5, 22.5), ("A5", 70.5, 57.5), 
        ("A6", 76.5, 27.5), ("A7", 20.0, 40.0), ("A8", 29.5, 62.5), ("A9", 29.5, 62.5), ("A10", 28.33, 45.0), 
        ("A11", 20.33, 55.0), ("A12", 133.5, 22.5), ("B1", 93.0, 55.0), ("B2", 72.0, 60.0), ("B3", 20.0, 40.0), 
        ("B4", 23.17, 57.5), ("B5", 31.5, 72.5), ("B6", 44.5, 47.5), ("B7", 83.5, 52.5), ("B8", 121.0, 55.0), 
        ("B9", 28.33, 45.0), ("B10", 79.5, 32.5), ("B11", 28.67, 50.0), ("B12", 95.0, 65.0), ("C1", 121.0, 55.0), 
        ("C2", 28.67, 50.0), ("C3", 57.0, 35.0), ("C4", 44.5, 47.5), ("C5", 28.67, 50.0), ("C6", 28.67, 50.0), 
        ("C7", 83.5, 52.5), ("C8", 44.5, 47.5), ("C9", 54.17, 52.5), ("C10", 54.17, 52.5), ("C11", 20.0, 40.0), 
        ("C12", 56.5, 27.5), ("D1", 37.17, 37.5), ("D2", 76.5, 27.5), ("D3", 71.5, 32.5), ("D4", 76.5, 27.5), 
        ("D5", 57.0, 35.0), ("D6", 75.5, 32.5), ("D7", 20.33, 55.0), ("D8", 76.5, 27.5), ("D9", 54.17, 52.5), 
        ("D10", 56.5, 27.5), ("D11", 83.5, 52.5), ("D12", 28.33, 45.0), ("E1", 76.5, 27.5), ("E2", 71.5, 32.5), 
        ("E3", 43.5, 52.5), ("E4", 37.17, 37.5), ("E5", 95.0, 65.0), ("E6", 70.5, 57.5), ("E7", 79.5, 32.5), 
        ("E8", 73.0, 35.0), ("E9", 33.5, 62.5), ("E10", 70.5, 57.5), ("E11", 43.5, 52.5), ("E12", 57.0, 35.0), 
        ("F1", 39.33, 50.0), ("F2", 95.0, 65.0), ("F3", 13.83, 47.5), ("F4", 31.5, 72.5), ("F5", 72.0, 60.0), 
        ("F6", 132.5, 27.5), ("F7", 72.0, 60.0), ("F8", 75.5, 32.5), ("F9", 56.5, 27.5), ("F10", 33.5, 62.5), 
        ("F11", 33.5, 62.5), ("F12", 23.17, 57.5), ("G1", 93.5, 22.5), ("G2", 93.5, 22.5), ("G3", 73.0, 35.0), 
        ("G4", 28.67, 50.0), ("G5", 23.17, 57.5), ("G6", 93.0, 55.0), ("G7", 93.0, 55.0), ("G8", 76.5, 27.5), 
        ("G9", 43.5, 52.5), ("G10", 132.5, 27.5), ("G11", 37.17, 37.5), ("G12", 73.0, 35.0), ("H1", 79.5, 32.5), 
        ("H2", 13.83, 47.5), ("H3", 29.5, 62.5), ("H4", 31.5, 72.5), ("H5", 13.83, 47.5), ("H6", 28.67, 50.0), 
        ("H7", 132.5, 27.5), ("H8", 39.33, 50.0), ("H9", 71.5, 32.5), ("H10", 75.5, 32.5), ("H11", 20.33, 55.0), 
        ("H12", 133.5, 22.5)
    ]
        
    m_pva_10 = [
        ("A2", 20.0), ("A3", 0.0), ("A4", 20.0), ("A5", 20.0), ("A6", 20.0), ("A7", 60.0), ("A12", 20.0), 
        ("B1", 0.0), ("B2", 40.0), ("B3", 60.0), ("B5", 20.0), ("B7", 0.0), ("B8", 0.0), ("B10", 60.0), 
        ("B12", 0.0), ("C1", 0.0), ("C3", 60.0), ("C7", 0.0), ("C11", 60.0), ("C12", 60.0), ("D2", 20.0), 
        ("D3", 60.0), ("D4", 20.0), ("D5", 60.0), ("D6", 20.0), ("D8", 20.0), ("D10", 60.0), ("D11", 0.0), 
        ("E1", 20.0), ("E2", 60.0), ("E3", 40.0), ("E5", 0.0), ("E6", 20.0), ("E7", 60.0), ("E8", 60.0), 
        ("E9", 40.0), ("E10", 20.0), ("E11", 40.0), ("E12", 60.0), ("F2", 0.0), ("F4", 20.0), ("F5", 40.0), 
        ("F6", 0.0), ("F7", 40.0), ("F8", 20.0), ("F9", 60.0), ("F10", 40.0), ("F11", 40.0), ("G1", 20.0), 
        ("G2", 20.0), ("G3", 60.0), ("G6", 0.0), ("G7", 0.0), ("G8", 20.0), ("G9", 40.0), ("G10", 0.0), 
        ("G12", 60.0), ("H1", 60.0), ("H4", 20.0), ("H7", 0.0), ("H9", 60.0), ("H10", 20.0), ("H12", 20.0)
    ]
    
    m_pva_15 = [
        ("A1", 66.67), ("A8", 40.0), ("A9", 40.0), ("A10", 66.67), ("A11", 106.67), ("B4", 93.33), ("B6", 80.0), 
        ("B9", 66.67), ("B11", 93.33), ("C2", 53.33), ("C4", 80.0), ("C5", 53.33), ("C6", 93.33), ("C8", 80.0), 
        ("C9", 53.33), ("C10", 53.33), ("D1", 53.33), ("D7", 106.67), ("D9", 53.33), ("D12", 66.67), ("E4", 53.33), 
        ("F1", 66.67), ("F3", 106.67), ("F12", 93.33), ("G4", 93.33), ("G5", 93.33), ("G11", 53.33), ("H2", 106.67), 
        ("H3", 40.0), ("H5", 106.67), ("H6", 53.33), ("H8", 66.67), ("H11", 106.67)
    ]
    
    m_lap_05 = [
        ("A1", 44.0), ("A2", 24.0), ("A3", 24.0), ("A4", 64.0), ("A5", 52.0), ("A6", 76.0), ("A7", 80.0), 
        ("A8", 68.0), ("A9", 68.0), ("A10", 60.0), ("A12", 24.0), ("B1", 52.0), ("B2", 28.0), ("B3", 80.0), 
        ("B5", 76.0), ("B6", 28.0), ("B7", 64.0), ("B8", 24.0), ("B9", 60.0), ("B10", 28.0), ("B12", 40.0), 
        ("C1", 24.0), ("C2", 68.0), ("C3", 48.0), ("C4", 28.0), ("C5", 68.0), ("C7", 64.0), ("C8", 28.0), 
        ("C11", 80.0), ("C12", 56.0), ("D1", 72.0), ("D2", 76.0), ("D3", 36.0), ("D4", 76.0), ("D5", 48.0), 
        ("D6", 72.0), ("D8", 76.0), ("D10", 56.0), ("D11", 64.0), ("D12", 60.0), ("E1", 76.0), ("E2", 36.0), 
        ("E3", 64.0), ("E4", 72.0), ("E5", 40.0), ("E6", 52.0), ("E7", 28.0), ("E8", 32.0), ("E9", 64.0), 
        ("E10", 52.0), ("E11", 64.0), ("E12", 48.0), ("F1", 44.0), ("F2", 40.0), ("F4", 76.0), ("F5", 28.0), 
        ("F6", 40.0), ("F7", 28.0), ("F8", 72.0), ("F9", 56.0), ("F10", 64.0), ("F11", 64.0), ("G1", 64.0), 
        ("G2", 64.0), ("G3", 32.0), ("G6", 52.0), ("G7", 52.0), ("G8", 76.0), ("G9", 64.0), ("G10", 40.0), 
        ("G11", 72.0), ("G12", 32.0), ("H1", 28.0), ("H3", 68.0), ("H4", 76.0), ("H6", 68.0), ("H7", 40.0), 
        ("H8", 44.0), ("H9", 36.0), ("H10", 72.0), ("H12", 24.0)
    ]
    
    m_lap_1 = [
        ("A11", 18.0), ("B4", 26.0), ("B11", 28.0), ("C6", 28.0), ("C9", 40.0), ("C10", 40.0), ("D7", 18.0), 
        ("D9", 40.0), ("F3", 32.0), ("F12", 26.0), ("G4", 28.0), ("G5", 26.0), ("H2", 32.0), ("H5", 32.0), 
        ("H11", 18.0)
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
    h_s.close_labware_latch()

    # --- 4. REACTIVOS ---
    pegda_80 = res_lapeg['C1']
    agua = res['A1']
    pva_10 = res_lapeg['B1']
    pva_15 = res_lapeg['B2']
    lap_05 = res_lapeg['A1']
    lap_1 = res_lapeg['A2']

    vol_max_p200 = 190

    #PASO 1: AGUA
    protocol.comment("Distribuyendo Agua...")
    pipette.flow_rate.aspirate = 80
    pipette.flow_rate.dispense = 30
    pipette.flow_rate.blow_out = 60
    
    pipette.pick_up_tip(tipracks['A1'])
    for well, v_agua, v_peg in muestras:
        pipette.aspirate(v_agua, agua.bottom(z=3))
        pipette.dispense(v_agua, plate[well].top(z=2))
        dest_pared = plate[well].top(z=-2).move(Point(x=0, y=-2.5, z=0))
        pipette.move_to(dest_pared, speed=10) 
        pipette.blow_out(dest_pared)
        pipette.move_to(plate[well].top(z=10))
        protocol.delay(seconds=1)
    pipette.drop_tip(trash)

    #PASO 2: PVA 10%
    protocol.comment("Distribuyendo PVA 10%...")
    pipette.flow_rate.aspirate = 10
    pipette.flow_rate.dispense = 10
    pipette.flow_rate.blow_out = 30
    pipette.pick_up_tip(tipracks['A2'])
    for well, v_pva in m_pva_10:
        pipette.aspirate(v_pva, pva_10.bottom(z=8))
        protocol.delay(seconds=5) 
        pipette.move_to(pva_10.top(z=5),speed=5)
        pipette.dispense(v_pva, plate[well].top(z=2))
        protocol.delay(seconds=5) 
        dest_pared = plate[well].top(z=-2).move(Point(x=0, y=-2.5, z=0))
        pipette.move_to(dest_pared, speed=10) 
        pipette.blow_out(dest_pared)
        pipette.move_to(plate[well].top(z=10))
        protocol.delay(seconds=1)
    pipette.drop_tip(trash)

    #PASO 3: PVA 15%
    protocol.comment("Distribuyendo PVA 15%...")
    pipette.flow_rate.aspirate = 5
    pipette.flow_rate.dispense = 5
    pipette.flow_rate.blow_out = 20
    pipette.pick_up_tip(tipracks['A3'])
    for well, v_pva in m_pva_15:
        pipette.aspirate(v_pva, pva_15.bottom(z=8))
        protocol.delay(seconds=5) 
        pipette.move_to(pva_15.top(z=5),speed=5)
        pipette.dispense(v_pva, plate[well].top(z=2))
        protocol.delay(seconds=5)
        dest_pared = plate[well].top(z=-2).move(Point(x=0, y=-2.5, z=0))
        pipette.move_to(dest_pared, speed=10) 
        pipette.blow_out(dest_pared)
        protocol.delay(seconds=3)
        pipette.move_to(plate[well].top(z=10))
        protocol.delay(seconds=1)
    pipette.drop_tip(trash)

    #PASO 4: PEGDA
    protocol.comment("Distribuyendo Pegda...")
    pipette.flow_rate.aspirate = 30
    pipette.flow_rate.dispense = 30
    pipette.flow_rate.blow_out = 40
    pipette.pick_up_tip(tipracks['A4'])
    for well, v_agua, v_peg in muestras:
        pipette.aspirate(v_peg, pegda_80.bottom(z=8))
        protocol.delay(seconds=3) 
        pipette.move_to(pegda_80.top(z=5),speed=10)
        pipette.dispense(v_peg, plate[well].top(z=2))
        dest_pared = plate[well].top(z=-2).move(Point(x=0, y=-2.5, z=0))
        pipette.move_to(dest_pared, speed=10) 
        pipette.blow_out(dest_pared)
        pipette.move_to(plate[well].top(z=10))
        protocol.delay(seconds=1)
    pipette.drop_tip(trash)

    #PASO 5: LAP 0.5%
    protocol.comment("Distribuyendo LAP 0.5%...")
    pipette.flow_rate.aspirate = 80
    pipette.flow_rate.dispense = 40
    
    pipette.pick_up_tip(tipracks['A5'])
    liquido_en_punta = 0
    for well, v_lap in m_lap_05:
        if liquido_en_punta < (v_lap + 10):
            espacio_libre = vol_max_p200 - liquido_en_punta
            pipette.aspirate(espacio_libre, lap_05.bottom(z=8))
            liquido_en_punta = vol_max_p200
        pipette.dispense(v_lap, plate[well].top(z=2))
        pipette.touch_tip(v_offset=-3, speed=5)
        protocol.delay(seconds=2)
        liquido_en_punta -= v_lap
    pipette.drop_tip(trash)
    
        # PASO 6: LAP 1%
    protocol.comment("Distribuyendo LAP 0.5%...")
    pipette.flow_rate.aspirate = 80
    pipette.flow_rate.dispense = 40
    
    pipette.pick_up_tip(tipracks['A6'])
    liquido_en_punta = 0
    for well, v_lap in m_lap_1:
        if liquido_en_punta < (v_lap + 10):
            espacio_libre = vol_max_p200 - liquido_en_punta
            pipette.aspirate(espacio_libre, lap_1.bottom(z=8))
            liquido_en_punta = vol_max_p200
        pipette.dispense(v_lap, plate[well].top(z=2))
        pipette.touch_tip(v_offset=-3, speed=5)
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