import os
import requests
import time
import urllib.parse

BASE_URL = "https://wiki.guildwars.com/api.php"
OUTPUT_DIR = "skills_icons"

def get_subcategories(category):
    """Liste toutes les sous-catégories d'une catégorie."""
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": f"Category:{category}",
        "cmtype": "subcat",
        "cmlimit": "max",
        "format": "json"
    }
    subcats = []
    while True:
        res = requests.get(BASE_URL, params=params).json()
        subcats.extend(res["query"]["categorymembers"])
        if "continue" in res:
            params["cmcontinue"] = res["continue"]["cmcontinue"]
        else:
            break
    return [s["title"].replace("Category:", "") for s in subcats]

def get_images_from_category(category):
    """Récupère toutes les images d'une catégorie (pagination incluse)."""
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": f"Category:{category}",
        "cmtype": "file",
        "cmlimit": "max",
        "format": "json"
    }
    images = []
    while True:
        res = requests.get(BASE_URL, params=params).json()
        images.extend(res["query"]["categorymembers"])
        if "continue" in res:
            params["cmcontinue"] = res["continue"]["cmcontinue"]
        else:
            break
    return images

def get_image_url(filename):
    """Récupère l'URL directe d'une image (File:xxx.jpg)."""
    params = {
        "action": "query",
        "titles": f"File:{filename}",
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json"
    }
    res = requests.get(BASE_URL, params=params).json()
    pages = res["query"]["pages"]
    for page in pages.values():
        if "imageinfo" in page:
            return page["imageinfo"][0]["url"]
    return None

def sanitize_filename(name):
    """Nettoie les noms de fichiers pour enlever les caractères bizarres."""
    name = urllib.parse.unquote(name)  # remplace %27 par '
    invalid = '<>:"/\\|?*'
    for c in invalid:
        name = name.replace(c, "_")
    return name

def download_image(url, output_dir):
    """Télécharge une image dans le dossier cible."""
    filename = sanitize_filename(url.split("/")[-1])
    path = os.path.join(output_dir, filename)
    if not os.path.exists(path):
        img_data = requests.get(url).content
        with open(path, "wb") as f:
            f.write(img_data)
        print(f"✅ Downloaded {filename}")
    else:
        print(f"⚡ Skipped {filename} (already exists)")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Catégorie principale
    main_category = "Skill_icons"
    subcategories = get_subcategories(main_category)

    print(f"Found {len(subcategories)} subcategories in {main_category}")

    for subcat in subcategories:
        subcat_dir = os.path.join(OUTPUT_DIR, subcat.replace(" ", "_"))
        os.makedirs(subcat_dir, exist_ok=True)

        images = get_images_from_category(subcat)
        print(f"\n📂 {subcat}: {len(images)} images")

        for img in images:
            filename = img["title"].replace("File:", "")
            url = get_image_url(filename)
            if url:
                download_image(url, subcat_dir)
            time.sleep(0.2)  # évite de spammer le serveur

    print(f"\n🎉 All done! Images saved in: {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
