import os
import random
import datetime
from pathlib import Path

from PIL import Image

temp_outputs_path = os.path.join(Path.home(), ".cache/imaaage/outputs")
os.makedirs(temp_outputs_path, exist_ok=True)


def generate_temp_filename(folder='./outputs/', extension='png'):
    current_time = datetime.datetime.now()
    date_string = current_time.strftime("%Y-%m-%d")
    time_string = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    random_number = random.randint(1000, 9999)
    filename = f"{time_string}_{random_number}.{extension}"
    result = os.path.join(folder, date_string, filename)
    return date_string, os.path.realpath(result), filename


def current_img_log_file():
    current_time = datetime.datetime.now()
    date_string = current_time.strftime("%Y-%m-%d")
    rel_html = os.path.join(date_string, "log.html")
    return rel_html


def current_eval_log_file():
    current_time = datetime.datetime.now()
    date_string = current_time.strftime("%Y-%m-%d")
    rel_html = os.path.join(date_string, "eval.html")
    return rel_html


def log_img(img: Image.Image, dic):
    date_string, local_temp_filename, only_name = \
        generate_temp_filename(folder=temp_outputs_path, extension='webp')
    os.makedirs(os.path.dirname(local_temp_filename), exist_ok=True)
    img.save(local_temp_filename, format="WEBP", quality=80)
    html_name = os.path.join(os.path.dirname(local_temp_filename), 'log.html')

    if not os.path.exists(html_name):
        with open(html_name, 'a+') as f:
            f.write(f"<p>图片历史记录 {date_string} </p>\n")

    with open(html_name, 'a+') as f:
        div_name = only_name.replace('.', '_')
        f.write(f'<div id="{div_name}"><hr>\n')
        f.write(f"<p>{only_name}</p>\n")
        i = 0
        for k, v in dic:
            if i < 2:
                f.write(f"<p>{k}: <b>{v}</b> </p>\n")
            else:
                if i % 2 == 0:
                    f.write(f"<p>{k}: <b>{v}</b>, ")
                else:
                    f.write(f"{k}: <b>{v}</b></p>\n")
            i += 1
        f.write(
            f"<p><img src=\"{only_name}\" width=512 onerror=\"document.getElementById('{div_name}').style.display = 'none';\"></img></p></div>\n")

    print(f'History saved: {html_name}')
    return local_temp_filename


def log_evaluation(dic):
    date_string, local_temp_filename, only_name = \
        generate_temp_filename(folder=temp_outputs_path, extension='txt')
    os.makedirs(os.path.dirname(local_temp_filename), exist_ok=True)
    with open(local_temp_filename, "w") as f:
        f.write(str(dic))
    html_name = os.path.join(os.path.dirname(local_temp_filename), 'eval.html')
    with open(html_name, 'a+') as f:
        div_name = only_name.replace('.', '_')
        f.write(f'<div id="{div_name}"><hr>\n')
        f.write(f"<p>{only_name}</p>\n")
        i = 0
        for k, v in dic:
            if i < 2:
                f.write(f"<p>{k}: <b>{v}</b> </p>\n")
            else:
                if i % 2 == 0:
                    f.write(f"<p>{k}: <b>{v}</b>, ")
                else:
                    f.write(f"{k}: <b>{v}</b></p>\n")
            i += 1
    print(f'Eval saved: {html_name}')
    return local_temp_filename

def pretty_eval_report(d):
    from tabulate import tabulate
    return tabulate(d)
