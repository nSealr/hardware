# Two-host firmware owner, update and reset contract

Author `/root/h01_sol`, 20 October 2026, after `77310fc`. This is the finite C04
paper policy and source correspondence, not a bootloader, provisioned device,
accepted root/key, successful update or custody qualification. Every hardware,
entropy, transport, display and power pre-use stop remains. No command or secret
for a provisioning ceremony is supplied, and no irreversible action is authorized.

P01 PROD-03/11 and recovery §95 distinguish local `nsec` recovery from persistent
custody, assigned to D02/S04. H01 does **not** invent a PIN/password vault, AEAD
format or selected-SE service. The host qualification workload uses public
fixtures/disposable identities and explicitly cleared internal session memory.
Persistent Signer identity/PIN/storage remains a D02/S04/H02S/K01 stop before
use, not a first-release waiver. XTS encryption is not authenticated custody,
PIN enforcement, operation binding or protection from trusted-firmware memory
corruption. The generic SDK is independently programmable and Nostr-free; a
qualified Signer is a separately enforced configuration of one trusted image.

## States and permitted authority

| State | Permitted behavior | Boundary and transition requirement |
| --- | --- | --- |
| Developer | Disposable/public fixtures; inspect/program/debug owner firmware through the exact supported kit routes. No production identities or claims about protected custody. | Open debug, ROM logs/download and changed startup can expose all state. Clear framing/epochs after boot text; never mix logs with an accepted application stream. Record exact flags and resource owners. |
| Prepared owner candidate | Offline owner roots, prospective option/eFuse state, boot image, bounded update path and recovery are reviewable artifacts only. | Effective binary/map, source/hardware/entropy/power prerequisites and a separately authorized sacrificial provisioning procedure must pass before any transition. Security-enabled first boot can program fuses automatically; it is not an ordinary H02 flash/run. |
| Owner-secured proposal | Only the declared owner boot/image authority; exact debug/download/print restrictions and rollback policy. Fresh local session/recovery import is distinct from firmware authorization. | This state has not been reached or tested. A fuse/RDP label does not qualify firmware, display, entropy, persistent identity or physical-attacker resistance. Any mismatched field/root/ROM refuses before secrets. |
| Update pending | Cancel all operations, clear session material, blank and enter a dedicated locally acknowledged update flow. Accept only bounded signed firmware under the separate owner authority. | No Nostr operation, identity import/export, PIN-vault service or secrets load during validation, rollback self-test, interrupted state or floor commitment. Normal USB input does not authorize an update. |
| Recovery | Run only the authenticated fixed recovery/update authority; restore firmware at or above the committed security floor, then fresh reset and complete qualification. | No unsigned maintenance image, ROM `Go`, lowered counter, alternate transport/provider or persistent-custody fallback. A blocked recovery may require destructive reprovisioning or unit retirement. |
| Product-qualified Signer | Only after all independent semantic/source/effective-build/UI/custody/physical/release gates. | This is not another RDP/eFuse value and is not claimed by any H01 state. Generic owner firmware does not inherit it. |

## U585 fixed boot and flash proposal

Propose TZEN1, RDP level1 (neither0.5 nor2), BOOT_LOCK1 and
SECBOOTADD0 field=`0x0180000`, corresponding to secure address`0x0C000000`.
BOOT_LOCK forces that entry independently of BOOT0/NSWBOOT0. Preserve the
other option fields deliberately rather than copying a whole example word.
DUALBANK1/SWAP_BANK0, SRAM2_RST0/SRAM_RST0 and SRAM2_ECC0/SRAM3_ECC0 have the
previously recorded erase/ECC polarities. Ordinary reset does not erase OTP,
backup SRAM/registers, external memory or panel GRAM; no secret is allocated
there. DHUK is unused; the common RDP0 DHUK is never device-unique custody.

