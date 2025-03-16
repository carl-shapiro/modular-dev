"""\
image-2-cv.py

This script converts the RGB pixel values of an image to CV, gate and trigger signals.
Currently, it reads a csv file that contains the RGB values from a BMP, converts those values to a voltage (CV, gate, trigger, etc...)
and transmits them via a DAC.

This script is intended to be run on a Raspberry Pico 2040.

TODO (in no particular order):

    Toggle/button to switch between attenuvertion and attenuation?
    Gate/trig logic (might want to wait until three position switches come in)
    Start on envelope (will need to add another DAC)
    Some sort of image file selector (how to display which file is selected?)
    Write out "performance" file to SD card (write modified RGB values from module to file on SD card)    
    Lambda/API Gateway to do image conversion to CSV. Create three versions of the CSV
        * normal/x to y (left to right, top to bottom)
        * vertical/y to x (top to bottom, left to right)
        * random (mangle the order of each pixel value/row
    Glide toggle for each color? So that changes between each CV value isn't so abrupt?        
    Idea: Some way of iterating through all of a rows color (red, green or blue) at a different rate than the other colors. If a color "finishes" all of the values in a row/column
          then loop back to the beginning of the current row/column for that color. Perhaps trig in could *only* advance the position in the row/column for a specific color?
          
              
        

"""


from machine import Pin, I2C, ADC
import mcp4725
import time, random, gc, sdcard, uos


### DAC SETTINGS
DAC_ADDR = {
    "red": {
        "addr": 0x60,
        "i2c": 0
    },

    "green": {
        "addr": 0x60,
        "i2c": 1
    },
    "blue": {
        "addr": 0x61,
        "i2c": 0
    }
}
I2C_FREQ = 100000

### SD SETTINGS
CLK_SRC_PIN = 9
SD_READER_PINS = {
    "sck": 10,
    "mosi":11,
    "miso":8    
}
pots = {
    "red":{
        "adc_pin": 26
    },
    "green":{
        "adc_pin":27
    },
    "blue":{
        "adc_pin":28
    }
}


FILENAMES = [
    "test.csv"
]

ATTENUVERT = 1
BUTTON_PRESS_WAIT_MS = 150
MAX_VOLTAGE = 4095
MAX_COLOR_VAL = 255
PIXEL_POS = {
    "red":0,
    "green":1,
    "blue":2
}


dacs = {}
file = None




def init():
    global dacs
    global pots
    ### SD Card
    cs = machine.Pin(CLK_SRC_PIN, machine.Pin.OUT)
    # Intialize SPI peripheral (start with 1 MHz)
    spi = machine.SPI(1,
                      baudrate=1000000,
                      polarity=0,
                      phase=0,
                      bits=8,
                      firstbit=machine.SPI.MSB,
                      sck=machine.Pin(SD_READER_PINS["sck"]),
                      mosi=machine.Pin(SD_READER_PINS["mosi"]),
                      miso=machine.Pin(SD_READER_PINS["miso"]))

    sd = sdcard.SDCard(spi, cs)
    vfs = uos.VfsFat(sd)
    uos.mount(vfs, "/sd")
    
    ### DACS
    i2cs = [
            I2C(0,scl=Pin(13),sda=Pin(12),freq=I2C_FREQ),
            I2C(1,scl=Pin(7),sda=Pin(6),freq=I2C_FREQ)        
    ]
    for key in DAC_ADDR.keys():        
        dacs[key] = mcp4725.MCP4725(i2cs[DAC_ADDR[key]["i2c"]],DAC_ADDR[key]["addr"])
    for key in pots.keys():
        pots[key]["pot"] = ADC(machine.Pin(pots[key]["adc_pin"]))
     

#Vout = 2aVin - Vin
# Vout is the output voltage 
# Vin is the input voltage 
# 'a' is a value between 0 and 1 representing the control's position (0 = fully attenuated, 1 = fully open) 
def attenuvert(sig_in, position):
    return ((2*position)*sig_in) - sig_in
     

def sendCV(dac, color_val):
    voltage = int((color_val / MAX_COLOR_VAL) * MAX_VOLTAGE)
    voltage = MAX_VOLTAGE if (voltage > MAX_VOLTAGE) else voltage;
    print(f'{color_val} Output Voltage: {voltage}')
    dac.write(voltage)

def getPotsValues():
    pot_vals = {}
    for key in pots.keys():
        adc_val = pots[key]["pot"].read_u16()
        pot_vals[key] = {
            "adc_val": adc_val,
            "voltage": (3.3/65535)*adc_val
        }
    return pot_vals        
    #print("ADC Voltage: ", round(volt,2))
    


# dacs = init()
init()
trig_button = Pin(2,Pin.IN, Pin.PULL_DOWN)
gate_button = Pin(3, Pin.IN, Pin.PULL_DOWN)
#file = open("/sd/test.csv", "r")
file = open("/sd/test.csv", "r")
line = file.readline()

lines_read = 0
while len(line) > 0:
    if( gate_button.value() != 1):
        
    if trig_button.value() == 1 or gate_button.value() == 1:
        lines_read += 1        
        print(f"Line: {line}", end='')                       
        pot_vals = getPotsValues()        
        pixel_vals = list(map(int,line.split(",")))
        for key in PIXEL_POS:
            color_val = pixel_vals[PIXEL_POS[key]]
            pixel_attenuverted = attenuvert(color_val, (pot_vals[key]['voltage']/3.3))                        
            sendCV(dacs[key], color_val)
            
        gc.collect()  # Run garbage collection to free up memory
        free_memory = gc.mem_free()  # Get available free memory in bytes
        print("Free memory:", int(free_memory / 1024), "KB", "<> Lines Read: ", lines_read)        
        print("=============================================")        
        line = file.readline()
        if(len(line) <= 0):
            file.close()
            
        time.sleep(BUTTON_PRESS_WAIT_MS / 1000)
        

# while (line := file.readline()):
# create a variable named "var_name" and assign it the value of 50
#exec(f"{var_name} = 50")
     
 
file.close()    
        
