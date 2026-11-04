with open('E:/VoiceAI/extracted_ui_design/app/globals.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace .voice-range::-webkit-slider-thumb and track rules
old_thumb_rule = """.voice-range::-webkit-slider-thumb {
    appearance: none;
    width: 16px;
    height: 16px;
    margin-top: -6px;
    border: 2px solid var(--background);
    border-radius: 9999px;
    background: var(--primary);
    box-shadow: 0 1px 5px color-mix(in oklab, var(--primary) 28%, transparent);
    transition:
      transform 180ms cubic-bezier(0.2, 0.8, 0.2, 1),
      box-shadow 180ms ease;
  }"""

new_thumb_rule = """.voice-range::-webkit-slider-thumb {
    appearance: none;
    width: 3px;
    height: 14px;
    margin-top: -5.5px;
    border: none;
    border-radius: 1px;
    background: #18181b;
    box-shadow: 0 0 2px rgba(0, 0, 0, 0.4);
    cursor: pointer;
  }"""

if old_thumb_rule in css:
    css = css.replace(old_thumb_rule, new_thumb_rule)
    print("Replaced .voice-range::-webkit-slider-thumb")
else:
    print("Could not find exact old_thumb_rule, appending override at end")
    css += "\n" + new_thumb_rule

old_track_rule = """.voice-range::-webkit-slider-runnable-track {
    height: 4px;
    border-radius: 9999px;
    background-color: var(--muted);
    background-image: linear-gradient(var(--primary), var(--primary));
    background-repeat: no-repeat;
    background-size: var(--range-progress) 100%;
    transition: background-size 100ms ease-out;
  }"""

new_track_rule = """.voice-range::-webkit-slider-runnable-track {
    height: 3px;
    border-radius: 2px;
    background-color: #e4e4e7;
    background-image: linear-gradient(#52525b, #52525b);
    background-repeat: no-repeat;
    background-size: var(--range-progress) 100%;
  }"""

if old_track_rule in css:
    css = css.replace(old_track_rule, new_track_rule)
    print("Replaced .voice-range::-webkit-slider-runnable-track")
else:
    print("Could not find exact old_track_rule, appending override at end")
    css += "\n" + new_track_rule

with open('E:/VoiceAI/extracted_ui_design/app/globals.css', 'w', encoding='utf-8') as f:
    f.write(css)
print("Updated globals.css successfully")