Two independent64-bit OEM1/OEM2 regression credentials are future off-device
owner-recovery material, separate from the identity, boot signing key and each
other. Proposed OEM1LOCK1/OEM2LOCK1 restrict level1→0 and level1→0.5 respectively.
LOCK0 means unrestricted corresponding regression, not a stronger lock. Key
registers read zero and are not credential readback. No all-zero/all-one
credential is valid. Actual credential generation, option modification/reload,
challenge and interruption recovery need separate authorized qualification.

The following physical flash ranges are a **capacity/ownership proposal** for
the2MiB U585. Secure aliases add`0x04000000`; page size8192 bytes. Nothing here
claims the linked boot/app fits, an image is installed or a journal implemented.

| Range, end excluded | Size / owner | Required protection |
| --- | --- | --- |
|0x08000000–0x08040000 |256KiB owner boot verifier/recovery and public roots | Bank1 WRP1A pages0..31, UNLOCK0; no mutable data in this range. |
|0x08040000–0x08044000 |Two8KiB boot-only version/floor journal pages32/33 | Mutable only before hide closure; not WRP, both within HDP1. |
|0x08044000–0x08060000 |112KiB unallocated | No identity/policy secret or executable feature assumed. |
|0x08060000–0x08100000 |640KiB app slotA | Signed for secure load/entry address0x0C060000; no bank swap. |
|0x08100000–0x081A0000 |640KiB app slotB | Signed for secure load/entry address0x0C100000; distinct link image, not a relocated slotA assumption. |
|0x081A0000–0x08200000 |384KiB unallocated | No future SDK/storage capacity claim without another map/budget. |

Both banks' secure watermarks cover pages0..127. HDP1EN1/HDP1_PEND33,
SECWM1_PSTRT0 therefore hides the first34 pages (272KiB), including the boot
root and two journal pages. HDP2 is unused. Secure firmware must establish and
verify attribution, root/slot/floor validity and the protected transition,
then close HDP1 with HDP1_ACCDIS before application entry. Closing prevents
read/write/erase/execute and freezes the corresponding HDP/watermark settings
until system reset. A reviewed RAM transition/call sequence and cache/entry
handling are H02 implementation gates; no hidden-root helper is assumed correct.
WRP UNLOCK0 cannot be undone merely by secure application code; full RDP
regression to0 is the documented unlock path.

RM0456 p310's numerical HDP example does not match its stated start/end pages.
The allocation above uses the current inclusive SECWM/HDP fields and Tables60/61,
not that example. It is not an observed option-byte or hidden-region result.

Use the already accepted maintained k2560.14.0 raw BIP340 verification route as
the **paper software verifier hypothesis**, with a separate offline firmware
owner key and domain-separated canonical image manifest binding exact target,
slot/load/entry/length, digest and monotonic security version. It does not reuse
the Nostr identity as a firmware root. Exact manifest encoding, trusted code/
backend footprint, immutable-root audit and complete verified boot/update call
path remain H02 prerequisites; an unsigned header/version or API success flag
does not authenticate an image. No new cryptographic backend/algorithm lead is
opened, and no supported signed-update implementation is claimed.

The version journal must persist and verify an update's raised floor **before**
activation or any operation under the new version. On reset, never fall back to
an otherwise valid old image below that floor. A floor without a complete new
image enters authenticated recovery. Redundant records need canonical validation,
sequence/version/target/hash correspondence, full checked readback and a power-
interruption protocol. Copy/verify the only authoritative floor before erasing
its page. ECC/error/partially programmed or ambiguous floor state fails closed;
do not select a smaller floor simply because it is the surviving readable record.
If the floor cannot be recovered safely, destructive owner recovery is required.

Programming is16-byte quad-word and erase is8KiB page work; same-bank stalls,
FLASH_OPSR/error/ECC inspection after reset and complete affected-page recovery
remain mandatory. No interrupted write is atomic, no all-ones read alone proves
virginity, and no journal/slot operation runs across a long masked section or
feeds the watchdog without verified progress. C09 supplies actual rail/write
permission and H02/H03 must test each activation/erase/program/GC interruption.

