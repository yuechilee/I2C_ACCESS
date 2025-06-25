import ctypes
import time

# 載入 DLL
ch341dll = ctypes.WinDLL("C:\\python\\demo\\CH341DLLA64.DLL")

# 初始化 CH341 裝置
if ch341dll.CH341OpenDevice(0) < 0:
    raise RuntimeError("無法開啟 CH341 裝置")

# 設定為 I2C 模式
mode = 0x1
ch341dll.CH341SetStream(0, mode)

def write_register(device_addr, reg_addr, value):
    """對 I2C 裝置的暫存器寫入單一位元組資料"""
    ret = ch341dll.CH341WriteI2C(0, device_addr, reg_addr, value)
    if ret != 2:
        raise IOError("寫入失敗")
    time.sleep(0.01)

def read_register(device_addr, reg_addr):
    """從 I2C 裝置的暫存器讀取單一位元組資料"""
    read_buf = (ctypes.c_ubyte * 1)()
    ret = ch341dll.CH341ReadI2C(0, device_addr, reg_addr, 1)
    if ret != 1:
        raise IOError("讀取失敗")
    return read_buf[0]

print("📌 輸入格式：0x15 0xF0         → 讀取")
print("📌 輸入格式：0x15 0xF0 0x01    → 寫入")
print("✴ 輸入 exit 離開程式")

while True:
    try:
        user_input = input("\n請輸入指令：")
        if user_input.strip().lower() == "exit":
            print("離開程式。")
            break

        parts = user_input.strip().split()
        hex_vals = [int(p, 16) for p in parts]

        if len(hex_vals) == 2:
            device_addr, reg_addr = hex_vals
            print(f"📥 讀取暫存器 Device 0x{device_addr:02X}, Reg 0x{reg_addr:02X} ...")
            value = read_register(device_addr, reg_addr)
            print(f"✅ 讀取值：0x{value:02X}")

        elif len(hex_vals) == 3:
            device_addr, reg_addr, value = hex_vals
            print(f"📤 寫入暫存器 Device 0x{device_addr:02X}, Reg 0x{reg_addr:02X} ← 0x{value:02X} ...")
            write_register(device_addr, reg_addr, value)
            print("✅ 寫入完成")

        else:
            print("⚠ 輸入錯誤：請輸入 2 或 3 個十六進位數值（例如：0x15 0xF0 或 0x15 0xF0 0x01）")

    except ValueError:
        print("⚠ 格式錯誤：請確認每個值皆為合法的 16進位格式（例如：0x15）")

    except Exception as e:
        print(f"❌ 發生錯誤：{e}")

# 關閉裝置
ch341dll.CH341CloseDevice(0)
