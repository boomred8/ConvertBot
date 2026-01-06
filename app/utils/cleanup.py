from pathlib import Path
import shutil


def cleanup_user_files(user_id: int) -> None:
    uid = str(user_id) #message.from_user_id

    base_dir = Path(f"from_user") / uid
    try:
        shutil.rmtree(base_dir, ignore_errors=True)
    except Exception as e:
        print(f"cleanup failed: {e}")

