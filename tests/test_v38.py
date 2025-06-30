import os
import glob
import traceback
from spine_asset.v38.AtlasFile import AtlasFile
from spine_asset.v38.SkeletonBinary import SkeletonBinary
from spine_asset.v38.SkeletonData import SkeletonData
from spine_asset.v38.SkeletonJson import SkeletonJson


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


def test_single_skeleton(file_path: str):
    """Test a single skeleton file."""
    std_file_path = os.path.splitext(file_path)[0] + ".std.txt"
    out_file_path = os.path.splitext(file_path)[0] + ".out.txt"

    if file_path.endswith(".json"):
        with open(file_path, "r", encoding="utf-8") as f:
            skeleton = SkeletonJson().read_skeleton_data(f.read())
    else:
        with open(file_path, "rb") as f:
            skeleton = SkeletonBinary().read_skeleton_data(f.read())

    out_content = summary(skeleton)

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


def test_single_atlas(file_path: str):
    """Test a single atlas file."""
    out_file_path = os.path.splitext(file_path)[0] + ".out.atlas"

    with open(file_path, "r", encoding="utf-8") as f:
        atlas_content = f.read()
        atlas = AtlasFile.loads(atlas_content)

    out_content = atlas.dumps()

    with open(out_file_path, "w", encoding="utf-8") as f:
        f.write(out_content)

    if out_content == atlas_content:
        print("  Deserialization matches source file")
    else:
        raise AssertionError("Deserialization does not match source file")


def test_batch(folder_path: str):
    """Batch test all files in folder."""
    print(f"🚀 Spine parsing test, target folder: {folder_path}")

    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"Folder '{folder_path}' does not exist or is not a directory")

    skel_files = glob.glob(os.path.join(folder_path, "*.skel"))
    json_files = glob.glob(os.path.join(folder_path, "*.json"))
    atlas_files = glob.glob(os.path.join(folder_path, "*.atlas"))
    all_files = list(filter(lambda x: not ".out." in x, skel_files + json_files + atlas_files))

    if not skel_files:
        raise FileNotFoundError(f"No available file found in '{folder_path}'")

    failed = False

    print("=" * 60)

    for i, file_name in enumerate(all_files, 1):
        print(f"[{i}/{len(all_files)}] {os.path.relpath(file_name, folder_path)}")
        try:
            if file_name.endswith(".atlas"):
                test_single_atlas(file_name)
            else:
                test_single_skeleton(file_name)
        except AssertionError as e:
            print(f"  '{file_name}': Assertion error. {e}")
            failed = True
            break
        except Exception as e:
            print(f"  '{file_name}': Unexpected error.")
            print("\n" + traceback.format_exc() + "\n")
            failed = True
            break

    print("=" * 60)

    if failed:
        print("❌ Oops! Some files failed the test. Please check the messages above.")
        return False
    else:
        print(f"✅ Well done! {len(all_files)} files tested.")
        return True
