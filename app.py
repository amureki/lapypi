import os

import boto3
from chalice import Chalice, Response, NotFoundError
from jinja2 import Environment, PackageLoader, select_autoescape

S3_BUCKET_NAME = os.environ.get("BUCKET_NAME")

# chalice
app = Chalice(app_name="LaPPI")
# jinja2
env = Environment(
    loader=PackageLoader("app", "chalicelib/templates"),
    autoescape=select_autoescape(["html", "xml"]),
)
# boto3
s3_client = boto3.client("s3")


def get_presigned_url(key):
    """Generate short-lived URL for getting the package."""
    url = s3_client.generate_presigned_url(
        "get_object",
        ExpiresIn=300,
        Params={"Bucket": S3_BUCKET_NAME, "Key": key},
        HttpMethod="GET",
    )
    return url


@app.route("/", methods=["GET"])
def simple():
    template = env.get_template("simple.html")
    s3_root_objects = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME, Delimiter="/")
    package_list = [obj["Prefix"] for obj in s3_root_objects["CommonPrefixes"]]
    return Response(
        body=template.render(package_list=package_list),
        status_code=200,
        headers={"Content-Type": "text/html"},
    )


@app.route("/{package_name}", methods=["GET"])
def package(package_name):
    template = env.get_template("package.html")
    paginator = s3_client.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=S3_BUCKET_NAME, Prefix=f"{package_name}/")

    keys = [key.get("Key") for page in pages for key in page.get("Contents") or []]
    if not keys:
        raise NotFoundError

    urls = [get_presigned_url(key) for key in keys]
    names = [os.path.split(key)[-1] for key in keys]
    items = [(href, name) for href, name in zip(urls, names)]

    # drop S3 folder element
    if items:
        del items[0]

    return Response(
        body=template.render(package_name=package_name, items=items),
        status_code=200,
        headers={"Content-Type": "text/html"},
    )
