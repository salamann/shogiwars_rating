
from ftplib import FTP_TLS

import yaml

from ranking import generate_htmls
from rating import save_data


def upload_file_with_ftp_over_ssl():
    with open("config.yaml", "r") as f:
        configs = yaml.safe_load(f)
    local_path = "index.html"
    print("uploading..\t", local_path)
    remote_path = f"shogiwars/{local_path}"
    with FTP_TLS(host=configs["host_name"], user=configs["user_name"], passwd=configs["password"]) as ftp:
        with open(local_path, 'rb') as f:
            ftp.storbinary(f'STOR {remote_path}', f)


if __name__ == '__main__':
    save_data()
    generate_htmls()
    upload_file_with_ftp_over_ssl()
