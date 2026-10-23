/* Public compile-only diagnostic. This image is NOT admitted to a device. */
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

#include "sdkconfig.h"
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"
#include "soc/gpio_reg.h"
#include "soc/efuse_reg.h"

#if !CONFIG_IDF_TARGET_ESP32S3
#error "Only the admitted esp32s3 build is supported"
#endif
#if !defined(BOD_RST_SEL) || (BOD_RST_SEL != 0 && BOD_RST_SEL != 1)
#error "BOD_RST_SEL must be 0 or 1"
#endif
#if defined(CONFIG_ESP_BROWNOUT_DET) || defined(CONFIG_SECURE_BOOT) || defined(CONFIG_SECURE_FLASH_ENC_ENABLED)
#error "No SDK brownout handler or security provisioning in this diagnostic"
#endif

_Static_assert(RTC_CNTL_BROWN_OUT_REG == UINT32_C(0x600080e8), "pinned register address");
_Static_assert(RTC_CNTL_BROWN_OUT_RST_SEL_M == UINT32_C(0x08000000), "TRM selector bit27");
_Static_assert(RTC_CNTL_BROWN_OUT_RST_SEL_S == 27, "TRM selector shift");
_Static_assert(RTC_CNTL_BROWN_OUT_CNT_CLR_M == UINT32_C(0x20000000), "WO counter clear");
_Static_assert(RTC_CNTL_BROWN_OUT_DET_M == UINT32_C(0x80000000), "RO detector status");
_Static_assert(GPIO_STRAP_REG == UINT32_C(0x60004038), "pinned strap address");

/* Keep this real linked writer separately inspectable. It is called below.
 * The intent changes bit27 in a captured raw word. That word includes RO/WO
 * fields: this is not a guarantee about other physical effects or concurrency.
 * The caller refuses an observed1 on WO CNT_CLR rather than echoing that strobe.
 */
__attribute__((noinline, noclone)) uint32_t bod_probe_apply_selector(uint32_t before)
{
    uint32_t intended = (before & ~RTC_CNTL_BROWN_OUT_RST_SEL_M)
        | ((uint32_t)BOD_RST_SEL << RTC_CNTL_BROWN_OUT_RST_SEL_S);
    REG_WRITE(RTC_CNTL_BROWN_OUT_REG, intended);
    __asm__ volatile("memw" ::: "memory");
    return REG_READ(RTC_CNTL_BROWN_OUT_REG);
}

void app_main(void)
{
    uint32_t before = REG_READ(RTC_CNTL_BROWN_OUT_REG);
    uint32_t strap = REG_GET_FIELD(GPIO_STRAP_REG, GPIO_STRAPPING);
    uint32_t cause = REG_READ(RTC_CNTL_RESET_STATE_REG);
    uint32_t print_control = REG_GET_FIELD(EFUSE_RD_REPEAT_DATA3_REG, EFUSE_UART_PRINT_CONTROL);
    uint32_t live0 = REG_READ(GPIO_IN_REG) & 1U;
    uint32_t live46 = (REG_READ(GPIO_IN1_REG) >> (46 - 32)) & 1U;
    printf("public_probe selector=%u before=%08" PRIx32 " strap=%08" PRIx32
           " reset_raw=%08" PRIx32 " gpio0=%" PRIu32 " gpio46=%" PRIu32
           " uart_print=%" PRIu32 " no_bench_admission=1\n",
           (unsigned)BOD_RST_SEL, before, strap, cause, live0, live46, print_control);
    if ((before & RTC_CNTL_BROWN_OUT_CNT_CLR_M) || print_control == 1U
        || print_control == 2U || !live0 || !(strap & (1U << 3))) {
        puts("public_probe refused_context; no selector write requested");
        return;
    }
    uint32_t after = bod_probe_apply_selector(before);
    printf("public_probe after=%08" PRIx32 " requested=%u observed=%" PRIu32
           " xor_raw=%08" PRIx32 " not_armed_by_this_probe=1 hardware_state_unknown=1\n",
           after, (unsigned)BOD_RST_SEL, (after & RTC_CNTL_BROWN_OUT_RST_SEL_M) >> 27,
           before ^ after);
    /* No threshold/enable/interrupt/stimulus/watchdog/fuse/flash operation.
     * Returning does not attest reset scope, a safe rail or disabled hardware.
     */
}
