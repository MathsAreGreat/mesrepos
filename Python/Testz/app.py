import base64
import json
import re
from urllib.parse import urlparse

import requests

# Static framework hash parts
_m1 = "7350"
_m2 = "3d58-f228-"
_m3 = "425f-97f1-"
_m4 = "2d9512f5772c"
FRAMEWORK_HASH = ""

restricted_domains = ["www.yourupload.com", "www.mp4upload.com", "videa.hu"]


# This is your Base64 string
def initialize_resources(encoded_str: str):
    decoded_bytes = base64.b64decode(encoded_str)
    resources = decoded_bytes.decode("utf-8")
    return resources


def get_parameter_offset(config_settings):
    index_key = base64.b64decode(config_settings["k"]).decode()
    return config_settings["d"][int(index_key)]


def render_module_content(module_key, resource_registry, config_registry):
    global FRAMEWORK_HASH, _m1, _m2, _m3, _m4

    resource_data = resource_registry[module_key]
    config_settings = config_registry[module_key]

    if not (resource_data and config_settings):
        return None  # nothing to render

    if not FRAMEWORK_HASH:
        FRAMEWORK_HASH = _m1 + _m2 + _m3 + _m4
        _m1 = _m2 = _m3 = _m4 = None

    # Reverse string and clean
    resource_data = resource_data[::-1]
    resource_data = "".join(c for c in resource_data if c.isalnum() or c in "+/=")

    # Decode base64
    param_offset = get_parameter_offset(config_settings)
    decoded_resource = base64.b64decode(resource_data).decode()[:-param_offset]

    # Add API key if matches pattern
    if decoded_resource.startswith("https://yonaplay.org/embed.php?id="):
        resolved_resource = f"{decoded_resource}&apiKey={FRAMEWORK_HASH}"
    else:
        resolved_resource = decoded_resource

    # Domain restrictions
    try:
        domain = urlparse(resolved_resource).hostname
        sandbox = domain in restricted_domains
    except Exception:
        sandbox = False

    return resolved_resource


def ep(u):
    session = requests.Session()
    session.headers.update(
        {
            "Referer": "https://witanime.red/",
        }
    )
    r = session.get(u)
    htext = r.text
    sv = [
        re.findall(r"[a-z0-9\s\-\.]+", e, flags=re.IGNORECASE)
        for e in re.findall(r"server-id([^/]+)<", htext, flags=re.IGNORECASE)
    ]
    sv = {k: v for k, *_, v in sv if "ok" in v or "dailymotion" in v}
    ds = {
        k: v
        for k, v in re.findall(r"(_z[gh])[\"=\s]+([^\"]+)", htext, flags=re.IGNORECASE)
    }
    rel = [
        initialize_resources(f"{u}=")
        for u in re.findall(r"'(aH[^=]+)", htext, flags=re.IGNORECASE)
    ]

    return sv, ds, rel


if __name__ == "__main__":
    u = "https://witanime.red/episode/kaijuu-8-gou-2nd-season-الحلقة-3/"
    dd = ep(u)
    # configy = initialize_resources(ds["_zH"])
    # resourcey = initialize_resources(ds["_zG"])
    # result = render_module_content(9, json.loads(resourcey), json.loads(configy))
    u = "aHR0cHM6Ly93aXRhbmltZS5yZWQvZXBpc29kZS9rYWlqdXUtOC1nb3UtMm5kLXNlYXNvbi0lZDglYTclZDklODQlZDglYWQlZDklODQlZDklODIlZDglYTktMS8="
    # sv = initialize_resources(u)
    print(dd)
