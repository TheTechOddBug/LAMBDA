import gradio
import html
import re

def display_text(text):
    return f"""<div style="border: 1px solid #ccc; padding: 10px; margin-bottom: 10px;"><p>{text}</p></div>"""

def display_image(path):
    return f"""<img src=\"file={path}\" style="max-width: 80%;">"""


def display_status(text):
    return f"""\n\n<div class="lambda-status">{html.escape(text)}</div>\n\n"""


def display_exe_results(text):
    escaped_text = html.escape(text)
    return f"""\n\n<details class="execution-results"><summary>✅ Click to view execution results</summary><pre>{escaped_text}</pre></details>\n\n"""


def display_download_file(path, filename):
    return f"""\n\n<div style="border: 1px solid #ccc; padding: 10px; margin-bottom: 10px;"><a href=\"file={path}\" download style="font-weight: bold; color: #007bff;">Download {filename}</a></div>\n\n"""

def suggestion_html(suggestions: list) -> str:
    buttons_html = ""
    for suggestion in suggestions:
        buttons_html += f"""<button class='suggestion-btn'>{html.escape(suggestion)}</button>"""
    return f"\n\n<div>{buttons_html}</div>\n\n"


def display_suggestions(prog_response, chat_history_display_last):
    '''
        replace：
            Next, you can:
            [1] Do something...
            [2] Do something else...

        by：
            <div>
                <button class="suggestion-btn" data-bound="true">...</button>
                <button class="suggestion-btn" data-bound="true">...</button>
            </div>
    '''
    marker_matches = list(re.finditer(r'Next,\s*you\s*can:', prog_response, flags=re.IGNORECASE))
    if not marker_matches:
        return chat_history_display_last

    marker = marker_matches[-1]
    suggestions_text = prog_response[marker.end():]
    suggest_list = []
    for line in suggestions_text.splitlines():
        match = re.match(r'\s*(?:\[\d+\]|\d+[\.\)])\s*(.+?)\s*$', line)
        if match:
            suggest_list.append(match.group(1))

    if not suggest_list:
        return chat_history_display_last

    button_html = suggestion_html(suggest_list)
    pattern = r'(Next,\s*you\s*can:)(?![\s\S]*Next,\s*you\s*can:)[\s\S]*$'
    chat_history_display_last = re.sub(
        pattern,
        r'\1' + button_html,
        chat_history_display_last,
        flags=re.IGNORECASE
    )

    return chat_history_display_last
