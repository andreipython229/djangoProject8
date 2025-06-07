import json
import os
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag(takes_context=True)
def get_react_bundle(context):
    print("[ReactBundle] Вызов тега get_react_bundle")

    manifest_path = os.path.join(settings.BASE_DIR, 'frontend', 'build', 'asset-manifest.json')
    print(f"[ReactBundle] manifest_path: {manifest_path}")

    nonce = context.get('nonce', '')
    print(f"[ReactBundle] nonce: {nonce}")

    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)

        main_js = manifest['files'].get('main.js', '')
        print(f"[ReactBundle] main.js: {main_js}")

        if main_js:
            return mark_safe(f'<script src="{main_js}" nonce="{nonce}" defer></script>')
        else:
            return '<!-- main.js не найден в asset-manifest.json -->'

    except Exception as e:
        print(f"[ReactBundle] Ошибка: {e}")
        return f'<!-- Ошибка при чтении asset-manifest.json: {e} -->'
