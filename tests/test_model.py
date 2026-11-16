from app import model


def test_model_positive():
    # Controllo una recensione positiva
    assert model.predict(["This product is amazing! I love it."])[0] == "positive"


def test_model_negative():
    # Controllo una recensione negativa
    assert model.predict(["I hate it. Terrible product."])[0] == "negative"


def test_model_neutral():
    # Controllo una recensione neutra
    assert model.predict(["Neither good nor bad."])[0] == "neutral"
