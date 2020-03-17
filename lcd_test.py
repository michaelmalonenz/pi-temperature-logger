import luma.oled.device
from luma.core.sprite_system import framerate_regulator
from luma.core import cmdline
import sys
from PIL.ImageFont import truetype


class make_serial(object):
    """
    Serial factory.
    """

    def __init__(self, opts, gpio=None):
        self.opts = opts
        self.gpio = gpio

    def i2c(self):
        from luma.core.interface.serial import i2c
        return i2c(port=self.opts['i2c_port'], address=self.opts['i2c_address'])

    def spi(self):
        from luma.core.interface.serial import spi
        if hasattr(self.opts, 'gpio') and self.opts['gpio'] is not None:
            GPIO = importlib.import_module(self.opts['gpio'])

            if hasattr(self.opts, 'gpio_mode') and self.opts['gpio_mode'] is not None:
                (packageName, _, attrName) = self.opts['gpio_mode'].rpartition('.')
                pkg = importlib.import_module(packageName)
                mode = getattr(pkg, attrName)
                GPIO.setmode(mode)
            else:
                GPIO.setmode(GPIO.BCM)

            atexit.register(GPIO.cleanup)
        else:
            GPIO = None

        return spi(port=self.opts['spi_port'],
                   device=self.opts['spi_device'],
                   bus_speed_hz=self.opts['spi_bus_speed'],
                   cs_high=self.opts['spi_cs_high'],
                   transfer_size=self.opts['spi_transfer_size'],
                   gpio_DC=self.opts['gpio_data_command'],
                   gpio_RST=self.opts['gpio_reset'],
                   gpio=self.gpio or GPIO)

    def ftdi_spi(self):
        from luma.core.interface.serial import ftdi_spi
        return ftdi_spi(device=self.opts['ftdi_device'],
                        bus_speed_hz=self.opts['spi_bus_speed'],
                        gpio_DC=self.opts['gpio_data_command'],
                        gpio_RST=self.opts['gpio_reset'])

    def ftdi_i2c(self):
        from luma.core.interface.serial import ftdi_i2c
        return ftdi_i2c(address=self.opts['i2c_address'])


parser = cmdline.create_parser(description='lcd test')
args = parser.parse_args(sys.argv[1:])

args = {
  'spi_cs_high': False, 'loop': 0, 'duration': 0.01, 'rotate': 0, 'mode': 'RGB', 'transform': 'scale2x',
  'gpio_data_command': 23, 'ftdi_device': 'ftdi://::/1', 'i2c_port': 1, 'spi_bus_speed': 8000000,
  'config': None, 'gpio_mode': None, 'v_offset': 0, 'gpio': None, 'spi_transfer_size': 4096, 'h_offset': 0,
  'scale': 2, 'gpio_backlight': 18, 'width': 128, 'interface': 'spi', 'bgr': False, 'display': 'ssd1306',
  'gpio_reset': 24, 'backlight_active': 'low', 'framebuffer': 'diff_to_previous', 'i2c_address': '0x3C',
  'max_frames': None, 'height': 64, 'block_orientation': 0, 'spi_port': 0, 'spi_device': 0
}


Device = getattr(luma.oled.device, args['display'])
Serial = getattr(make_serial(args), args['interface'])
piboto_font = truetype('/usr/share/fonts/truetype/piboto/Piboto-Regular.ttf', size=20)


class LcdScreen:

    def display(self, text, num_frames = 40):
        device = Device(serial_interface=Serial(), **args)
        canvas = luma.core.render.canvas(device)
        regulator = framerate_regulator(fps=0)
        while num_frames > 0:
            with regulator:
                with canvas as c:
                    c.text((2, 0), text, fill="white", font=piboto_font)
            num_frames -= 1

    def display_image(self, image):
        num_frames = 40
        device = Device(serial_interface=Serial(), **args)
        canvas = luma.core.render.canvas(device, background=image)
        regulator = framerate_regulator(fps=0)
        while num_frames > 0:
            with regulator:
                with canvas as c:
                    pass
            num_frames -= 1
