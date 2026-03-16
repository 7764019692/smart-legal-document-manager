import difflib

def compare_text(old_text, new_text):

    old_lines = old_text.splitlines()
    new_lines = new_text.splitlines()

    diff = difflib.unified_diff(
        old_lines,
        new_lines,
        lineterm=""
    )

    return "\n".join(diff)