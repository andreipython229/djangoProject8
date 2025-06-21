import json
import os
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag(takes_context=True)
def get_react_bundle(context):
    manifest_path = os.path.join(settings.BASE_DIR, 'frontend', 'build', 'asset-manifest.json')
    nonce = context.get('nonce', '')

    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)

        files = manifest.get('files', {})
        main_js = files.get('main.js')
        main_css = files.get('main.css')

        tags = []
        if main_css:
            tags.append(f'<link rel="stylesheet" href="{main_css}" nonce="{nonce}">')
        if main_js:
            tags.append(f'<script src="{main_js}" nonce="{nonce}" defer></script>')

        if not tags:
            return '<!-- JS/CSS бандлы не найдены в asset-manifest.json -->'
        
        return mark_safe('\n'.join(tags))

    except Exception as e:
        return f'<!-- Ошибка при чтении asset-manifest.json: {e} -->'
