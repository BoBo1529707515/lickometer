
#include "bsp_touchkey.h"

void TTP224_GPIO_Init(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    

    __HAL_RCC_GPIOA_CLK_ENABLE();
    
   
    GPIO_InitStruct.Pin = TOUCH_PIN_1 | TOUCH_PIN_2 | TOUCH_PIN_3 | TOUCH_PIN_4;
    GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
    GPIO_InitStruct.Pull = GPIO_PULLDOWN;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    
    HAL_GPIO_Init(TOUCH_PORT, &GPIO_InitStruct);
}

uint8_t Key_IN1_Scanf(void)
{
    return HAL_GPIO_ReadPin(TOUCH_PORT, TOUCH_PIN_1);
}


uint8_t Key_IN2_Scanf(void)
{
    return HAL_GPIO_ReadPin(TOUCH_PORT, TOUCH_PIN_2);
}


uint8_t Key_IN3_Scanf(void)
{
    return HAL_GPIO_ReadPin(TOUCH_PORT, TOUCH_PIN_3);
}


uint8_t Key_IN4_Scanf(void)
{
    return HAL_GPIO_ReadPin(TOUCH_PORT, TOUCH_PIN_4);
}
