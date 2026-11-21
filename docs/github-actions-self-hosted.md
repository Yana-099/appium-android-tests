# Запуск Android UI-тестов из GitHub Actions на своём ПК

Workflow `.github/workflows/android-self-hosted.yml` запускается вручную из вкладки **Actions** в GitHub. Тесты исполняются на вашем компьютере, поэтому используют уже настроенные Android-эмулятор, ADB и Appium Server.

## Однократная настройка runner

1. Откройте GitHub-репозиторий: **Settings → Actions → Runners**.
2. Нажмите **New self-hosted runner**.
3. Выберите **Windows** и **x64**.
4. Выполните команды, которые покажет GitHub, в отдельной папке runner на вашем ПК.
5. При настройке добавьте пользовательскую метку `appium`. Workflow ожидает метки `self-hosted`, `windows` и `appium`.
6. Запустите runner командой `run.cmd` и оставьте это окно открытым на время выполнения workflow.

## Требования к ПК

- Android-эмулятор `emulator-5554` запущен и отображается в `adb devices`.
- Appium Server запущен по адресу `http://127.0.0.1:4723`.
- ADB доступен через переменную окружения `PATH` для учётной записи, из-под которой запущен runner.

## Запуск workflow

1. Откройте вкладку **Actions** в репозитории.
2. Выберите workflow **Android UI tests (self-hosted)**.
3. Нажмите **Run workflow**.
4. Выберите группу тестов: `smoke`, `regression`, `negative` или `known_bug`.
5. После завершения скачайте артефакт `allure-and-artifacts-<номер запуска>` с Allure-результатами и скриншотами.

`crash_demo` намеренно завершается с ошибкой и не включён в workflow. Его запускают только локально с флагом `--run-crash-demo`.