Owner-root replacement on U585 uses authenticated **destructive** full RDP1→0
regression and re-establishment of new owner roots/options/credentials. It does
not retain a privileged session. The manual erases main flash, SRAMs and listed
cache/backup/OTFDEC/PKA state, while OTP survives; all surviving option/device
state must be read and deliberately reconciled, not assumed zero. OEM credentials
can be changed at RDP0 even when previously locked. RDP1→0.5 preserves secure
watermark flash and is **not** fresh-owner replacement. RDP2→1 likewise does
not erase application code; neither transition is selected here. Loss of the
necessary credential/root can prevent recovery; local identity backup is a
different recovery requirement.

ROM entry in development has AN2606's exact overlapping pins/radios and watchdog
behavior; sensitive display remains externally blank. Owner operation never
returns through ROM `Go`: only a fresh trusted reset reestablishes ownership.
ROM's periodic IWDG feed is not application health or a way to recover a blocked
owner updater. No manufacturer-ROM firmware-authentication guarantee substitutes
for the proposed owner verifier.

## S3 owner values, roots and finite limits

The owner hypothesis retains fixed USJ only if its independent C07/C09 source,
descriptor and power gates close. Required readback values include:

| Field/policy | Paper owner requirement |
| --- | --- |
| Secure Boot v2 |SECURE_BOOT_EN1; ROM and second-stage RSA-3072 PSS/SHA256, MGF1 and32-byte salt; only owner roots, no public/developer keys. |
| Flash encryption |XTS-AES256 only: two separate256-bit secret key blocks with purposes2 and3, no purpose4 AES128 key. SPI_BOOT_CRYPT_CNT7 (three set bits, odd) and write protection. Neither an “enabled” bit nor a helper accepting one found key substitutes for exact required-pair readback. |
| Key allocation |BLOCK_KEY0/1 purposes2/3, read+write protected; BLOCK_KEY2/3/4 public boot digests purposes9/10/11, write protected **readable**. KEY5 remains unused purpose0, no secret; prevent later purpose/root substitution. Protect purpose fields and establish all required read-protected keys before locking RD_DIS. |
| Initial boot roots |Three independently generated owner-controlled offline RSA private keys; only their digests on device. Initial fixed second-stage bootloader is signed by all three; ordinary app by the current key. No vendor/manufacturer update root is implied. Third digest slot is not a third SE. |
| Revocation |Propose SECURE_BOOT_AGGRESSIVE_REVOKE1, initial revoke0/1/2 clear and not prematurely write-locked. Invalid verification can permanently consume roots and all roots lost can brick the unit; this negative availability cost needs explicit future review, not hidden recovery. Migrate app and verify the fixed bootloader under a remaining root before revoking the old one. |
| Debug/download |DIS_PAD_JTAG1/DIS_USB_JTAG1, DIS_FORCE_DOWNLOAD1, DIS_DIRECT_BOOT1, DIS_DOWNLOAD_MODE1, both separate Serial/JTAG and OTG download-disable fields1. No HMAC/debug re-enable service. ENABLE_SECURITY_DOWNLOAD0 is no fallback around global download disable. |
| CDC/PHY/cache |DIS_USB_SERIAL_JTAG0, USB_PHY_SEL0/internal PHY with normal GPIO19/20 mapping; debug disable is not whole-CDC disable. DIS_USB_OTG1 excludes the unused OTG block, DIS_APP_CPU0 preserves the silicon option while software holds CPU1 reset/gated. Normal instruction/data caches remain enabled as required by C05; download caches/manual encryption disabled. Verify all grouped fields before lock. |
| Output writers |DIS_USB_SERIAL_JTAG_ROM_PRINT1, UART_PRINT_CONTROL=`11`; both boot/application consoles NONE, secondary NONE, no VFS/REPL/panic/core-dump/trace/debug writer on application stream. Cold ROM suppression must be permanent before an owner secret load. |
| Rollback |CONFIG_BOOTLOADER_APP_ANTI_ROLLBACK and APP_ROLLBACK enabled in the future owner build; full16-bit SECURE_VERSION field, no reduced-size field, emulation, factory or test partition. Security floor is set-bit count, not an arbitrary16-bit binary version. |

