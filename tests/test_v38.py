import os
import glob
import traceback
from spine_asset.v38.SkeletonBinary import SkeletonBinary
from spine_asset.v38.SkeletonData import SkeletonData


def summary(skeleton_data: SkeletonData):
    """Generate a summary of the skeleton data."""

    def summary_list(lst: list):
        return str(list(map(lambda x: x.name, lst)))

    return "\n".join(
        [
            f"Name: {skeleton_data.name}",
            f"Bones: {summary_list(skeleton_data.bones)}",
            f"Slots: {summary_list(skeleton_data.slots)}",
            f"Skins: {summary_list(skeleton_data.skins)}",
            f"Events: {summary_list(skeleton_data.events)}",
            f"Animations: {summary_list(skeleton_data.animations)}",
            f"IK Constraints: {len(skeleton_data.ik_constraints)}",
            f"Transform Constraints: {len(skeleton_data.transform_constraints)}",
            f"Path Constraints: {len(skeleton_data.path_constraints)}",
            f"Version: {skeleton_data.version}",
            f"Hash: {skeleton_data.hash}",
        ]
    )


def test_single(file_path: str, skeleton_binary: SkeletonBinary):
    """Test a single skeleton file."""
    std_file_path = os.path.splitext(file_path)[0] + ".std.txt"
    out_file_path = os.path.splitext(file_path)[0] + ".out.txt"

    with open(file_path, "rb") as f:
        skeleton_data = skeleton_binary.read_skeleton_data(f.read())

    out_content = summary(skeleton_data)

    with open(out_file_path, "w", encoding="utf-8") as f:
        f.write(out_content)

    if os.path.isfile(std_file_path):
        with open(std_file_path, "r", encoding="utf-8") as f:
            std_content = f.read()
        if out_content != std_content:
            raise AssertionError("Output does not match standard file")
        print("  Output matches standard file")
    else:
        print("  No standard file found")


def test_batch(folder_path: str):
    """Batch test all .skel files in folder."""
    print(f"🚀 Spine skeleton test, target folder: {folder_path}")

    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"Folder '{folder_path}' does not exist or is not a directory")

    skel_files = glob.glob(os.path.join(folder_path, "*.skel"))

    if not skel_files:
        raise FileNotFoundError(f"No .skel files found in '{folder_path}'")

    skeleton_binary = SkeletonBinary(scale=1.0)
    failed = False

    print("=" * 60)

    for i, skel_file in enumerate(skel_files, 1):
        print(f"[{i}/{len(skel_files)}] {os.path.relpath(skel_file, folder_path)}")
        try:
            test_single(skel_file, skeleton_binary)
        except AssertionError as e:
            print(f"  '{skel_file}': Assertion error. {e}")
            failed = True
            break
        except Exception as e:
            print(f"  '{skel_file}': Unexpected error.")
            print("\n" + traceback.format_exc() + "\n")
            failed = True
            break

    print("=" * 60)

    if failed:
        print("❌ Oops! Some files failed the test. Please check the messages above.")
        return False
    else:
        print(f"✅ Well done! {len(skel_files)} files tested.")
        return True
