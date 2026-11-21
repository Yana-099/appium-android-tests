# Руководство по участию в проекте

Этот документ помогает подготовить окружение, запустить тесты и оформить изменения в проекте.

## 1. Подготовка проекта

Склонируйте репозиторий и перейдите в папку проекта:

```powershell
git clone https://github.com/Yana-099/appium-android-tests.git
cd appium-android-tests
```

Создайте и активируйте виртуальное окружение:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Установите зависимости:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 2. Подготовка Android-окружения

Перед запуском убедитесь, что установлены Android SDK и Appium.

Запустите Android-эмулятор с приложением Sauce Labs My Demo App. Затем проверьте, что ADB видит устройство:

```powershell
adb devices
```

В списке должно быть устройство со статусом `device`, например:

```text
emulator-5554    device
```

## 3. Запуск Appium

В отдельном окне PowerShell запустите Appium-сервер:

```powershell
appium --address 127.0.0.1 --port 4723
```

Проект использует адрес `http://127.0.0.1:4723`. Локальные настройки устройства, сервера и приложения находятся в `config/settings.py`.

## 4. Запуск тестов

Запуск одного тестового файла:

```powershell
python -m pytest tests/login/test_login_form.py -v
```

Запуск smoke-набора:

```powershell
python -m pytest -m smoke -v
```

Другие маркеры проекта:

```powershell
python -m pytest -m regression -v
python -m pytest -m negative -v
python -m pytest -m known_bug -v
```

Демонстрация падения приложения изолирована и не входит в обычные запуски. Запускайте её только явно:

```powershell
python -m pytest tests/lifecycle/test_crash_demo.py --run-crash-demo -v
```

## 5. Просмотр Allure-отчёта

После запуска тестов откройте локальный отчёт:

```powershell
allure serve allure-results
```

Последний отчёт из успешного GitHub Actions запуска доступен в GitHub Pages:

https://yana-099.github.io/appium-android-tests/

## 6. Правила для новых тестов

- Один тестовый сценарий — один файл.
- Используйте Page Object Model: локаторы и действия находятся в `pages/`, а проверки — в `tests/`.
- Размещайте тестовые данные в `config/test_data.py`.
- Добавляйте русские комментарии перед логическими блоками теста.
- Оформляйте действия и проверки понятными Allure-шагами.
- Не добавляйте в репозиторий реальные пароли, токены, локальные отчёты, скриншоты и логи.

## 7. Работа через Pull Request

Ветка `main` защищена от прямых изменений. Для каждой задачи создавайте отдельную ветку:

```powershell
git switch main
git pull
git switch -c feature/short-task-name
```

После изменений проверьте нужный тест или маркер, затем отправьте ветку:

```powershell
git add <файлы>
git commit -m "test: short description"
git push -u origin feature/short-task-name
```

Создайте Pull Request в `main`, заполните описание и добавьте ссылку на Allure-отчёт, если выполнялись UI-тесты. После проверки владелец репозитория выполняет merge.
