import qrcode 
from urllib.parse import urlparse

def add_http_if_missing(url):
    parsed_url = urlparse(url)
    if parsed_url.scheme == "":
        return 'http://' + url
    else:
        return url

def url_to_qr(url, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print(f"{url} successfully converted to QR code => {filename}")

if __name__ == "__main__":
    input_url = input("Enter the URL that will be turned into a QR code: ")
    input_url = add_http_if_missing(input_url)
    output_filename = "C:/Users/Rahmet/Desktop/koustech/qr_code/koustech_qr_code.png"

    url_to_qr(input_url, output_filename)
