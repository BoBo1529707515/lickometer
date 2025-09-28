# lickometer
用于记录小鼠舔舐次数的低成本解决方案
# 舔舐感知系统 - 基于 STM32F103C8T6 与 TTP224

本项目旨在通过串口通信实现舔舐动作的感知与数据标记，包含上位机数据采集程序和 STM32 固件工程两部分。系统基于 **STM32F103C8T6** 单片机与 **TTP224 触摸传感器**。

---

##  项目结构

├── 舔舐感知上位机 上位机数据采集与标记程序（Python）  
├── UARTNEW STM32 工程文件（Keil 与 STM32CubeMX 工程）  
├── README.md  项目说明文件


---

##  硬件平台

- 主控芯片：STM32F103C8T6  
- 感知模块：TTP224 电容触摸传感器  
- 通信方式：UART 串口通信  

## 使用说明
### 1. 舔舐感知上位机（数据采集与标记）
连接 STM32 开发板（确保使用的是对应串口）

进入虚拟环境并运行：python main.py
按照程序界面指引进行数据采集和标记。

### 2. UARTNEW（STM32 工程）
使用 Keil uVision 或 STM32CubeIDE 打开该工程文件夹  
编译工程  
通过 ST-Link 或 USB-TTL 烧录到 STM32F103C8T6 开发板  
确保波特率设置与上位机程序一致（115200）
连接 STM32 开发板（确保使用的是对应串口） 
### 3.注意配置好接线
VCC--3.3V  
GND--GND  
A01(PA1)--OUT1   
A02(PA2)--OUT2  
A03(PA3)--OUT3  
A04(PA4)--OUT4   
## 串口配置建议
参数	设置值  
波特率	115200  
数据位	8  
停止位	1  
校验位	无  
流控	无  
# lickometer
A low-cost solution for recording mouse licking events

# Lick Detection System - Based on STM32F103C8T6 and TTP224
This project is designed to detect licking actions and record data through UART serial communication. It includes a PC-based data acquisition and labeling program as well as an STM32 firmware project. The system is based on the **STM32F103C8T6** microcontroller and the **TTP224 capacitive touch sensor**.

## Project Structure
├── Lickometer_PC   PC program for data acquisition and labeling (Python)  
├── UARTNEW         STM32 firmware project (Keil and STM32CubeMX)  
├── README.md       Project documentation  

## Hardware Platform
- MCU: STM32F103C8T6  
- Sensor: TTP224 capacitive touch sensor  
- Communication: UART serial communication  

## Usage Instructions
### 1. Lickometer PC Program (Data Acquisition and Labeling)  
Connect the STM32 development board (make sure the correct COM port is used).    
Activate the virtual environment and run:  

python main.py  
Follow the program instructions to collect and label data.↳  

### 2. UARTNEW (STM32 Project)
Open the project with Keil uVision or STM32CubeIDE.
Compile the project.
Flash the firmware to the STM32F103C8T6 development board using ST-Link or USB-TTL.
Ensure the baud rate matches the PC program (115200).
Connect the STM32 development board (make sure the correct COM port is used).

### 3. Wiring Notes
VCC → 3.3V
GND → GND
A01 (PA1) → OUT1
A02 (PA2) → OUT2
A03 (PA3) → OUT3
A04 (PA4) → OUT4

# Recommended UART Configuration
Parameter	Value
Baudrate	115200
Data bits	8
Stop bits	1
Parity	None
Flow ctrl	None
