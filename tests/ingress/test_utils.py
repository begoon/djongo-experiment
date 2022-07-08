from ingress.utils import mask_database_url_password


def test_mask_database_url_password():
    url = "mongodb://root:localroot@localhost:27017"
    masked = mask_database_url_password(url)
    assert masked == "mongodb://root:***@localhost:27017"
