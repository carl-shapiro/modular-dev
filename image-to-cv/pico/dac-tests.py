from machine import Pin, I2C
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

MAX_VOLTAGE = 4095
MAX_COLOR_VAL = 255
PIXEL_POS = {
    "red":0,
    "green":1,
    "blue":2
}
led = Pin(25,Pin.OUT)
dacs = {}
file = None
               

def init():
    global dacs
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
     
def sendCV(dac, color_val):
    voltage = int((color_val / MAX_COLOR_VAL) * MAX_VOLTAGE)
    voltage = MAX_VOLTAGE if (voltage > MAX_VOLTAGE) else voltage;
    print(f'Voltage: {voltage}')
    dac.write(voltage)

# dacs = init()
init()

file = open("/sd/test.csv", "r")
line = file.readline()
while line:
    print(f"Line: {line}", end='')
    p_vals = list(map(int,line.split(",")))
    for key in PIXEL_POS:
        sendCV(dacs[key], p_vals[PIXEL_POS[key]])
    gc.collect()  # Run garbage collection to free up memory
    free_memory = gc.mem_free()  # Get available free memory in bytes
    print("Free memory:", free_memory, "bytes")
    print("=============================================")
    line = file.readline()
    time.sleep(1)

file.close()    
        
