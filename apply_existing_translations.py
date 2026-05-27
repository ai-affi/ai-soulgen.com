#!/usr/bin/env python3
"""
Apply existing translation JSONs to all language subfolders.
Uses trans_*_complete.json and trans_*_final.json files.
"""

import json
import os
import glob
import re

LANGS = ['fr','de','es','it','pt','nl','pl','ru','tr','ja','kr','hi']

def load_translations():
    all_trans = {}
    
    # Load complete files first
    for f in sorted(glob.glob('trans_*_complete.json')):
        lang = f.split('_')[1]
        with open(f, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
        all_trans[lang] = data
        print(f"Loaded {lang} complete: {len(data)} entries")
    
    # Load final files (override/add to complete)
    for f in sorted(glob.glob('trans_*_final.json')):
        lang = f.split('_')[1]
        with open(f, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
        if lang in all_trans:
            all_trans[lang].update(data)
            print(f"Loaded {lang} final: {len(data)} entries (merged)")
        else:
            all_trans[lang] = data
    
    return all_trans

def apply_translations(html, trans_dict):
    """Apply translations, longest first to avoid partial replacements."""
    items = sorted(trans_dict.items(), key=lambda x: len(x[0]), reverse=True)
    count = 0
    for en, tr in items:
        if en in html and tr and tr != en:
            html = html.replace(en, tr)
            count += 1
    return html, count

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        en_html = f.read()
    
    all_trans = load_translations()
    
    for lang in LANGS:
        print(f"\n=== Processing {lang} ===")
        
        lang_path = f"{lang}/index.html"
        if not os.path.exists(lang_path):
            os.makedirs(lang, exist_ok=True)
            lang_html = en_html
        else:
            with open(lang_path, 'r', encoding='utf-8') as f:
                lang_html = f.read()
        
        # Start fresh from EN to ensure clean translations
        lang_html = en_html
        
        # Apply translations
        trans = all_trans.get(lang, {})
        lang_html, count = apply_translations(lang_html, trans)
        print(f"  Applied {count} translations")
        
        # Update meta tags
        lang_html = lang_html.replace('lang="en"', f'lang="{lang}"')
        
        # Update og:locale
        locales = {
            'fr': 'fr_FR', 'de': 'de_DE', 'es': 'es_ES', 'it': 'it_IT',
            'pt': 'pt_PT', 'nl': 'nl_NL', 'pl': 'pl_PL', 'ru': 'ru_RU',
            'tr': 'tr_TR', 'ja': 'ja_JP', 'kr': 'ko_KR', 'hi': 'hi_IN'
        }
        lang_html = lang_html.replace('og:locale" content="en_US"', f'og:locale" content="{locales.get(lang, "en_US")}"')
        
        # Update canonical
        lang_html = lang_html.replace('href="https://ai-soulgen.com/"', f'href="https://ai-soulgen.com/{lang}/"')
        
        # Fix paths for subfolder
        lang_html = lang_html.replace('href="index.html"', 'href="../index.html"')
        lang_html = lang_html.replace('href="privacy.html"', 'href="../privacy.html"')
        lang_html = lang_html.replace('href="terms.html"', 'href="../terms.html"')
        lang_html = lang_html.replace('href="affiliate-disclosure.html"', 'href="../affiliate-disclosure.html"')
        lang_html = lang_html.replace('src="images/', 'src="../images/')
        lang_html = lang_html.replace('href="images/', 'href="../images/')
        
        # Write back
        with open(lang_path, 'w', encoding='utf-8') as f:
            f.write(lang_html)
        
        # Verify remaining EN texts
        ru_texts = set(re.findall(r'>([^<]{10,}?)<', lang_html))
        en_remaining = [t for t in ru_texts if re.search(r'[a-zA-Z]{5,}', t) and not t.startswith('http') and 'function' not in t and 'var ' not in t and 'CSS' not in t and 'margin' not in t]
        print(f"  Remaining EN texts: {len(en_remaining)}")

if __name__ == '__main__':
    main()
