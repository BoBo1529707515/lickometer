#ifndef __BSP_TOUCHKEY_H
#define __BSP_TOUCHKEY_H

#include "stm32f1xx_hal.h"  // ??HAL????

// ????????(????????)
#define TOUCH_PORT        GPIOA
#define TOUCH_PIN_1       GPIO_PIN_1
#define TOUCH_PIN_2       GPIO_PIN_2
#define TOUCH_PIN_3       GPIO_PIN_3
#define TOUCH_PIN_4       GPIO_PIN_4

// ????
void TTP224_GPIO_Init(void);
uint8_t Key_IN1_Scanf(void);
uint8_t Key_IN2_Scanf(void);
uint8_t Key_IN3_Scanf(void);
uint8_t Key_IN4_Scanf(void);

#endif /* __BSP_TOUCHKEY_H */