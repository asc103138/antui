#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

with open('scripts/build_22p_reveal_deck.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 找出所有包含 font-size 的行
lines = text.splitlines()
print(f"Total lines: {len(lines)}")
for idx, line in enumerate(lines):
    if 'font-size' in line and not line.strip().startswith('/*'):
        print(f"L{idx+1:04d}: {line.strip()[:100]}")
