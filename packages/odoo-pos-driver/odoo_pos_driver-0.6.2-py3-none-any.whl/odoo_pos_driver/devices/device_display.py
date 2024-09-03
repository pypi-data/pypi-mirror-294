from unidecode import unidecode

from .device_abstract import DeviceAbstract


class DeviceDisplay(DeviceAbstract):
    use_serial = True
    device_type = "display"

    def _process_task_serial(self, serial, task):
        # TODO, check correct data
        lines_ascii = []

        for line in task.data:
            lines_ascii.append(unidecode(line))

        self._clear_screen(serial)

        for row, text in enumerate(lines_ascii, 1):
            # Begin text at the correct place
            self._position_cursor(serial, 1, row)
            serial.write(text.encode("ascii"))

    @classmethod
    def _clear_screen(cls, serial):
        serial.write(b"\x0C")

    @classmethod
    def _position_cursor(cls, serial, col=1, row=1):
        serial.write(b"\x1F\x24" + (chr(col) + chr(row)).encode("ascii"))
