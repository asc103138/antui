---
name: antigravity-windows-boot-diagnostics
description: 奕鈞老師 Windows 開機與登入後效能診斷 Skill（15-windows-boot-diagnostics / windows-boot-diagnostics）——安全診斷 Windows 開機與登入後變慢原因。當使用者提到「Windows開機慢」「開機診斷」「登入後很卡」「桌面跑很久」「檢查開機速度」「開機很久」「排查開機問題」「開機效能」「windows-boot-diagnostics」「boot diagnostics」時載入。以事件紀錄（Diagnostics-Performance 100/101/108/110）、啟動來源（Run/排程/服務）、系統負載（CPU/RAM/Disk）、Defender、TPM、Google Drive 等可重現證據分析，提出安全、可復原的優化建議。Diagnose slow Windows startup and post-login sluggishness with read-only evidence from boot performance events, startup entries, scheduled tasks, services, Windows Update, Defender, Google Drive, Phone Link/cross-device components, TPM, crash logs, storage, and live resource usage.
---

# Windows Boot Diagnostics（Windows 開機診斷 Skill）

> **奕鈞老師數位教學備課室** ｜ 專案來源：<https://ijun-ai.com/app/windows-boot-diagnostics/>  
> 適用於 Google Antigravity、Claude Code、OpenCode 及各類 AI Coding Agent

---

## 核心設計精神與安全紅線（Core Principles & Safety Rules）

1. **先回答「慢在哪裡」，再決定要不要關閉**：
   - 嚴格區分「BIOS／主機板廠牌畫面卡住」、「進入桌面後滑鼠轉圈／不能操作」與「特定軟體啟動後當機」，不盲目把問題全推給開機啟動程式。
2. **證據 → 風險 → 可復原調整 → 重新開機驗證**：
   - 預設一律採**唯讀檢測（Read-Only Audit）**。
   - 未經使用者明確授權前，**嚴禁**擅自停止程序、停用服務、修改機碼、刪除檔案、加入防毒排除或強制重啟。
   - 任何變更必須保留**原始數值與復原指令**，每次僅調整一個最小邏輯群組，並重開機驗證。
3. **日常最易誤判項目與高風險紅線**：
   - **Google Drive**：若為日常同步工具，優先排查同步模式（串流 vs 鏡像）、離線檔案、頻寬設定，**絕不直接建議停用**或刪除未同步快取。
   - **手機連結 / 跨裝置服務（CrossDeviceService, CDPUserSvc, cbdhsvc）**：牽涉剪貼簿歷史、鄰近分享與多裝置協作，先確認需求，不承諾可完全移除。
   - **Intel TPM Provisioning Service**：與安全性、Windows Hello、BitLocker 綁定，**嚴禁當作一般加速項目停用，更不可清除 TPM**。
   - **Defender 即時防護與竄改防護**：不可繞過或永久關閉；若需白名單僅限狹窄且受信任的專案目錄。
   - **重開機驗證**：必須採計真實完整重新開機（Kernel-General 12/13、EventLog 6005/6006 且產生新 Event 100），**不得將睡眠喚醒（Wake-from-sleep）當成新測試**。

---

## Operating rules

- Match the user's language and explain technical findings in plain language.
- Start with a read-only audit. Do not stop processes, disable services, edit the registry, add Defender exclusions, uninstall software, reboot, or delete files unless the user explicitly authorizes that specific action.
- Use administrator elevation only when needed to read protected event logs, service configuration, Defender status, TPM status, or WER metadata. Explain why elevation is needed.
- Treat a command that returns success as insufficient evidence. Verify the resulting state after every authorized change and after the next complete reboot.
- Never bypass Tamper Protection, Defender safeguards, BitLocker, TPM protections, UAC, or endpoint-management policy. If Windows blocks a requested security change, report that fact and use an official UI or a safer alternative.
- Preserve exact names, paths, previous startup types, previous task states, and registry values before changing anything. Prefer disabling one identified item over a broad “clean boot.”
- Separate observations, likely causes, and hypotheses. A process appearing in Event 101 is evidence of boot-time delay, not proof that it caused a crash.

## Standard workflow

### 1. Establish the symptom and a valid baseline

1. Record the current time, computer model, Windows version, last boot time, memory, C: free space, physical-disk health, and whether the user means pre-desktop delay or post-desktop unresponsiveness.
2. Determine whether the machine completed a real restart. Correlate `Win32_OperatingSystem.LastBootUpTime` with System events: shutdown/start markers (`Kernel-General` 13/12, `EventLog` 6006/6005), `Kernel-Boot`, and `Power-Troubleshooter`. Treat wake-from-sleep or hibernation as a separate path. Do not report a new boot result unless a new Diagnostics-Performance Event 100 exists after the reboot marker.
3. Read Diagnostics-Performance Event 100 and parse `Boot Duration`, `MainPathBootTime`, and `BootPostBootTime`. Use Event 101 for slow applications and Events 108/110 for policy or session-manager delays. Report milliseconds as seconds.
4. Compare the newest valid boot with 5–20 earlier valid boots. Use the same metric each time. A useful comparison is:

   | Metric | Interpretation |
   |---|---|
   | `MainPathBootTime` | Pre-desktop system path; firmware, drivers, services, and shell initialization. |
   | `BootPostBootTime` | Work still occurring after the desktop appears; usually the user's complaint. |
   | Event 101 `DegradationTime` | A component that Windows recorded as slower than its baseline. |
   | System Event 7009 | A service startup timeout; treat the timeout duration as material evidence. |

