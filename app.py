import os

import boto3
from chalice import Chalice, Response
from jinja2 import Environment, PackageLoader, select_autoescape

BUCKET_NAME = os.environ.get("BUCKET_NAME")

app = Chalice(app_name="LaPPI")
env = Environment(
    loader=PackageLoader("app", "chalicelib/templates"),
    autoescape=select_autoescape(["html", "xml"]),
)
s3_client = boto3.client("s3")


@app.route("/")
def index():
    template = env.get_template("index.html")
    return Response(
        body=template.render(), status_code=200, headers={"Content-Type": "text/html"},
    )


@app.route("/simple", methods=["GET"])
def simple():
    template = env.get_template("simple.html")
    s3_root_objects = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Delimiter="/")
    package_list = [obj["Prefix"] for obj in s3_root_objects["CommonPrefixes"]]
    return Response(
        body=template.render(package_list=package_list),
        status_code=200,
        headers={"Content-Type": "text/html"},
    )


@app.route("/simple/{package_name}")
def package(package_name):
    template = env.get_template("package.html")

    paginator = s3_client.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=BUCKET_NAME, Prefix=f"{package_name}/")

    keys = [key.get("Key") for page in pages for key in page.get("Contents") or []]
    names = [os.path.split(key)[-1] for key in keys]
    items = [(href, name) for href, name in zip(keys, names)]
    return Response(
        body=template.render(package_name=package_name, items=items),
        status_code=200,
        headers={"Content-Type": "text/html"},
    )
