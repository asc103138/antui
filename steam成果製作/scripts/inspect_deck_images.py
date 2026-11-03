#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

with open(r'成果展繳交資料/steam-gigo-balance-deck/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

imgs = sorted(set(re.findall(r'src=["\']([^"\']+\.(?:png|jpg|jpeg|svg))["\']', text)))
print("Found images in HTML slide deck:")
for img in imgs:
    print(" ", img)
