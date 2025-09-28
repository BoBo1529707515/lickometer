#ifndef __BSP_TOUCHKEY_H
#define __BSP_TOUCHKEY_H

#ifdef __cplusplus
extern "C" {
#endif

#include "main.h"

// ???? (?gpio.c??????)
#define TOUCH_KEY1_PIN      GPIO_PIN_1
#define TOUCH_KEY1_PORT     GPIOA
#define TOUCH_KEY2_PIN      GPIO_PIN_2
#define TOUCH_KEY2_PORT     GPIOA
#define TOUCH_KEY3_PIN      GPIO_PIN_3
#define TOUCH_KEY3_PORT     GPIOA
#define TOUCH_KEY4_PIN      GPIO_PIN_4
#define TOUCH_KEY4_PORT     GPIOA

// ???????
void TTP224_GPIO_Init(void);

// ????????
uint8_t Key_IN1_Scanf(void);
uint8_t Key_IN2_Scanf(void);
uint8_t Key_IN3_Scanf(void);
uint8_t Key_IN4_Scanf(void);

#ifdef __cplusplus
}
#endif

#endif /* __BSP_TOUCHKEY_H */