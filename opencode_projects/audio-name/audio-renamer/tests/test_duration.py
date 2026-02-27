from audio_renamer.duration import format_duration

def test_format_duration_mm_ss():
    assert format_duration(120.0) == "02-00"
    assert format_duration(65.0) == "01-05"
    assert format_duration(59.0) == "00-59"
    assert format_duration(0.0) == "00-00"
    assert format_duration(-1.0) == "00-00"

def test_format_duration_mm_colon_ss():
    assert format_duration(120.0, 'mm:ss') == "02:00"
    assert format_duration(65.0, 'mm:ss') == "01:05"
    assert format_duration(59.0, 'mm:ss') == "00:59"

def test_format_duration_ss():
    assert format_duration(120.0, 'ss') == "120"
    assert format_duration(65.0, 'ss') == "065"
    assert format_duration(59.0, 'ss') == "059"