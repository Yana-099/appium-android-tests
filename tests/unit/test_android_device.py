from utils import android_device


def test_filters_logcat_to_error_lines_for_application():
    logcat = "\n".join(
        [
            "11-24 20:00:00.000 I SystemServer: unrelated info",
            "11-24 20:00:01.000 E MyDemoApp: com.saucelabs.mydemoapp.android relevant error",
            "11-24 20:00:02.000 D MyDemoApp: com.saucelabs.mydemoapp.android normal state",
            "11-24 20:00:03.000 F MyDemoApp: com.saucelabs.mydemoapp.android relevant fatal error",
            "11-24 20:00:04.000 W SystemServer: unrelated warning",
        ]
    )

    assert hasattr(android_device, "filter_failure_logcat")
    filtered = android_device.filter_failure_logcat(
        logcat, "com.saucelabs.mydemoapp.android"
    )

    assert "unrelated info" not in filtered
    assert "unrelated warning" not in filtered
    assert "relevant error" in filtered
    assert "normal state" not in filtered
    assert "relevant fatal error" in filtered


def test_reports_when_logcat_has_no_relevant_lines():
    assert hasattr(android_device, "filter_failure_logcat")
    filtered = android_device.filter_failure_logcat(
        "11-24 20:00:00.000 D MyDemoApp: com.saucelabs.mydemoapp.android normal state",
        "com.saucelabs.mydemoapp.android",
    )

    assert filtered == "В Android logcat не найдены релевантные ошибки приложения."
