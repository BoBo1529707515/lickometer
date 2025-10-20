#ifndef __BSP_TOUCHKEY_H
#define __BSP_TOUCHKEY_H

#include "stm32f1xx_hal.h"

// ???8?????? (????????)
#define TOUCH_PORT        GPIOA
#define TOUCH_PIN_1       GPIO_PIN_1
#define TOUCH_PIN_2       GPIO_PIN_2
#define TOUCH_PIN_3       GPIO_PIN_3
#define TOUCH_PIN_4       GPIO_PIN_4
#define TOUCH_PIN_5       GPIO_PIN_5  // ????5
#define TOUCH_PIN_6       GPIO_PIN_6  // ????6
#define TOUCH_PIN_7       GPIO_PIN_7  // ????7
#define TOUCH_PIN_8       GPIO_PIN_8  // ????8

// ????
void TTP224_GPIO_Init(void);
uint8_t Key_IN1_Scanf(void);
uint8_t Key_IN2_Scanf(void);
uint8_t Key_IN3_Scanf(void);
uint8_t Key_IN4_Scanf(void);
uint8_t Key_IN5_Scanf(void);  // ????5????
uint8_t Key_IN6_Scanf(void);  // ????6????
uint8_t Key_IN7_Scanf(void);  // ????7????
uint8_t Key_IN8_Scanf(void);  // ????8????

#endif /* __BSP_TOUCHKEY_H */