If the Diagnostics-Performance log is inaccessible, retry the same read-only query with elevation or `wevtutil`; do not infer timing from the clock alone.

### 2. Collect evidence in layers

Use the bundled `scripts/collect_boot_diagnostics.ps1` for a repeatable snapshot. Run it from an elevated PowerShell session when possible; it is read-only and emits JSON to standard output unless `-OutputPath` is supplied.

Collect, in this order:

1. **Boot and crash evidence**: Diagnostics-Performance, System, Application, Windows Error Reporting, WHEA, display-driver events, Event 41/6008, Application Error 1000, Application Hang 1002, and recent minidump metadata. Distinguish an app hang from a blue screen or abrupt power loss.
2. **Startup sources**: HKCU/HKLM/WOW6432 `Run` values, per-user and common Startup folders, `Win32_StartupCommand`, and enabled logon/boot scheduled tasks. Record command, target path, publisher if available, and whether the target exists. A missing target is a stale entry, not a reason to uninstall a surviving product.
3. **Services**: automatic services, service paths, state, start account, dependencies, and Service Control Manager 7000/7009 events. Identify third-party services separately from Windows security, storage, networking, audio, input, and device services.
4. **Current load**: three one-second samples of CPU, available memory, physical-disk time, and disk queue; top memory/CPU processes; SSD health and C: free space. A healthy idle snapshot does not invalidate a boot-time event.
5. **Targeted components**: Defender state and scheduled-scan settings; Windows Update/BITS status and recent update events; Google Drive processes and mount/sync state; Phone Link/cross-device processes and per-user services; TPM status and Intel/firmware service details.

### 3. Classify the cause before recommending changes

Classify findings into one or more of these buckets:

- **One-time Windows work**: Windows Update, .NET optimization, component servicing, signature updates, or post-update Defender work. Validate after the update completes and after another complete reboot.
- **Recurring security or file-scan work**: `MsMpEng.exe` or Defender file-filter events. Distinguish scheduled scans from always-on real-time protection. Do not call a Defender Event 101 a “scheduled scan” without checking the task and Defender state.
- **Required synchronization**: Google Drive, OneDrive, or another required sync client. Keep required sync enabled; optimize scope, cache, mode, bandwidth, and timing instead of disabling it.
- **Optional startup load**: browsers, launchers, tray utilities, update helpers, device utilities, and editors. Ask whether the user needs the function, not whether the executable looks familiar.
- **Stale or broken registration**: an auto-start value or service points to a missing executable, or an old version coexists with a newer updater. Verify exact paths before disabling only the stale registration.
- **Service/driver/firmware timeout**: SCM 7000/7009, TPM, Intel CSME, storage, graphics, or device initialization. Prefer vendor driver/BIOS repair over disabling a security or hardware service.
- **Application crash or hang**: correlate the user's action time with Application 1000/1001/1002, WER reports, loaded module, and security-filter events. Do not blame the last startup program without correlation.

### 4. Give a ranked recommendation

For each finding, report: evidence, confidence, user-visible impact, recommendation, risk, and rollback. Use three groups:

- **Safe now**: wait for an update to finish, close unused apps, reduce optional startup entries, fix stale registrations, or adjust Google Drive bandwidth/sync scope.
- **Needs user choice**: stop a required sync client, remove Phone Link features, disable an updater, add a Defender exclusion, or change a service start type.
- **Do not disable as a first step**: Defender real-time protection, TPM/Intel TPM provisioning, BitLocker, Windows Update core services, storage drivers, firewall, and core networking.

### 5. Apply only explicitly authorized reversible changes

Before changing an item:

1. State the exact target, what function will stop, what will remain, and how to restore it.
2. Capture its previous state. For a Run value, save registry path/name/value; for a task, save enabled/disabled state; for a service, save start type and running state.
3. Change one logical group at a time. Do not mix Defender, TPM, startup values, and third-party services in one opaque command.
4. Verify immediately, then ask the user to perform a complete restart if boot timing is the goal.
5. Re-run the same diagnostics and compare the same metrics. Do not call the work improved until a valid new Event 100 exists.

For startup entries, remove only the startup registration, not the application. For stale service registrations, disable first; delete a service registration only if the user explicitly requests cleanup, the executable is confirmed missing, and the exact service is isolated from newer versions.

## Component-specific guidance

### Defender

