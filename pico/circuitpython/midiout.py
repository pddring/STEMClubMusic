import board
import busio
import time
import terminalio
import displayio
import digitalio
from adafruit_display_text import label
from adafruit_st7789 import ST7789
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

i2c = busio.I2C(board.GP21, board.GP20)

# First set some parameters used for shapes and text
BORDER = 10
FONTSCALE = 2
BACKGROUND_COLOR = 0x00FF00  # Bright Green
FOREGROUND_COLOR = 0xAA0088  # Purple
TEXT_COLOR = 0xFFFF00


buttonA = digitalio.DigitalInOut(board.GP12)
buttonA.switch_to_input(pull=digitalio.Pull.UP)

# Release any resources currently in use for the displays
displayio.release_displays()

tft_cs = board.GP17
tft_dc = board.GP16
spi_mosi = board.GP19
spi_clk = board.GP18
spi = busio.SPI(spi_clk, spi_mosi)

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = ST7789(
    display_bus, rotation=180, width=240, height=240, rowstart=80
)

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BACKGROUND_COLOR

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(
    display.width - BORDER * 2, display.height - BORDER * 2, 1
)
inner_palette = displayio.Palette(1)
inner_palette[0] = FOREGROUND_COLOR
inner_sprite = displayio.TileGrid(
    inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
)
splash.append(inner_sprite)

# Draw a label
text = "MIDI"
text_area = label.Label(terminalio.FONT, text=text, color=TEXT_COLOR)
text_width = text_area.bounding_box[2] * FONTSCALE
text_group = displayio.Group(
    scale=FONTSCALE,
    x=display.width // 2 - text_width // 2,
    y=(display.height // 2) - 15,
)
text_group.append(text_area)  # Subgroup for text scaling

text_area1 = label.Label(terminalio.FONT, text="", color=TEXT_COLOR)
text_width1 = text_area1.bounding_box[2] * FONTSCALE
text_group1 = displayio.Group(
    scale=FONTSCALE,
    x=display.width // 2 - text_width1 // 2,
    y=(display.height // 2) + 15,
)
text_group1.append(text_area1)  # Subgroup for text scaling

splash.append(text_group)
splash.append(text_group1)
i = 0

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

while True:
    
    
    if not buttonA.value:
        text_area1.text = "Sending"
        midi.send(NoteOn("C2", 120))  # G sharp 2nd octave
        while not buttonA.value:
            time.sleep(0.1)
        midi.send(NoteOff("C2"))
        text_area1.text = ""
    time.sleep(0.1)
    i += 0.1
    pass


