import subprocess
from urllib.parse import urljoin
import asyncio
import glob
import os
import re
import requests
from bs4 import BeautifulSoup
import aiohttp


async def fetch_resource_size(
    session: aiohttp.ClientSession, url: str
) -> tuple[str, int]:
    """Return ressource size for a url

    Args:
        session (aiohttp.ClientSession): Session for async requests
        url (str): ressource's url

    Returns:
        tuple[str, int]: ressource's url, ressource's size
    """
    try:
        async with session.get(url) as response:
            content = await response.read()
            return url, len(content)
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return url, 0


async def download_all(base_url: str, page: str) -> tuple[str, int]:
    """Download all content for a url (HTML, media, css, scripts, etc)

    Args:
        base_url (str): Website base url
        page (str): page to retrieve as public path

    Returns:
        tuple[str, int]: page's path, page's size
    """
    p_url = page.replace("public", "").replace("\\", "/")
    url = base_url + p_url
    async with aiohttp.ClientSession() as session:
        response = requests.get(url, timeout=3)
        soup = BeautifulSoup(response.text, "html.parser")
        resource_urls = set()
        # Add URLs from <img> and <scripts> tags
        for tag in ["img", "script"]:
            for ressource in soup.find_all(tag):
                res_url = ressource.get("src")
                if res_url:
                    resource_urls.add(urljoin(url, res_url))
        # Add URLs from <link> tags (e.g., stylesheets)
        for link in soup.find_all("link"):
            link_url = link.get("href")
            if link_url:
                resource_urls.add(urljoin(url, link_url))

        total_size = len(response.content)
        tasks = [fetch_resource_size(session, res_url) for res_url in resource_urls]
        results = await asyncio.gather(*tasks)
        for res_url, res_size in results:
            total_size += res_size
    print(f"Page : {page} weigh {total_size/1000} kB")
    return page, total_size


def find_pages(directory: str) -> list[str]:
    """Find all unique *.html pages in a given directory

    Args:
        directory (str): directory to search in

    Returns:
        list[str]: list of path
    """
    matches = set(glob.glob(os.path.join(directory, "**", "*.html"), recursive=True))
    return list(matches)


async def compute_weight_all(base_url: str, pages: list[str]) -> dict[str, int]:
    """Compute weight of all pages passed as parameters

    Args:
        base_url (str): Base url to use
        pages (list[str]): list of *.html pages in the website's 'public' directory

    Returns:
        dict[str, int]: Association of page path and size
    """
    res = await asyncio.gather(*[download_all(base_url, p) for p in pages])
    res_dict = dict(res)
    return res_dict


def update_pages(weight_dict: dict[str, int]):
    """Update pages with corresponding size in kB

    Args:
        weight_dict (dict[str, int]): Association of page path and size
    """
    for page, weight in weight_dict.items():
        html = ""
        with open(page, "rb") as html_buf:
            html = html_buf.read()
        soup = BeautifulSoup(html, "html.parser")
        old_text = soup.find("span", {"id": "hugo-sizer"})
        if old_text is not None:
            old_text.string.replaceWith(f"{weight/1000}")
            with open(page, "wb") as f_output:
                f_output.write(soup.prettify("utf-8"))
    print(f"Updated {len(weight_dict)} pages")


def launch_hugo_serve() -> tuple[subprocess.Popen, str]:
    """Launch Hugo server in a separate process

    Returns:
        tuple[subprocess.Popen, str]: Hugo server process and base url
    """
    hugo_server = subprocess.Popen(
        ["hugo", "serve", "--disableLiveReload"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    buff = ""
    while "Press Ctrl+C to stop" not in buff:
        buff += hugo_server.stdout.read(1).decode("latin-1")
    base_url = get_base_url(buff)
    return hugo_server, base_url


def get_base_url(hugo_out: str) -> str:
    """Retrieve base url from hugo output

    Args:
        hugo_out (str): Hugo output

    Raises:
        IndexError: Raise if url is not found

    Returns:
        str: Base url
    """
    finds = re.findall(r"http:\/\/[\dA-Za-z]*:[\d]*\/", hugo_out)
    if len(finds) == 1:
        return finds[0]
    else:
        raise IndexError("Url not found")


def main():
    all_pages = find_pages("public")
    if len(all_pages)>0:
        hugo_server, base_url = launch_hugo_serve()
        weight_dict = asyncio.run(compute_weight_all(base_url, all_pages))
        update_pages(weight_dict)
        hugo_server.terminate()
    else:
        print("No page to process")


if __name__ == "__main__":
    main()