- Keep real-time protection, behavior monitoring, IOAV/download scanning, cloud protection, and Tamper Protection on by default.
- The scheduled Defender scan is separate from real-time protection. Disabling the scheduled task does not stop `MsMpEng.exe` from scanning files as they open or execute.
- If the user requests a temporary test, use Windows Security UI, explain the exposure, do not bypass Tamper Protection, and restore real-time and Tamper Protection immediately after the test or at the next safe checkpoint.
- For a trusted development workload, prefer a narrowly scoped exclusion only after confirming the exact project path and trust boundary. Never exclude an entire drive, Downloads, temporary folders, or Google Drive broadly.

### Google Drive

- Do not disable Google Drive when the user requires it. Check whether the account uses streaming or mirroring, how many folders are offline, whether sync is active, and where the local cache resides.
- Suggest limiting bandwidth only if Drive is starving other work; a too-low limit makes sync slower. Keep cache on a local healthy SSD and do not delete the cache while unsynced changes exist.
- Reduce unnecessary mirrored/offline folders and backup sources. Pause sync during heavy builds, then resume and confirm “up to date.”
- Distinguish Drive's startup delay from current sync activity; a large initial file set can dominate post-boot work.

### Phone Link and cross-device services

- `CrossDeviceService.exe`, `PhoneExperienceHost.exe`, `CDPSvc`, `CDPUserSvc_<id>`, and `cbdhsvc_<id>` cover more than phone linking: connected devices, cross-device experiences, and clipboard scenarios.
- To stop phone-related background behavior, unlink the phone, turn off Android “Link to Windows,” and set Phone Link background permission to Never where the Windows build exposes it.
- Do not promise that Phone Link can be fully uninstalled; it is integrated into Windows. Disabling per-user services can also remove clipboard history/sync, nearby sharing, or other connected-device features. Explain the tradeoff before making that change.

### TPM and Intel TPM Provisioning Service

- The service is not the TPM hardware. `Get-Tpm` should be used to check `TpmPresent`, `TpmReady`, `TpmEnabled`, and `TpmActivated`.
- Do not disable TPM or its provisioning service as a first response to a 7009 timeout. TPM supports BitLocker/device encryption, Windows Hello, measured boot, credential protection, certificates, and device health attestation.
- A repeated Intel TPM provisioning timeout plus TPM Event 17 indicates a firmware/driver/TPM-command problem hypothesis. Check BitLocker state, Windows Hello use, BIOS/UEFI version, Intel CSME/Management Engine driver, and OEM firmware notes. Use the computer manufacturer's support page, not a random driver site.
- If a controlled diagnostic test of the service start type is explicitly authorized, record the original Auto state, prefer Manual over Disabled, test one reboot, and restore Auto if TPM/Hello/BitLocker behavior changes. Never clear the TPM as a troubleshooting shortcut; clearing it can make protected data or sign-in credentials inaccessible.

### Windows Update and stale updaters

- Record update IDs and whether installation completed. Do not diagnose a permanent startup regression while a cumulative update is installing or servicing the component store.
- For an updater service, verify the executable path and version. If version 136 is missing but version 152 exists, a 136 service is stale evidence; preserve the current version and Google Drive. Disable only the confirmed stale registration after authorization.
- A service that is stopped but Auto-start and repeatedly generates 7009 can still delay startup; distinguish it from a healthy stopped Manual service.

## Crash and project-run handling

When the user says “the project crashed”:

1. Ask for the approximate time and whether Windows, the IDE, the terminal, or the whole desktop stopped responding.
2. Read Application Hang 1002, Application Error 1000, WER 1001, System Event 41/6008, WHEA, display-driver events, and minidump metadata.
3. Correlate the faulting executable and module with the project action. A Codex/ChatGPT app hang is not the same as a project runtime crash.
4. If a Defender `WdFilter` event is present, describe it as a correlation or possible file-filter interaction, not proof of causality. Test one variable at a time and restore security protection promptly.
5. Preserve dumps and WER reports. Do not delete them during diagnosis.

## Required handoff format

Return a compact, evidence-backed report containing:

1. **Result**: improved, unchanged, inconclusive, or blocked.
2. **Valid boot comparison**: newest complete reboot versus prior baseline, with total, pre-desktop, and post-desktop times.
3. **Top causes**: each with process/service, measured delay, recurrence, and confidence.
4. **Health checks**: storage, memory, current load, crash evidence, Defender, updates, Drive, cross-device, and TPM.
5. **Changes made**: exact targets and verified post-change state; say explicitly when nothing was changed.
6. **Next steps**: ranked, reversible, and tied to the user's priorities.

Never report a sleep/wake measurement as a reboot result, and never call a preparation step, draft, or unverified change “complete.”

## Bundled resources

- `scripts/collect_boot_diagnostics.ps1`: read-only Windows snapshot script. Use it for the first evidence pass or when a repeatable artifact is useful.
- `references/interpretation.md`: event IDs, component mappings, safety boundaries, and additional checks.
