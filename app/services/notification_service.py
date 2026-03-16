from difflib import SequenceMatcher
import threading


def is_significant_change(old_text, new_text):

    similarity = SequenceMatcher(
        None,
        old_text,
        new_text
    ).ratio()

    return similarity < 0.95


def send_notification(doc_id):

    print(f"Significant change detected in document {doc_id}")


def notify_async(doc_id):

    thread = threading.Thread(
        target=send_notification,
        args=(doc_id,)
    )

    thread.start()