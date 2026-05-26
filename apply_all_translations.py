#!/usr/bin/env python3
"""
Applique les traductions sur les 11 sous-dossiers langue de ai-soulgen.com
Méthode: recréation depuis source EN + dictionnaire exhaustif
"""

import json, re, os
from pathlib import Path

# Lire le source EN
with open('/root/ai-soulgen.com/index.html', 'r', encoding='utf-8') as f:
    source_en = f.read()

# Langues à traiter (tout sauf FR déjà fait)
langs = ['de', 'es', 'it', 'nl', 'pl', 'pt', 'ru', 'tr', 'ja', 'kr', 'hi']

# Mapping langue -> nom du dossier
lang_folders = {
    'de': 'de', 'es': 'es', 'it': 'it', 'nl': 'nl', 'pl': 'pl',
    'pt': 'pt', 'ru': 'ru', 'tr': 'tr', 'ja': 'ja', 'kr': 'kr', 'hi': 'hi'
}

# Devise par langue
currencies = {
    'de': '€', 'es': '€', 'it': '€', 'nl': '€', 'pl': 'PLN',
    'pt': '€', 'ru': '₽', 'tr': '₺', 'ja': '¥', 'kr': '₩', 'hi': '₹'
}

results = {}

for lang in langs:
    print(f"\n{'='*60}")
    print(f"🔄 Traitement: {lang.upper()}")
    print(f"{'='*60}")
    
    # Charger le dictionnaire
    dict_path = f'/root/ai-soulgen.com/trans_{lang}_complete.json'
    with open(dict_path, 'r', encoding='utf-8') as f:
        translations = json.load(f)
    
    # Copier le source EN
    content = source_en
    
    # Mettre à jour lang attribute
    content = content.replace('lang="en"', f'lang="{lang}"')
    
    # Mettre à jour canonical URL
    content = content.replace('href="https://ai-soulgen.com/"', f'href="https://ai-soulgen.com/{lang}/"')
    
    # Mettre à jour og:locale
    og_locales = {
        'de': 'de_DE', 'es': 'es_ES', 'it': 'it_IT', 'nl': 'nl_NL', 'pl': 'pl_PL',
        'pt': 'pt_PT', 'ru': 'ru_RU', 'tr': 'tr_TR', 'ja': 'ja_JP', 'kr': 'ko_KR', 'hi': 'hi_IN'
    }
    content = content.replace('content="en_US"', f'content="{og_locales[lang]}"')
    
    # Appliquer les traductions (ordre: plus long d'abord)
    sorted_keys = sorted(translations.keys(), key=len, reverse=True)
    count = 0
    for key in sorted_keys:
        if key in content:
            content = content.replace(key, translations[key])
            count += 1
    
    # Adapter les prix avec la devise locale
    currency = currencies[lang]
    if currency == '€':
        content = content.replace('$0/month', '0€/mois').replace('$12.99/month', '12.99€/mois').replace('$24.99/month', '24.99€/mois')
    elif currency == 'PLN':
        content = content.replace('$0/month', '0 PLN/mois').replace('$12.99/month', '12.99 PLN/mois').replace('$24.99/month', '24.99 PLN/mois')
    elif currency == '₽':
        content = content.replace('$0/month', '0₽/месяц').replace('$12.99/month', '12.99₽/месяц').replace('$24.99/month', '24.99₽/месяц')
    elif currency == '₺':
        content = content.replace('$0/month', '0₺/ay').replace('$12.99/month', '12.99₺/ay').replace('$24.99/month', '24.99₺/ay')
    elif currency == '¥':
        content = content.replace('$0/month', '0円/月').replace('$12.99/month', '12.99円/月').replace('$24.99/month', '24.99円/月')
    elif currency == '₩':
        content = content.replace('$0/month', '0원/월').replace('$12.99/month', '12.99원/월').replace('$24.99/month', '24.99원/월')
    elif currency == '₹':
        content = content.replace('$0/month', '0₹/माह').replace('$12.99/month', '12.99₹/माह').replace('$24.99/month', '24.99₹/माह')
    
    # Sauvegarder
    folder = lang_folders[lang]
    output_path = f'/root/ai-soulgen.com/{folder}/index.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    results[lang] = count
    print(f"✅ {lang.upper()}: {count} remplacements appliqués")
    print(f"   Fichier: {output_path}")

# Rapport final
print(f"\n{'='*60}")
print("📊 RAPPORT FINAL")
print(f"{'='*60}")
total = 0
for lang, count in results.items():
    print(f"  {lang.upper()}: {count} remplacements")
    total += count
print(f"\n  TOTAL: {total} remplacements sur 11 langues")
print(f"  Moyenne: {total//11} remplacements/langue")
