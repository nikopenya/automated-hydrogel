"""
This is a script which can be used to make measurements if samples are in standard 96 well SBS micro plate. This is the
main measurement taking script.

Parts of this code are adapted from the godirect-examples github repository found here:

https://github.com/VernierST/godirect-examples/tree/main
Copyright (c) 2018, Vernier Software and Technology, @VernierST

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
may be used to endorse or promote products derived from this software without
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

This acknowledgement does not constitute an endorsement or promotion


Part of this code are also adapted from the python_to_GRBL github repository found here:

https://github.com/Sam-Freitas/python_to_GRBL/tree/main
Copyright (c) 2016 Florent Gallaire <fgallaire@gmail.com>
Copyright (c) 2014 Gabriele Cirulli

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

import serial
import time
from threading import Event
from godirect import GoDirect
import statistics
import csv
import logging
import numpy as np
import math
import warnings
import pandas as pd
import os

import matplotlib.pyplot as pyplot

warnings.filterwarnings("ignore", category=RuntimeWarning)
from scipy.optimize import curve_fit
logging.basicConfig()

# --- CONFIGURACIÓN DE CONEXIÓN Y RUTAS ---
BAUD_RATE = 115200
GRBL_port_path = "COM6"  # Puerto de tu CNC
x_init = 19.81
y_init = 48.4
offset = 9

# Ruta corregida con 'r' para evitar errores de unicode (OneDrive/Nicolas)
ruta_trabajo = r"C:\Users\nicolas.pena\OneDrive - FUNDACIÓN IMDEA MATERIALES\Desktop\PenDrive CNC\ASMI"
if not os.path.exists(ruta_trabajo):
    os.makedirs(ruta_trabajo)
os.chdir(ruta_trabajo) # Establece la carpeta de trabajo automáticamente

files = os.listdir(ruta_trabajo)
godirect = GoDirect(use_ble=True, use_usb=True)
device = godirect.get_device(threshold=-100)
lowest = -20
height_offset = 7.5


def remove_comment(string):
    if (string.find(';') == -1):
        return string
    else:
        return string[:string.index(';')]


def remove_eol_chars(string):
    # removed \n or traling spaces
    return string.strip()


def send_wake_up(ser):
    # Wake up
    # Hit enter a few times to wake the Printrbot
    ser.write(str.encode("\r\n\r\n"))
    time.sleep(2)  # Wait for Printrbot to initialize
    ser.flushInput()  # Flush startup text in serial input


def wait_for_movement_completion(ser, cleaned_line):
    Event().wait(1)

    if cleaned_line != '$X' or '$$':

        idle_counter = 0

        while True:

            # Event().wait(0.01)
            ser.reset_input_buffer()
            command = str.encode('?' + '\n')
            ser.write(command)
            grbl_out = ser.readline()
            grbl_response = grbl_out.strip().decode('utf-8')
            #print(grbl_response)

            if grbl_response != 'ok':

                if grbl_response.find('Idle') > 0:
                    idle_counter += 1

            if idle_counter > 0:
                break
    return


def move_gcode(GRBL_port_path, gcode, home, x, y, z): #used to move CNC to one particular (x, y, z) location
    # with contect opens file/connection and closes it if function(with) scope is left
    with serial.Serial(GRBL_port_path, BAUD_RATE) as ser:
        send_wake_up(ser)
        cleaned_line = remove_eol_chars(remove_comment(gcode))
        if home:
            ##print(f'G92 X{x} Y{y} Z{z}\n')
            command = str.encode(f'G92 X{x} Y{y} Z{z}\n')
            ser.write(command)  # Send g-code

            wait_for_movement_completion(ser, cleaned_line)

            grbl_out = ser.readline()  # Wait for response with carriage return
            ##print(" : ", grbl_out.strip().decode('utf-8'))
            x = 0
            y = 0
            z = 0
        if cleaned_line:  # checks if string is empty
            ##print("Sending gcode:" + str(cleaned_line))
                # converts string to byte encoded string and append newline
            command = str.encode(gcode + '\n')
            ser.write(command)  # Send g-code

            wait_for_movement_completion(ser, cleaned_line)

            grbl_out = ser.readline()  # Wait for response with carriage return
            ##print(" : ", grbl_out.strip().decode('utf-8'))
            position = [x, y, z]

        ##print('End of gcode')
        with open("position.csv", 'w') as csvfile: #update position of CNC
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(position)

def get_start_stats(well, filename): #calcula la media y la desviacion tipica de 10 medidas cuando el sensor todavia no ha contactado con la muestra (valores negativos ya que el sensor a fuerza de compresion las detecta negativas)
    measurements = []
    device.start()
    sensors = device.get_enabled_sensors()
    ##print("reading force")
    for i in range(0, 10):
        if device.read():
            for sensor in sensors:
                measurements.append(sensor.values[0])
                #print(measurements)
                ##print(sensor.values)
                sensor.clear()
        time.sleep(0.05)
    device.stop()
    average = statistics.mean(measurements)
    standard_dev = statistics.stdev(measurements)
    ##print(f"avg = {average}")
    ##print(f"stdev = {standard_dev}")
    with open(filename, 'a') as csvfile:
        csvwriter = csv.writer(csvfile)
        row = [well, str(average), str(standard_dev)]
        csvwriter.writerow(row)
    return average, standard_dev

def get_measurement(): #Enciende el sensor, lee un solo valor de fuerza actual y lo devuelve. Se usa constantemente durante la bajada para monitorizar si ya hemos tocado el gel.
    device.start()
    val = 0
    sensors = device.get_enabled_sensors()
    if device.read():
        for sensor in sensors:
            val = sensor.values
            val = val[0]
            ##print(val)
            sensor.clear()
    device.stop()
    #val = val[0]
    val = val
    return val


def stream_gcode(GRBL_port_path, gcode, x, y, well, filename): #Esta función controla el movimiento y decide cuándo parar. #used to indent a well with multiple lines of gcode
    # with contect opens file/connection and closes it if function(with) scope is left
    stiff = False
    with serial.Serial(GRBL_port_path, BAUD_RATE) as ser:
        send_wake_up(ser)
        avg, stdev = get_start_stats(well, filename)
        down = True
        up = False
        z = -1*height_offset+1 #punto de partida "seguro" por encima de la muestra.
        z_max = lowest - 2 #sets maximum depth indenter will indent to before automatically moving up
        contact = False
        measurements = []
        for line in gcode:
            ##print(z)
            value = get_measurement() #take force measurement
            if value < avg - 0.02: #force sensor indicates contact
                print("First contact detected")
                ##print(z_max)
                measurements.append(value * -1)
                if z == z_max or value <= -45: #exit conditions for testing well
                    if value <= -45 and len(measurements) <= 30: #force too high, threshold lower than max force for sensor to prevent taking another step
                        print("Sample too stiff to analyze")
                        stiff = True
                    return measurements, z, stiff
                if len(measurements) == 1: #set maximum indentation depth if contact detected for first time
                    ##print("creating z_max")
                    z_max = round(z - 1, 2)
                    print(z_max)
                contact = True
                z = round(z-0.02, 2)
            elif contact == True and value >= avg - 0.02: #reset if contact is no longer detected
                print("False alarm reset z data")
                z_max = lowest - 2 #reset maximum indentation depth
                contact = False
                measurements = []
                z = round(z-0.02, 2)
                #Start here!
            else:
                z = round(z-0.02, 2)
            with open(filename, 'a') as csvfile: #save measurement to file
                csvwriter = csv.writer(csvfile)
                row = [str(well), str(z), str(value * -1)]
                csvwriter.writerow(row)
            cleaned_line = remove_eol_chars(remove_comment(line))
            if cleaned_line:  # checks if string is empty
                ##print("Sending gcode:" + str(cleaned_line))
                # converts string to byte encoded string and append newline
                command = str.encode(line + '\n')
                ser.write(command)  # Send g-code

                wait_for_movement_completion(ser, cleaned_line)

                grbl_out = ser.readline()  # Wait for response with carriage return
                ##print(" : ", grbl_out.strip().decode('utf-8'))
            position = [x, y, z]
            with open("position.csv", 'w') as csvfile: #update position of CNC
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(position)

        return measurements, z, stiff


def load_csv(filename): #limpieza de filas
   with open(filename, 'r') as file:
       reader = csv.reader(file)
       data = list(reader)
   cleaned_data = []
   for i in range(0, len(data)):
       if data[i] != []:
           cleaned_data.append(data[i])
   return cleaned_data


def collect_run_data(data, well, stiff): #collect data for specific run from csv file
    well_data = []
    no_contact = []
    run_array = []
    forces = []
    if stiff:
        return run_array
    for i in range(0, len(data)):
        if data[i][0] == well: #collect data from most recent well
            values = [data[i][1], data[i][2]]
            well_data.append(values)
    #print(well_data)
    #print("\n")
    for l in range(1, len(well_data)):
        if float(well_data[l][1]) <= -1*float(well_data[0][0]) + 2*float(well_data[0][1]): #si el valor no es mayor que la media del ruido + 2* desv se considera no contact, del contrario si contacta.
            no_contact.append(l)
        run_array.append([well_data[l][0], well_data[l][1]])
    #print(run_array)
    #print("\n")
    #print(no_contact)
    #print("\n")
    if len(run_array) - int(no_contact[len(no_contact) - 1]) <= 10: #check if no or not enough data was collected for well
        print("Either well was not tested or no data was collected, either because sample was too short or too soft")
        run_array = []
        return run_array
    if len(no_contact) > 0: #find index of first continuous contact measurement
        start_val = int(no_contact[len(no_contact)-1]+1)
    else:
        start_val = 0
    #print(start_val)
    #print(len(well_data))
    #print(run_array[start_val][0])
    for k in range(0, len(run_array)): #format data for analysis
        run_array[k][0] = round(-1*(float(run_array[k][0]) - float(well_data[start_val][0])), 2) #set indentation depths relative to initial contact height
        run_array[k][1] = float(run_array[k][1]) + float(well_data[0][0]) #zero forces
        forces.append(run_array[k][1])
        
    if forces == [] or max(forces)-min(forces) < 0.04: #check that force measurements were large enough to make proper measurement
        print("Either well was not tested or no data was collected, either because sample was too short or too soft")
        run_array = []
        return run_array
    #print(run_array)
    #print("\n")
    return run_array

def split(run_array): #splits data from well into separate depth and force arrays
    depths = []
    forces = []
    for i in range(0, len(run_array)):
        depths.append(run_array[i][0])
        forces.append(run_array[i][1])
    return depths, forces

def find_d_and_f_in_range(run_array): #select data within desired depth range to determine elastic modulus
    forces = []
    depths = []
    for i in range(0, len(run_array)):
        if run_array[i][0] >= 0.3 and run_array[i][0] <= 0.7: #.04, .3
            forces.append(run_array[i][1])
            depths.append(run_array[i][0])
    return depths, forces

def approximate_height(run_array): #find height of sample to determine correction equation used
    depths = []
    for i in range(0, len(run_array)):
        depths.append(run_array[i][0])
    for j in range(0, len(depths)):
        depths[j] = abs(depths[j])
    zero = min(depths)
    num = depths.index(zero)
    z_pos = (num * 0.02) + 6.5##El 3 es del height offset y el num * 0.02 es lo que ha avanzado hasta el contacto
    approx_height = 18 - z_pos##CUIDADO CON ESE 15 ES LA DISTANCIA ENTRE LA BOLA Y EL FONDO DEL HIDROGEL varia segun la long de nuestro sist
    #print(approx_height)
    return approx_height

def correct_force(depths, forces, p_ratio, approx_height): #add correction factor based on simulation data since samples are not ideal shapes
    new_array = []
    for i in range(0, len(depths)):
        if p_ratio < 0.325:
            if approx_height >= 9.5:
                b = 0.13
                c = 1.24
            elif approx_height >= 8.5 and approx_height < 9.5:
                b = 0.131
                c = 1.24
            elif approx_height >= 7.5 and approx_height < 8.5:
                b = 0.133
                c = 1.25
            elif approx_height >= 6.5 and approx_height < 7.5:
                b = 0.132
                c = 1.24
            elif approx_height >= 5.5 and approx_height < 6.5:
                b = 0.132
                c = 1.24
            elif approx_height >= 4.5 and approx_height < 5.5:
                b = 0.139
                c = 1.27
            elif approx_height >= 3.5 and approx_height < 4.5:
                b = 0.149
                c = 1.3
            else:
                b = 0.162
                c = 1.38
        elif p_ratio >= 0.325 and p_ratio < 0.375:
            if approx_height >= 9.5:
                b = 0.132
                c = 1.25
            elif approx_height >= 8.5 and approx_height < 9.5:
                b = 0.132
                c = 1.25
            elif approx_height >= 7.5 and approx_height < 8.5:
                b = 0.134
                c = 1.25
            elif approx_height >= 6.5 and approx_height < 7.5:
                b = 0.136
                c = 1.26
            elif approx_height >= 5.5 and approx_height < 6.5:
                b = 0.126
                c = 1.25
            elif approx_height >= 4.5 and approx_height < 5.5:
                b = 0.133
                c = 1.27
            elif approx_height >= 3.5 and approx_height < 4.5:
                b = 0.144
                c = 1.32
            else:
                b = 0.169
                c = 1.42
        elif p_ratio >= 0.375 and p_ratio < 0.425:
            if approx_height >= 9.5:
                b = 0.181
                c = 1.33
            elif approx_height >= 8.5 and approx_height < 9.5:
                b = 0.182
                c = 1.34
            elif approx_height >= 7.5 and approx_height < 8.5:
                b = 0.183
                c = 1.34
            elif approx_height >= 6.5 and approx_height < 7.5:
                b = 0.183
                c = 1.34
            elif approx_height >= 5.5 and approx_height < 6.5:
                b = 0.194
                c = 1.38
            elif approx_height >= 4.5 and approx_height < 5.5:
                b = 0.198
                c = 1.4
            elif approx_height >= 3.5 and approx_height < 4.5:
                b = 0.203
                c = 1.44
            else:
                b = 0.176
                c = 1.46
        elif p_ratio >= 0.425 and p_ratio < 0.475:
            if approx_height >= 9.5:
                b = 0.156
                c = 1.35
            elif approx_height >= 8.5 and approx_height < 9.5:
                b = 0.152
                c = 1.34
            elif approx_height >= 7.5 and approx_height < 8.5:
                b = 0.156
                c = 1.35
            elif approx_height >= 6.5 and approx_height < 7.5:
                b = 0.161
                c = 1.37
            elif approx_height >= 5.5 and approx_height < 6.5:
                b = 0.153
                c = 1.37
            elif approx_height >= 4.5 and approx_height < 5.5:
                b = 0.166
                c = 1.42
            elif approx_height >= 3.5 and approx_height < 4.5:
                b = 0.179
                c = 1.47
            else:
                b = 0.205
                c = 1.59
        else:
            if approx_height >= 9.5:
                b = 0.203
                c = 1.58
            elif approx_height >= 8.5 and approx_height < 9.5:
                b = 0.207
                c = 1.6
            elif approx_height >= 7.5 and approx_height < 8.5:
                b = 0.212
                c = 1.62
            elif approx_height >= 6.5 and approx_height < 7.5:
                b = 0.217
                c = 1.65
            elif approx_height >= 5.5 and approx_height < 6.5:
                b = 0.21
                c = 1.64
            elif approx_height >= 4.5 and approx_height < 5.5:
                b = 0.22
                c = 1.68
            elif approx_height >= 3.5 and approx_height < 4.5:
                b = 0.17
                c = 1.58
            else:
                b = 0.182
                c = 1.64
        val = (forces[i])/(c*pow(depths[i], b))
        new_array.append(val)
    return new_array


def adjust_depth(run_array, d0): #using curve fit, adjust depth so that at zero force, depth is 0
    for i in range(0, len(run_array)):
        run_array[i][0] = run_array[i][0]-d0
    return run_array


def find_E(A, p_ratio): #determine elastic modulus from curve fit
    r_sphere = 0.00235
    sphere_p_ratio = 0.28
    sphere_E = 1.8 * pow(10, 11)
    polymer_p_ratio = p_ratio
    actual_A = A * pow(1000, 1.5)
    E_star = (actual_A * 0.75)/pow(r_sphere, 0.5)
    E_inv = 1/(E_star * (1 - pow(polymer_p_ratio, 2))) - (1 - pow(sphere_p_ratio, 2))/(sphere_E * (1 - pow(polymer_p_ratio, 2)))
    E_polymer = 1/E_inv
    return E_polymer

def adjust_E(E): #an empirical correction factor for softer samples which causes issues with getting proper data at small indentation depths
    if E < 660000:
        factor = 457*pow(E, -0.457)
        E = E/factor
    return E


def go_home(GRBL_port_path): #move CNC back to its home position
    n = 1
    with open('position.csv', mode='r') as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            if n == 1:
                position = lines
                #print(position)
            n = n + 1
    #print(position)
    x = position[0]
    y = position[1]
    z = position[2]
    if x !=0 or y != 0 or z !=0:
        #print(x)
        #print(y)
        #print(z)
        home = True
        gcode = f"G01 Z0 F500" #move CNC up first to prevent any collisions
        #print(f"G01 Z0 F500")
        home_z(GRBL_port_path, gcode, home, x, y, z)
        gcode = f"G01 X0 Y0 F500" #move CNC to home position
        #print(f"G01 X0 Y0 F500")
        home_xy(GRBL_port_path, gcode, home, x, y, z)

def home_z(GRBL_port_path, gcode, home, x, y, z): #move CNC to home height position
    # with contect opens file/connection and closes it if function(with) scope is left
    with serial.Serial(GRBL_port_path, BAUD_RATE) as ser:
        send_wake_up(ser)
        cleaned_line = remove_eol_chars(remove_comment(gcode))
        if home:
            #print(f'G92 Z{z}\n')
            command = str.encode(f'G92 Z{z}\n')
            ser.write(command)  # Send g-code

            wait_for_movement_completion(ser, cleaned_line)

            grbl_out = ser.readline()  # Wait for response with carriage return
            #print(" : ", grbl_out.strip().decode('utf-8'))
            z = 0
        if cleaned_line:  # checks if string is empty
            #print("Sending gcode:" + str(cleaned_line))
                # converts string to byte encoded string and append newline
            command = str.encode(gcode + '\n')
            ser.write(command)  # Send g-code

            wait_for_movement_completion(ser, cleaned_line)

            grbl_out = ser.readline()  # Wait for response with carriage return
            #print(" : ", grbl_out.strip().decode('utf-8'))
            position = [x, y, z]

        #print('End of gcode')
        with open("position.csv", 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(position)

def home_xy(GRBL_port_path, gcode, home, x, y, z): #move CNC to home x and y position
    # with contect opens file/connection and closes it if function(with) scope is left
    with serial.Serial(GRBL_port_path, BAUD_RATE) as ser:
        send_wake_up(ser)
        cleaned_line = remove_eol_chars(remove_comment(gcode))
        if home:
            #print(f'G92 X{x} Y{y}\n')
            command = str.encode(f'G92 X{x} Y{y}\n')
            ser.write(command)  # Send g-code

            wait_for_movement_completion(ser, cleaned_line)

            grbl_out = ser.readline()  # Wait for response with carriage return
            #print(" : ", grbl_out.strip().decode('utf-8'))
            x = 0
            y = 0
            z = 0
        if cleaned_line:  # checks if string is empty
            #print("Sending gcode:" + str(cleaned_line))
            # converts string to byte encoded string and append newline
            command = str.encode(gcode + '\n')
            ser.write(command)  # Send g-code

            wait_for_movement_completion(ser, cleaned_line)

            grbl_out = ser.readline()  # Wait for response with carriage return
            #print(" : ", grbl_out.strip().decode('utf-8'))
            position = [x, y, z]

        #print('End of gcode')
        with open("position.csv", 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(position)

if __name__ == "__main__":
    # Inicialización del dispositivo
    device.open(auto_start=False)

    # Limpiar archivo temporal de mediciones
    f = open("measurements.csv", "w")
    f.truncate()
    f.close()

    # Enviar CNC a Home
    go_home(GRBL_port_path) 

    entry_wells = []
    cols = ["A", "B", "C", "D", "E", "F", "G", "H"]
    rows = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
    x = {"A": "", "B": "", "C": "", "D": "", "E": "", "F": "", "G": "", "H": ""}
    y = {"1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": "", "9": "", "10": "", "11": "", "12": ""}
    
    # Parámetros de la placa
    x_init = 19.81
    y_init = 48.4
    offset = 9
    z_up = "0"
    height_offset = 7.5
    h_speed = "500"  
    v_speed = "100"  
    lowest = -20
    results = []

    for i in range(0, 8):  
        x[cols[i]] = str(x_init + offset * i)
    for j in range(0, 12):  
        y[rows[j]] = str(y_init + offset * j)

    # Lógica de nombre de archivo
    bad_name = True
    while bad_name:
        filename = input("Introduce el nombre del archivo (sin espacios): ")
        count = 0
        for i in range(0, len(filename)):
            if filename[i] == " ":
                count = count + 1
        if count > 0:
            print("Nombre inválido, contiene espacios.")
        else:
            results_filename = filename + "_results.csv"
            filename = filename + ".csv"
            bad_name = False

    # SELECCIÓN DE POZOS
    modes = ["1", "2", "3", "4"]
    entered = False
    while not entered: 
        mode = input("Modo: 1 (individual), 2 (filas), 3 (columnas), 4 (placa entera): ")
        while mode not in modes:
            mode = input("Error. Elige 1, 2, 3 o 4: ")
        
        if mode == "1":
            more = True
            while more:
                well = input("Introduce pozo (ej. A1) o Enter para terminar: ")
                if well == '': more = False
                elif well[0] not in cols or well.lstrip("ABCDEFGH") not in rows: print("Error")
                else: entry_wells.append(well)
        elif mode == "2":
            more = True
            while more:
                row = input("Introduce fila (1-12) o Enter para terminar: ")
                if row == '': more = False
                elif row not in rows: print("Error")
                else:
                    for i in range(0, len(cols)): entry_wells.append(cols[i] + row)
        elif mode == "3":
            more = True
            while more:
                col = input("Introduce columna (A-H) o Enter para terminar: ")
                if col == '': more = False
                elif col not in cols: print("Error")
                else:
                    for i in range(0, len(rows)): entry_wells.append(col + rows[i])
        elif mode == "4":
            for j in range(0, len(cols)):
                for i in range(0, len(rows)): entry_wells.append(cols[j] + rows[i])

        print(f"Pozos actuales: {entry_wells}")
        correct = input("¿Confirmar pozos? Y/N: ")
        if correct.lower() == 'y':
            entered = True
        else:
            entry_wells = []

    # Eliminar duplicados
    wells = []
    for well in entry_wells:
        if well not in wells: wells.append(well)

    # Lógica de Poisson's Ratio
    p_ratios = []
    same_ratio = input("¿Mismo Poisson Ratio para todos? Y/N: ")
    if same_ratio.lower() == 'y':
        pr = float(input("Introduce Poisson Ratio (0.3-0.5): "))
        for i in range(len(wells)): p_ratios.append(pr)
    else:
        for w in wells:
            pr = float(input(f"Poisson Ratio para {w}: "))
            p_ratios.append(pr)

    # BUCLE PRINCIPAL DE MEDICIÓN
    curr_x = 0
    curr_y = 0
    home = False

    for n in range(0, len(wells)):
        well = wells[n]
        print(f"\n--- Probando pozo {well} ---")
        col = well[0]
        X = float(x[col])
        new_X = str(X - curr_x)
        row = well.lstrip("ABCDEFGH")
        Y = float(y[row])
        new_Y = str(Y - curr_y)
        
        z_int = round(-1 * height_offset + 1, 2)
        Z = z_int

        # Mover a pozo
        if n == 0: gcode_move = f"G01 X{new_X} Y{new_Y} Z{z_int} F{h_speed}"
        else: gcode_move = f"G01 X{new_X} Y{new_Y} F{h_speed}"
        move_gcode(GRBL_port_path, gcode_move, home, X, Y, Z)

        # Indentación
        gcode_indent = []
        z_iter = -0.02
        while z_iter >= lowest + 1:
            gcode_indent.append(f"G01 Z{z_iter} F{v_speed}")
            z_iter = round(z_iter - 0.02, 2)

        measurements, z_final, stiff = stream_gcode(GRBL_port_path, gcode_indent, X, Y, well, filename)
        
        # Regresar eje Z
        move_gcode(GRBL_port_path, f"G01 Z{-z_final + Z} F{v_speed}", home, X, Y, Z)
        curr_x, curr_y = X, Y

        # ANALISIS Y GRÁFICA
        data = load_csv(filename)
        run_array = collect_run_data(data, well, stiff)
        
        if run_array != []:
            height = approximate_height(run_array)
            depth_in_range, force_in_range = find_d_and_f_in_range(run_array)
            p_ratio = p_ratios[n]
            adjusted_forces = correct_force(depth_in_range, force_in_range, p_ratio, height)
            
            depth_in_range = np.asarray(depth_in_range)
            adjusted_forces = np.asarray(adjusted_forces)

            def Hertz_func(depth, A, d0):
                return A * np.power(depth - d0, 1.5)

            error = False
            try:
                parameters, covariance = curve_fit(Hertz_func, depth_in_range, adjusted_forces, p0=[2, 0.03])
                fit_A, fit_d0 = float(parameters[0]), float(parameters[1])
            except:
                print(f"Error en ajuste del pozo {well}")
                error = True

            if not error:
                # Refinamiento cíclico de d0
                count = 0
                while abs(fit_d0) > 0.01 and count < 50:
                    count += 1
                    run_array = adjust_depth(run_array, fit_d0)
                    depth_in_range, force_in_range = find_d_and_f_in_range(run_array)
                    adjusted_forces = correct_force(depth_in_range, force_in_range, p_ratio, height)
                    depth_in_range, adjusted_forces = np.asarray(depth_in_range), np.asarray(adjusted_forces)
                    try:
                        parameters, _ = curve_fit(Hertz_func, depth_in_range, adjusted_forces, p0=[2, 0.03])
                        fit_A, fit_d0 = float(parameters[0]), float(parameters[1])
                    except: break

                E = round(adjust_E(find_E(fit_A, p_ratio)).real)
                err = np.sqrt(np.diag(covariance))
                std_dev = round(find_E(err[0], p_ratio))

                
                if len(depth_in_range) > 1:
                    print(f"Resultado pozo {well}: E = {E} Pa, Error = {std_dev} Pa")
                    pyplot.figure(figsize=(8, 5))
                    pyplot.scatter(depth_in_range, adjusted_forces, color='blue', alpha=0.5, label='Datos')
                    d_model = np.linspace(min(depth_in_range), max(depth_in_range), 100) # Aquí fallaba
                    f_model = fit_A * np.power(d_model, 1.5)
                    pyplot.plot(d_model, f_model, color='red', label=f'Hertz (E={E} Pa)')
                    pyplot.title(f"Pozo {well}")
                    pyplot.xlabel("Indentación (mm)")
                    pyplot.ylabel("Fuerza (N)")
                    pyplot.legend()
                    pyplot.grid(True)
                    pyplot.savefig(f"Plot_{well}_{filename.replace('.csv','')}.png")
                    pyplot.close() 
                else:
                    print(f"Resultado pozo {well}: E = {E} Pa. (Aviso: Datos insuficientes para graficar tras procesamiento)")

                
                row = [well, E, std_dev]
                results.append(row)
                with open(results_filename, 'a') as csvfile:
                    csv.writer(csvfile).writerow(row)
            else:
                results.append([well, "no data", "no data"])
        else:
            results.append([well, "no data", "no data"])

    # FINALIZAR Y MOSTRAR RESUMEN TOTAL[cite: 4]
    move_gcode(GRBL_port_path, "G01 X0 Y0 Z0 F500", True, round(curr_x, 2), round(curr_y, 2), round(Z, 2))
    
    print("\n--- TEST COMPLETADO ---")
    print("Resumen de resultados finales:")
    for res in results:
        print(f"Pozo {res[0]}: E = {res[1]} N/m^2, Incertidumbre = {res[2]} N/m^2")