# Tests for the neuron page (frontend/crawler.py). Checks safety and privacy basics.

from frontend import crawler


def test_words_cannot_break_out_of_the_script():
    html = crawler.build_html([{"kind": "journal", "text": "hello </script><b>x</b>"}])
    assert html.count("</script>") == 1


def test_all_placeholders_are_filled():
    html = crawler.build_html([{"kind": "answer", "text": "a b c"}], height=300)
    assert "__DATA__" not in html and "__H__" not in html
    assert "300px" in html


def test_empty_input_still_builds():
    assert "Nothing to show yet" in crawler.build_html([])


def test_word_weights_are_passed_on():
    html = crawler.build_html([{"kind": "journal", "text": "sad"}], {"sad": 2.0})
    assert '"sad": 2.0' in html


def test_the_page_makes_no_network_requests():
    html = crawler.build_html([{"kind": "journal", "text": "private words"}])
    for banned in ("fetch(", "XMLHttpRequest", "WebSocket", "sendBeacon", "navigator.", "localStorage"):
        assert banned not in html


def test_only_fonts_are_loaded_from_outside():
    html = crawler.build_html([{"kind": "journal", "text": "private words"}])
    assert "private words" not in html.split("<script>")[0]
    urls = [part.split(")")[0] for part in html.split("url(")[1:]]
    assert all("fonts.googleapis.com" in u for u in urls)


def test_reduced_motion_is_respected():
    assert "prefers-reduced-motion" in crawler.build_html([{"kind": "answer", "text": "a"}])