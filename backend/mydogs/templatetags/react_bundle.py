import json
import os
from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag(takes_context=True)
def get_react_bundle(context):
    """
    Возвращает тег <script> с React-бандлом из asset-manifest.json,
    добавляя nonce для CSP.
    """
    manifest_path = os.path.join(settings.BASE_DIR, 'frontend', 'build', 'asset-manifest.json')
    nonce = context.get('nonce', '')

    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        main_js = manifest['files'].get('main.js', '')

        if main_js:
            return f'<script src="{main_js}" nonce="{nonce}" defer></script>'
        else:
            return '<!-- main.js не найден в asset-manifest.json -->'
    except Exception as e:
        return f'<!-- Ошибка при чтении asset-manifest.json: {e} -->'
