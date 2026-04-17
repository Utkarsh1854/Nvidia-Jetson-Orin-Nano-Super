# 🔧 GPIO Pin Configuration — NVIDIA Jetson Orin Nano

A step-by-step guide to enable and configure GPIO pins on the **NVIDIA Jetson Orin Nano** using the Jetson-IO tool.


## 🛠️ Steps to Configure GPIO Pins

### Step 1 — Open the Terminal

Launch a terminal on your Jetson Orin Nano.

---

### Step 2 - Run the Jetson-IO Tool

Execute the following command with superuser privileges:

```
sudo /opt/nvidia/jetson-io/jetson-io.py
```

> **Note:** This launches an interactive terminal UI for configuring the Jetson's hardware interfaces.

---

### Step 3 — Select "Configure Jetson 40-pin Header"

Once the tool opens, use the **arrow keys** to navigate and select:

```
Configure Jetson 40pin Header
```

Press **Enter** to confirm.

---

### Step 4 — Select "Configure Header Pins Manually"

From the next menu, choose:

```
Configure header pins manually
```

Press **Enter** to continue.

---

### Step 5 — Select the Required Pin

- Use the **arrow keys** to scroll through the list of available pins.
- Press **Enter** to toggle/select the pin you want to configure as GPIO.
- Repeat for any additional pins you need.

---

### Step 6 — Save and Apply

After selecting the desired pins:

1. Navigate back to the main menu.
2. Select **Save and reboot pin changes**

```
sudo reboot
```

---

## 📌 Jetson Orin Nano — 40-Pin Header Pinout

```
 3.3V  [ 1] [ 2]  5V
  SDA  [ 3] [ 4]  5V
  SCL  [ 5] [ 6]  GND
GPIO4  [ 7] [ 8]  TXD
  GND  [ 9] [10]  RXD
GPIO17 [11] [12]  GPIO18
GPIO27 [13] [14]  GND
GPIO22 [15] [16]  GPIO23
  3.3V [17] [18]  GPIO24
 MOSI  [19] [20]  GND
 MISO  [21] [22]  GPIO25
 SCLK  [23] [24]  CE0
  GND  [25] [26]  CE1
  SDA  [27] [28]  SCL
GPIO5  [29] [30]  GND
GPIO6  [31] [32]  GPIO12
GPIO13 [33] [34]  GND
GPIO19 [35] [36]  GPIO16
GPIO26 [37] [38]  GPIO20
  GND  [39] [40]  GPIO21
```

## ⚠️ Important Notes

- Always run `GPIO.cleanup()` at the end of your script to release the pins.
- Make sure the pin is **not already in use** by another hardware interface (I2C, SPI, UART) before configuring it as GPIO.
- Incorrect wiring can **damage the board** — double-check voltage levels (3.3V logic on Jetson).
- Some pins may require a reboot to reflect changes made via `jetson-io.py`.
