from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from config import DATA_URL, LABELS_URL, DATA_FILE, LABELS_FILE
def download(url: str, target):
    print(f"Downloading: {url}")
    try:
        with urlopen(url, timeout=30) as response:
            content = response.read()
        target.write_bytes(content)
        print(f"Saved to: {target}")
    except (URLError, HTTPError) as exc:
        raise RuntimeError(f"Khong the tai du lieu tu {url}. Chi tiet:\n{exc}") from exc
def main():
    download(DATA_URL, DATA_FILE)
    download(LABELS_URL, LABELS_FILE)
    print("Da tai xong dataset NAB va file nhan.")
if __name__ == "__main__":
    main()