These values are requirements, not an executable fuse recipe. The generic
flash-encryption security-check loop iterates purpose2/3/4; its source explicitly
says S3 AES128 and AES256 types are mutually exclusive. Exact two-key presence,
purpose, read/write protection, current encryption count, flash/module voltage
and early boot behavior must agree. A read-protected secret reading as zero is
not evidence of a valid all-zero key. Conversely, read-protecting a boot digest
breaks software verification. No flash-encryption/HMAC key is created here.

WR_DIS2 groups whole-CDC/PHY/JTAG/cache and other fields: establish/verify their
entire intended state before locking. WR_DIS18 also locks SECURE_VERSION;
**it cannot be blanket-locked while future antirollback increments are required**.
Already set disable/print bits are monotonic, but still-writable neighboring
configuration/counter fields and their denial-of-service consequences remain
part of the exact state review. WR_DIS19 is a separate OTG-download/revision
group. Keep revocation write capability until the corresponding planned
revocation; a premature lock defeats that policy. Common first-boot helpers can
burn these fields automatically. H01 never invokes them, flashes a security-
enabled bootloader or treats their defaults as observed provisioning.

S3's16 antirollback bits support at most16 security-floor increments, not an
unlimited monotonic counter. One security version must not authorize a weaker
rollback image; multiple signed images at one floor can still roll among them.
The proposed acceptance policy therefore binds one authorized app content per
security version. Exhaustion is a maintenance limit requiring a new qualified
hardware/ownership decision, not resettable flash metadata. Three immutable
preloaded roots support only that finite planned succession/recovery set;
arbitrary new independent owner-generated roots cannot be promised after lock.
Flash erasure does not erase/reopen eFuse roots, XTS keys, revocations or counters.
Loss/exhaustion of the usable roots can retire the unit. Development before lock
and a subsequent independently owned programmable Board are distinct promises.

## S3 application update and interrupted-state requirements

Use only two OTA app slots and the two-sector8192-byte OTA data partition;
exclude factory/test. A paper8MiB flash reservation leaves128KiB for bootloader
and signatures (partition table at0x20000), OTA data0x21000–0x23000, appA
0x30000–0x330000 and appB0x330000–0x630000 (3MiB each), remaining flash
unallocated. All offsets/secure padding, fixed partition identity, ciphertext/
signature handling and actual bootloader/app fit require generated-map/source
verification before use. This is not the classic ESP32 boot-offset recipe.
No NVS/vault/font/data feature or secret is inferred from the unused capacity.

The pinned OTA documentation distinguishes resilient application-slot update
from **unsafe bootloader, partition-table and other-data update**. This proposal
updates inactive application slots only; the fixed bootloader/partition contract
does not receive an OTA path or assumed atomic rewrite. Exact boot source must
enforce the expected bounded partition/slot identities, signed image, security
version and entry/length policy; an unauthenticated partition-table MD5 or image
length alone is not that enforcement proof. All such source/build changes still
require H02 implementation review, not a new approved driver here.

NEW→PENDING_VERIFY is not acceptance. Run bounded public-data self-tests with
identity import/secret operations disabled. The VALID operation may advance
eFuses; initial erased OTA data with a higher-version image may advance them in
the bootloader too. No normal host probe calls these paths without a separately
authorized irreversible procedure. Only after verified metadata, required
floor readback, reset and complete fresh startup may an accepted version load
session material. A pending-image reboot can roll back only to a still-permitted
authenticated version; no image below the hardware floor is recovery. If no
bootable permitted app remains, report recovery failure/retirement, never bypass
antirollback. Interrupted metadata/fuse/write ambiguity stops before secrets.

