import time
from queue import Queue
from threading import Thread

import serial.tools.list_ports
from flask_babel import gettext as _
from loguru import logger
from serial import Serial

from ..usb_device import usb_device_tools
from .device_task import DeviceTask


class DeviceAbstract(Thread):
    use_serial = False
    device_type = False

    def __init__(self, interface, delay=0, max_queue_size=0):
        """Initialize a new Device.
        delay: time between processing two messages, in seconds.
        """
        Thread.__init__(self)
        self._interface = interface
        self._usb_device = False
        self.errored_tasks = []
        self._queue = Queue(max_queue_size)
        self.usb_device_name = False
        self.delay = delay
        self.terminal_file = False
        self._usb_image_name = False

    @property
    def name(self):
        if self.device_type == "display":
            return _("Display")
        elif self.device_type == "printer":
            return _("Printer")
        elif self.device_type == "payment":
            return _("Payment Terminal")
        elif self.device_type == "scale":
            return _("Scale")
        return "N/C"

    @property
    def usb_vendor_product_code(self):
        return usb_device_tools.get_device_id_vendor_id_product(
            self._usb_device
        )

    @property
    def is_connected(self):
        return bool(self._usb_device)

    @property
    def queue_size(self):
        return self._queue.qsize()

    @property
    def max_queue_size(self):
        return self._queue.maxsize

    @property
    def errored_tasks_qty(self):
        return len(self.errored_tasks)

    @property
    def disconnections(self):
        return self._interface.disconnections.get(
            self.usb_vendor_product_code, []
        )

    @property
    def disconnections_qty(self):
        return len(self.disconnections)

    @property
    def usb_image_name(self):
        return self._usb_image_name or f"{self.device_type}.png"

    # ###########################
    # Thread / Task Section
    # ###########################
    def run(self):
        while True:
            if self._usb_device:
                current_size = self._queue.qsize()
                if current_size:
                    self._logger(
                        "INFO", f"Process one of the {current_size} task(s)."
                    )
                else:
                    self._logger("INFO", "Waiting for message ...")
                task = self._queue.get(True)
                self._process_task_abstract(task)
                time.sleep(self.delay)
            else:
                time.sleep(1)

    def _process_task_abstract(self, task):
        self._logger("DEBUG", f"Processing task {task.uuid} ...")
        try:
            if self.use_serial:
                with self._get_serial() as serial:
                    self._process_task_serial(serial, task)
            else:
                self._process_task(task)
            if task in self.errored_tasks:
                self.errored_tasks.remove(task)
            self._logger("SUCCESS", f"Task processed. UUID: {task.uuid}.")

        except Exception as e:
            self._logger("ERROR", f"Task {task.uuid}. Error{e}")
            task.error = e
            if task not in self.errored_tasks:
                self._logger("INFO", f"Reenqueing task. UUID: {task.uuid} ...")
                self.errored_tasks.append(task)
                self._queue.put(task)
            if self._usb_device:
                self._interface._hook_usb_device_removed(self._usb_device, e)

    def add_task(self, data):
        if self.max_queue_size:
            while self._queue.qsize() >= self._queue.maxsize:
                self._logger("WARNING", "Removing obsolete task in queue.")
                self._queue.get_nowait()
        task = DeviceTask(data)
        self._queue.put(task)
        self._logger(
            "INFO",
            f"Task Enqueued ({self._queue.qsize()}/{self._queue.maxsize})."
            f" UUID: {task.uuid}",
        )

    # ###########################
    # Device Section
    # ###########################
    def set_usb_device(self, usb_device, extra_info):
        self._usb_device = usb_device
        self.usb_device_name = extra_info.get("name", False)
        self._usb_image_name = extra_info.get("image")
        connected_comports = [x for x in serial.tools.list_ports.comports()]
        for port in connected_comports:
            if (port.vid, port.pid) == (
                usb_device.idVendor,
                usb_device.idProduct,
            ):
                self.terminal_file = port.device
                self._logger(
                    "DEBUG", f"Terminal File found: {self.terminal_file}."
                )
                break
        if not self.terminal_file:
            self._logger("DEBUG", "Terminal File not found.")

    def remove_usb_device(self):
        self._usb_device = False
        self.usb_device_name = False
        self._usb_image_name = False
        self.terminal_file = False

    def _get_serial(self):
        if not self.terminal_file:
            raise Exception(
                "Unable to open a Serial connexion,"
                " because terminal_file is not defined."
            )
        return Serial(self.terminal_file, 9600, timeout=0.05)

    # ###########################
    # Loggging Section
    # ###########################
    def _logger(self, level, message):
        if self._usb_device:
            extra_info = (
                f" ({self.usb_device_name} - {self.usb_vendor_product_code})"
            )
        else:
            extra_info = ""
        logger.log(
            level, f"Device '{self.device_type}'{extra_info}: {message}"
        )
