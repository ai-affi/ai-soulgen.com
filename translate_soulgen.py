#!/usr/bin/env python3
"""
Script de traduction ai-soulgen.com
Traduit index.html EN vers 12 langues
"""

import os
import re

# Configuration
BASE_DIR = '/root/ai-soulgen.com'
LANGS = ['fr', 'es', 'pt', 'it', 'de', 'nl', 'pl', 'ru', 'tr', 'ja', 'kr', 'hi']

# Dictionnaire de traduction complet
# Clé = texte EN, Valeur = dict avec traductions par langue
TRANSLATIONS = {
    # META & HEAD
    "SoulGen AI – Free AI Soulmate & Image Generator 2026": {
        'fr': "SoulGen AI – Générateur d'Âme Sœur & d'Images IA Gratuit 2026",
        'es': "SoulGen AI – Generador de Alma Gemela & Imágenes IA Gratis 2026",
        'pt': "SoulGen AI – Gerador de Alma Gêmea & Imagens IA Grátis 2026",
        'it': "SoulGen AI – Generatore di Anima Gemella & Immagini IA Gratuito 2026",
        'de': "SoulGen AI – KI Seelengefährte & Bildgenerator Kostenlos 2026",
        'nl': "SoulGen AI – AI Zielsverwant & Afbeelding Generator Gratis 2026",
        'pl': "SoulGen AI – Generator Bratni Duszy & Obrazów AI Darmowy 2026",
        'ru': "SoulGen AI – Бесплатный Генератор ИИ-Пары & Изображений 2026",
        'tr': "SoulGen AI – Ücretsiz AI Ruh Eşi & Görüntü Oluşturucu 2026",
        'ja': "SoulGen AI – 無料AIソウルメイト＆画像生成 2026",
        'kr': "SoulGen AI – 묣 AI 소울메이트 & 이미지 생성기 2026",
        'hi': "SoulGen AI – मुफ्त AI जोड़ीदार & छवि जनरेटर 2026",
    },
    "Create your dream AI soulmate with SoulGen AI. Generate realistic & anime characters from text in seconds. Try free today.": {
        'fr': "Créez votre âme sœur IA de rêve avec SoulGen AI. Générez des personnages réalistes & anime à partir de texte en secondes. Essayez gratuitement.",
        'es': "Crea tu alma gemela IA de ensueño con SoulGen AI. Genera personajes realistas & anime desde texto en segundos. Prueba gratis hoy.",
        'pt': "Crie sua alma gêmea IA dos sonhos com SoulGen AI. Gere personagens realistas & anime a partir de texto em segundos. Experimente grátis.",
        'it': "Crea la tua anima gemella IA dei sogni con SoulGen AI. Genera personaggi realistici & anime dal testo in secondi. Prova gratis.",
        'de': "Erstelle deinen Traum-KI-Seelengefährten mit SoulGen AI. Generiere realistische & Anime-Charaktere aus Text in Sekunden. Kostenlos testen.",
        'nl': "Creëer je droom AI zielsverwant met SoulGen AI. Genereer realistische & anime karakters van tekst in seconden. Probeer gratis.",
        'pl': "Stwórz wymarzoną bratnią duszę AI z SoulGen AI. Generuj realistyczne & anime postacie z tekstu w sekundy. Wypróbuj za darmo.",
        'ru': "Создай свою идеальную ИИ-пару с SoulGen AI. Генерируй реалистичных & аниме-персонажей из текста за секунды. Попробуй бесплатно.",
        'tr': "SoulGen AI ile hayalindeki AI ruh eşini oluştur. Saniyeler içinde metinden gerçekçi & anime karakterler üret. Ücretsiz dene.",
        'ja': "SoulGen AIで夢のAIソウルメイトを作成。テキストからリアル＆アニメキャラを数秒で生成。今すぐ無料でお試し。",
        'kr': "SoulGen AI로 꿈의 AI 소울메이트를 만들어보세요. 텍스트에서 실사 & 애니 캐릭터를 수 초 만에 생성하세요. 지금 묣으로 시도하세요.",
        'hi': "SoulGen AI के साथ अपने सपनों का AI जोड़ीदार बनाएं। टेक्स्ट से कुछ ही सेकंड में यथार्थवादी & एनीमे कैरेक्टर जनरेट करें। आज ही मुफ्त आजमाएं।",
    },
    "AI SoulGen": {
        'fr': "AI SoulGen", 'es': "AI SoulGen", 'pt': "AI SoulGen", 'it': "AI SoulGen",
        'de': "AI SoulGen", 'nl': "AI SoulGen", 'pl': "AI SoulGen", 'ru': "AI SoulGen",
        'tr': "AI SoulGen", 'ja': "AI SoulGen", 'kr': "AI SoulGen", 'hi': "AI SoulGen",
    },
    # HERO
    "The ultimate AI soulmate and character generator. Create realistic and anime-style characters from text in seconds.": {
        'fr': "Le générateur d'âme sœur et de personnages IA ultime. Créez des personnages réalistes et de style anime à partir de texte en secondes.",
        'es': "El generador de alma gemela y personajes IA definitivo. Crea personajes realistas y de estilo anime desde texto en segundos.",
        'pt': "O gerador de alma gêmea e personagens IA definitivo. Crie personagens realistas e de estilo anime a partir de texto em segundos.",
        'it': "Il generatore di anime gemelle e personaggi IA definitivo. Crea personaggi realistici e in stile anime dal testo in secondi.",
        'de': "Der ultimative KI-Seelengefährten- und Charaktergenerator. Erstelle realistische und Anime-Charaktere aus Text in Sekunden.",
        'nl': "De ultieme AI zielsverwant- en karaktergenerator. Creëer realistische en anime-stijl karakters van tekst in seconden.",
        'pl': "Ostateczny generator bratniej duszy i postaci AI. Twórz realistyczne postacie w stylu anime z tekstu w sekundy.",
        'ru': "Лучший генератор ИИ-пары и персонажей. Создавай реалистичных и аниме-персонажей из текста за секунды.",
        'tr': "Nihai AI ruh eşi ve karakter oluşturucu. Saniyeler içinde metinden gerçekçi ve anime tarzı karakterler oluştur.",
        'ja': "究極のAIソウルメイト＆キャラクタージェネレーター。テキストから数秒でリアル＆アニメスタイルのキャラを作成。",
        'kr': "궁극의 AI 소울메이트 & 캐릭터 생성기。텍스트에서 수 초 만에 실사 & 애니 스타일 캐릭터를 생성하세요.",
        'hi': "अंतिम AI जोड़ीदार और कैरेक्टर जनरेटर। टेक्स्ट से कुछ ही सेकंड में यथार्थवादी और एनीमे-शैली के कैरेक्टर बनाएं।",
    },
    "✨ Free daily credits • No credit card required • Results in under 10 seconds": {
        'fr': "✨ Crédits quotidiens gratuits • Pas de carte requise • Résultats en moins de 10 secondes",
        'es': "✨ Créditos diarios gratis • Sin tarjeta requerida • Resultados en menos de 10 segundos",
        'pt': "✨ Créditos diários grátis • Sem cartão necessário • Resultados em menos de 10 segundos",
        'it': "✨ Crediti giornalieri gratuiti • Nessuna carta richiesta • Risultati in meno di 10 secondi",
        'de': "✨ Kostenlose tägliche Credits • Keine Karte erforderlich • Ergebnisse in unter 10 Sekunden",
        'nl': "✨ Gratis dagelijkse credits • Geen kaart nodig • Resultaten in minder dan 10 seconden",
        'pl': "✨ Darmowe codzienne kredyty • Bez karty wymaganej • Wyniki w mniej niż 10 sekund",
        'ru': "✨ Бесплатные ежедневные кредиты • Карта не требуется • Результаты менее чем за 10 секунд",
        'tr': "✨ Ücretsiz günlük kredi • Kart gerekmez • 10 saniyeden kısa sürede sonuçlar",
        'ja': "✨ 無料毎日クレジット • カード不要 • 10秒未満で結果",
        'kr': "✨ 묣 일일 크레딧 • 카드 불필요 • 10초 이내 결과",
        'hi': "✨ मुफ्त दैनिक क्रेडिट • कोई कार्ड नहीं चाहिए • 10 सेकंड से कम में परिणाम",
    },
    "Get Started Free": {
        'fr': "Commencer Gratuitement", 'es': "Empezar Gratis", 'pt': "Começar Grátis",
        'it': "Inizia Gratis", 'de': "Kostenlos Starten", 'nl': "Gratis Beginnen",
        'pl': "Zacznij Za Darmo", 'ru': "Начать Бесплатно", 'tr': "Ücretsiz Başla",
        'ja': "無料で始める", 'kr': "묣으로 시작", 'hi': "मुफ्त शुरू करें",
    },
    "How It Works": {
        'fr': "Comment Ça Marche", 'es': "Cómo Funciona", 'pt': "Como Funciona",
        'it': "Come Funziona", 'de': "Wie Es Funktioniert", 'nl': "Hoe Het Werkt",
        'pl': "Jak To Działa", 'ru': "Как Это Работает", 'tr': "Nasıl Çalışır",
        'ja': 