The exact pinned helper source does not itself prove a checked floor commit.
`esp_efuse_fields.c` defaults to only four bits without the explicit configuration,
ignores the blob-read return while deriving the set-bit count, and ignores the
blob-write return before reporting an update and returning success. Its three
matching count reads/checks are an additional fault assertion, not an independent
measurement or confirmation that those underlying calls succeeded. The public
blob/count readers in `esp_efuse_api.c` retry damaged readings without a finite
cap; the bit helper can collapse a returned error to false when assertions are
disabled. A false read of a required zero field is not verified owner state.

H02 therefore needs a bounded, error-preserving effective read/commit path with
the exact coding scheme, synchronization/reload/status and fresh floor readback
checked before secret use. Never blindly repeat programming of already set bits
after an ambiguous result. No helper log, `ESP_OK` from the outer function or
three equal values qualifies that path. The utility/HAL/caller chain and effective
configuration have not been completely reviewed; this is a precise source-to-
requirement gap, not an executed failure or an upstream vulnerability finding.

## Reset, ownership transfer and qualification stops

All updates, reset causes, power failures, owner changes and recovery entry cancel
the operation and clear owned parser/result/private row/secret stacks/backend
state before fresh input. U585 system reset and S3 CPU/core/system/RTC/chip reset
have different retention; clearing is explicit across C05's aliases/RTC/backup/
external caches, not inferred from a reset label. The S3 brownout reset-selector
contradiction remains unsatisfied; no dependent reset-scope claim is made. Panel
GRAM and optical state need external blanking/full rewrite before a new review.

Neither host carries privileged identity state silently into different owner
firmware. MCU firmware update authority, local `nsec` backup, device transport
identity, prospective SE pairing/PIN state and vendor SE applet-update authority
are separate. Exact persistent-object destruction/rekey/recovery and one-SE
failure/compromise are still S04/H02S/D02, with the existing access/advisory gates
unchanged. No selected two-SE composition, third SE, persistent vault or custody
guarantee follows from this C04 host table.

H02 must verify the effective boot/helper/config/link/manifest/journal/partition
path and complete flash/image/root/allocator fit, source-defined errors and
every reset/update interruption on identified authorized resources. Public-data
positive/negative cases include bad signatures/target/length/version, wrong key
purpose or missing XTS half, read-protected digest, exhausted floor/root,
unintended first-boot fuse writer, ROM/console output, old pending slot, ambiguous
journal/ECC, stale session and changed owner. No generic USB descriptor, successful
boot/signature or CI flag qualifies these outcomes. C09 normal power/attach,
all source prerequisites and distinct final H01 review remain.

## Actual source scope

This C04 increment rereads RM0456 Rev7 §§3.10.1 pp184–186/Tables21–22,
7.3.1 pp292–293, 7.5.3 pp310–311 and selected current option/protection fields
pp321–324/344–354. Figures25/26 were encountered as extracted text, **not** newly
visually reviewed. S3 TRM1.8 Tables5.3-1/2 pp412–414 and selected fields435–436,
the pinned eFuse CSV's selected shared-lock/key/purpose rows, the versioned
Secure Boot/OTA sections and the common flash-encryption helper410–458 are the
other exact source scopes. Earlier recorded ROM/reset/flash-interruption and
S02 backend evidence is reused, not claimed as a new complete implementation audit.

Newly read pinned source scopes are
[eFuse API lines1–92](https://github.com/espressif/esp-idf/blob/fff9895c82d744c7237be8847347bdd1b07c6643/components/efuse/src/esp_efuse_api.c#L1)
and [eFuse field helpers1–112, selected counter44–95](https://github.com/espressif/esp-idf/blob/fff9895c82d744c7237be8847347bdd1b07c6643/components/efuse/src/esp_efuse_fields.c#L44).
The unrelated short bootloader eFuse locator contains no counter implementation;
it is not counter evidence. Originals/code/extractions remain private; public
metadata and original analysis do not assert target execution or complete SDK audit.
