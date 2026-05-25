from opentrons import protocol_api
from opentrons.protocol_api import SINGLE
from opentrons.types import Point

metadata = {
    'protocolName': 'Sintesis Automatizada de Hidrogeles PVA-PEGDA-LAP (primeras 32-3 rep) optimizado (LHS Design)',
    'author': 'NicoPeña',
    'description': 'Preparacion de 96 muestras con gradientes de PEGDA, PVA y LAP usando Latin Hypercube Sampling.',
}

requirements = {"robotType": "Flex", "apiLevel": "2.21"}

def run(protocol: protocol_api.ProtocolContext):
    muestras = [
        ("A1", 91.00, 25.00), ("A2", 32.50, 27.50), ("A3", 89.50, 22.50), 
        ("A4", 37.50, 42.50), ("A5", 92.50, 27.50), ("A6", 44.50, 27.50), 
        ("A7", 80.50, 67.50), ("A8", 56.00, 60.00), ("A9", 146.00, 30.00), 
        ("A10", 46.00, 30.00), ("A11", 21.00, 35.00), ("A12", 63.00, 45.00), 
        ("B1", 85.00, 35.00), ("B2", 43.50, 32.50), ("B3", 108.00, 40.00), 
        ("B4", 18.50, 37.50), ("B5", 81.50, 62.50), ("B6", 59.00, 25.00), 
        ("B7", 44.50, 27.50), ("B8", 21.00, 35.00), ("B9", 21.00, 35.00), 
        ("B10", 36.50, 47.50), ("B11", 76.50, 27.50), ("B12", 108.00, 40.00), 
        ("C1", 121.50, 22.50), ("C2", 31.67, 55.00), ("C3", 28.00, 40.00), 
        ("C4", 44.50, 27.50), ("C5", 83.00, 25.00), ("C6", 91.50, 52.50), 
        ("C7", 68.00, 60.00), ("C8", 91.00, 25.00), ("C9", 31.67, 55.00), 
        ("C10", 24.17, 62.50), ("C11", 18.50, 37.50), ("C12", 46.00, 30.00), 
        ("D1", 32.50, 27.50), ("D2", 146.00, 30.00), ("D3", 83.00, 25.00), 
        ("D4", 91.50, 52.50), ("D5", 76.50, 27.50), ("D6", 36.50, 47.50), 
        ("D7", 45.00, 35.00), ("D8", 92.50, 27.50), ("D9", 89.50, 22.50), 
        ("D10", 24.17, 62.50), ("D11", 28.00, 40.00), ("D12", 32.50, 27.50), 
        ("E1", 63.00, 45.00), ("E2", 89.50, 22.50), ("E3", 39.00, 45.00), 
        ("E4", 89.50, 22.50), ("E5", 43.50, 32.50), ("E6", 81.50, 62.50), 
        ("E7", 28.00, 40.00), ("E8", 108.00, 40.00), ("E9", 18.50, 37.50), 
        ("E10", 43.50, 32.50), ("E11", 56.00, 60.00), ("E12", 68.00, 60.00), 
        ("F1", 146.00, 30.00), ("F2", 59.00, 25.00), ("F3", 80.50, 67.50), 
        ("F4", 91.50, 52.50), ("F5", 45.00, 35.00), ("F6", 24.17, 62.50), 
        ("F7", 44.00, 40.00), ("F8", 76.50, 27.50), ("F9", 121.50, 22.50), 
        ("F10", 81.50, 62.50), ("F11", 45.00, 35.00), ("F12", 19.33, 50.00), 
        ("G1", 31.67, 55.00), ("G2", 83.00, 25.00), ("G3", 37.50, 42.50), 
        ("G4", 39.00, 45.00), ("G5", 19.33, 50.00), ("G6", 39.00, 45.00), 
        ("G7", 46.00, 30.00), ("G8", 89.50, 22.50), ("G9", 85.00, 35.00), 
        ("G10", 63.00, 45.00), ("G11", 56.00, 60.00), ("G12", 89.50, 22.50), 
        ("H1", 91.00, 25.00), ("H2", 36.50, 47.50), ("H3", 80.50, 67.50), 
        ("H4", 92.50, 27.50), ("H5", 68.00, 60.00), ("H6", 59.00, 25.00), 
        ("H7", 19.33, 50.00), ("H8", 44.00, 40.00), ("H9", 121.50, 22.50), 
        ("H10", 37.50, 42.50), ("H11", 44.00, 40.00), ("H12", 85.00, 35.00)
    ]
        
    m_pva_10 = [
        ("A1", 60.00), ("A2", 80.00), ("A3", 60.00), ("A4", 60.00), ("A5", 20.00), 
        ("A6", 60.00), ("A7", 20.00), ("A8", 40.00), ("A9", 0.00), ("A10", 100.00), 
        ("A11", 100.00), ("A12", 60.00), ("B1", 40.00), ("B2", 100.00), ("B3", 0.00), 
        ("B4", 100.00), ("B5", 20.00), ("B6", 80.00), ("B7", 60.00), ("B8", 100.00), 
        ("B9", 100.00), ("B10", 60.00), ("B11", 20.00), ("B12", 0.00), ("C1", 20.00), 
        ("C4", 60.00), ("C5", 60.00), ("C6", 20.00), ("C7", 0.00), ("C8", 60.00), 
        ("C11", 100.00), ("C12", 100.00), ("D1", 80.00), ("D2", 0.00), ("D3", 60.00), 
        ("D4", 20.00), ("D5", 20.00), ("D6", 60.00), ("D7", 80.00), ("D8", 20.00), 
        ("D9", 40.00), ("D12", 80.00),("E1", 60.00), ("E2", 60.00), ("E3", 60.00), 
        ("E4", 40.00), ("E5", 100.00), ("E6", 20.00), ("E8", 0.00), ("E9", 100.00), 
        ("E10", 100.00), ("E11", 40.00), ("E12", 0.00), ("F1", 0.00), ("F2", 80.00), 
        ("F3", 20.00), ("F4", 20.00), ("F5", 80.00),("F8", 20.00), ("F9", 20.00), 
        ("F10", 20.00),("F11", 80.00), ("G2", 60.00), ("G3", 60.00), ("G4", 60.00),
        ("G6", 60.00), ("G7", 100.00), ("G8", 40.00), ("G9", 40.00), ("G10", 60.00), 
        ("G11", 40.00), ("G12", 60.00), ("H1", 60.00), ("H2", 60.00), ("H3", 20.00), 
        ("H4", 20.00), ("H5", 0.00), ("H6", 80.00), ("H9", 20.00), ("H10", 60.00), ("H12", 40.00) 
    ]
        
    m_pva_15 = [
        ("C2", 93.33), ("C3", 80.00), ("C9", 93.33), ("C10", 53.33), ("D10", 53.33), 
        ("D11", 80.00), ("E7", 80.00), ("F6", 53.33), ("F7", 80.00),("F12", 106.67), 
        ("G1", 93.33), ("G5", 106.67), ("H7", 106.67), ("H8", 80.00), ("H11", 80.00)
    ]
    
    m_lap_05 = [
        ("A1", 24.00), ("A2", 60.00), ("A3", 28.00), ("A4", 60.00), ("A5", 60.00), 
        ("A6", 68.00), ("A7", 32.00), ("A8", 44.00), ("A9", 24.00), ("A10", 24.00), 
        ("A11", 44.00), ("A12", 32.00), ("B1", 40.00), ("B2", 24.00), ("B3", 52.00), 
        ("B4", 44.00), ("B5", 36.00), ("B6", 36.00), ("B7", 68.00), ("B8", 44.00), 
        ("B9", 44.00), ("B10", 56.00), ("B11", 76.00), ("B12", 52.00), ("C1", 36.00), 
        ("C2", 20.00), ("C3", 52.00), ("C4", 68.00), ("C5", 32.00), ("C6", 36.00), 
        ("C7", 72.00), ("C8", 24.00), ("C9", 20.00), ("C10", 60.00), ("C11", 44.00), 
        ("C12", 24.00), ("D1", 60.00), ("D2", 24.00), ("D3", 32.00), ("D4", 36.00), 
        ("D5", 76.00), ("D6", 56.00), ("D7", 40.00), ("D8", 60.00), ("D9", 48.00), 
        ("D10", 60.00), ("D11", 52.00), ("D12", 60.00), ("E1", 32.00), ("E2", 28.00), 
        ("E3", 56.00), ("E4", 48.00), ("E5", 24.00), ("E6", 36.00), ("E7", 52.00), 
        ("E8", 52.00), ("E9", 44.00), ("E10", 24.00), ("E11", 44.00), ("E12", 72.00), 
        ("F1", 24.00), ("F2", 36.00), ("F3", 32.00), ("F4", 36.00), ("F5", 40.00), 
        ("F6", 60.00), ("F8", 76.00), ("F9", 36.00), ("F10", 36.00), ("F11", 40.00), 
        ("G1", 20.00), ("G2", 32.00), ("G3", 60.00), ("G4", 56.00), ("G6", 56.00), 
        ("G7", 24.00), ("G8", 48.00), ("G9", 40.00), ("G10", 32.00), ("G11", 44.00), 
        ("G12", 28.00), ("H1", 24.00), ("H2", 56.00), ("H3", 32.00), ("H4", 60.00), 
        ("H5", 72.00), ("H6", 36.00), ("H9", 36.00), ("H10", 60.00), ("H12", 40.00)
    ]
        
    m_lap_1 = [
        ("F7", 36.00), ("F12", 24.00), ("G5", 24.00), 
        ("H7", 24.00), ("H8", 36.00), ("H11", 36.00)
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
        pipette.aspirate(v_pva, pva_10.bottom(z=9))
        protocol.delay(seconds=5) 
        pipette.move_to(pva_10.top(z=5),speed=5)
        pipette.dispense(v_pva, plate[well].top(z=2))
        protocol.delay(seconds=2) 
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
        pipette.aspirate(v_pva, pva_15.bottom(z=9))
        protocol.delay(seconds=5) 
        pipette.move_to(pva_15.top(z=5),speed=5)
        pipette.dispense(v_pva, plate[well].top(z=2))
        protocol.delay(seconds=5)
        dest_pared = plate[well].top(z=-2).move(Point(x=0, y=-2.5, z=0))
        pipette.move_to(dest_pared, speed=10) 
        pipette.blow_out(dest_pared)
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
        pipette.aspirate(v_peg, pegda_80.bottom(z=9))
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
            pipette.aspirate(espacio_libre, lap_05.bottom(z=9))
            liquido_en_punta = vol_max_p200
        pipette.dispense(v_lap, plate[well].top(z=2))
        pipette.touch_tip(v_offset=-3, speed=5)
        protocol.delay(seconds=2)
        liquido_en_punta -= v_lap
    pipette.drop_tip(trash)
    
    #PASO 6: LAP 1%
    protocol.comment("Distribuyendo LAP 0.5%...")
    pipette.flow_rate.aspirate = 80
    pipette.flow_rate.dispense = 40
    
    pipette.pick_up_tip(tipracks['A6'])
    liquido_en_punta = 0
    for well, v_lap in m_lap_1:
        if liquido_en_punta < (v_lap + 10):
            espacio_libre = vol_max_p200 - liquido_en_punta
            pipette.aspirate(espacio_libre, lap_1.bottom(z=9))
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