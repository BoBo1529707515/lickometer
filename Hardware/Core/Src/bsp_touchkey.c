#include "bsp_touchkey.h"

// ?????
void TTP224_GPIO_Init(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    
    // ????8???????
    GPIO_InitStruct.Pin = TOUCH_PIN_1 | TOUCH_PIN_2 | TOUCH_PIN_3 | TOUCH_PIN_4 |
                          TOUCH_PIN_5 | TOUCH_PIN_6 | TOUCH_PIN_7 | TOUCH_PIN_8;
    
    GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
    GPIO_InitStruct.Pull = GPIO_PULLUP;  // ?????????????
    
    HAL_GPIO_Init(TOUCH_PORT, &GPIO_InitStruct);
}

// ??1????
uint8_t Key_IN1_Scanf(void)
{
    return HAL_GPIO_ReadPin(TOUCH_PORT, TOUCH_PIN_1);
}

// ??2????
uint8_t Key_IN2_Scanf(void)
{
    return HAL_GPIO_ReadPin(TOUCH_PORT, TOUCH_PIN_2);
}

// ??3????
uint8_t Key_IN3_Scanf(void)
{
    return HAL_GPIO_ReadPin(TOUCH_PORT, TOUCH_PIN_3);
}

// ??4????
uint8_t Key_IN4_Scanf(void)
{
    return HAL_GPIO_ReadPin(TOUCH_PORT, TOUCH_PIN_4);
}

// ??5???? (??)
uint8_t Key_IN5_Scanf(void)
{
    return HAL_GPIO_ReadPin(TOUCH_PORT, TOUCH_PIN_5);
}

// ??6???? (??)
uint8_t Key_IN6_Scanf(void)
{
    return HAL_GPIO_ReadPin(TOUCH_PORT, TOUCH_PIN_6);
}

// ??7???? (??)
uint8_t Key_IN7_Scanf(void)
{
    return HAL_GPIO_ReadPin(TOUCH_PORT, TOUCH_PIN_7);
}

// ??8???? (??)
uint8_t Key_IN8_Scanf(void)
{
    return HAL_GPIO_ReadPin(TOUCH_PORT, TOUCH_PIN_8);
}