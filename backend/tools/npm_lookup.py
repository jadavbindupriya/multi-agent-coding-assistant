# backend/tools/npm_lookup.py
"""Look up npm package information."""

import logging
import requests

logger = logging.getLogger(__name__)


def lookup_npm_package(package_name: str) -> dict:
    """Fetch package info from the npm registry."""
    try:
        url = f"https://registry.npmjs.org/{package_name}"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 404:
            return {"available": False, "package": package_name, "error": "Package not found"}
        resp.raise_for_status()
        data = resp.json()
        latest = data.get("dist-tags", {}).get("latest", "")
        version_info = data.get("versions", {}).get(latest, {})
        return {
            "available": True,
            "package": package_name,
            "latest_version": latest,
            "description": data.get("description", ""),
            "homepage": data.get("homepage", ""),
            "license": version_info.get("license", ""),
            "dependencies": list(version_info.get("dependencies", {}).keys())[:10],
        }
    except Exception as e:
        logger.error(f"npm lookup failed: {e}")
        return {"available": False, "package": package_name, "error": str(e)}
