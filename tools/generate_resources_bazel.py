#!/usr/bin/env python3
"""Generate resources_rc.py for Bazel builds"""
import sys
import os
import tempfile
import shutil
from pathlib import Path

def main():
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <output_file> <qrc_file> <css_files...>", file=sys.stderr)
        sys.exit(1)
    
    output_file = Path(sys.argv[1]).absolute()  # Make output path absolute
    qrc_file = sys.argv[2]
    css_files = sys.argv[3:]
    
    print(f"Generating resources_rc.py to {output_file}", file=sys.stderr)
    print(f"QRC file: {qrc_file}", file=sys.stderr)
    print(f"CSS files: {len(css_files)}", file=sys.stderr)
    
    # Create temp directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create source/resources directory structure
        resources_dir = temp_path / "source" / "resources"
        resources_dir.mkdir(parents=True)
        styles_dir = resources_dir / "styles"
        styles_dir.mkdir()
        
        # Copy QRC file
        shutil.copy(qrc_file, resources_dir / "resources.qrc")
        
        # Generate global.qss from CSS files
        with open(styles_dir / "global.qss", "w") as out:
            for css_file in css_files:
                with open(css_file, "r") as f:
                    out.write(f.read())
                    out.write("\n")
        
        # Copy all resource files from runfiles
        # Look for resources in the runfiles directory
        runfiles_dir = os.environ.get("RUNFILES_DIR") or os.path.join(os.path.dirname(sys.argv[0]), "..", ".runfiles")
        if os.path.exists(runfiles_dir):
            source_resources = Path(runfiles_dir) / "_main" / "source" / "resources"
            if source_resources.exists():
                for item in ["api", "certificates", "fonts", "icons"]:
                    src = source_resources / item
                    if src.exists():
                        print(f"Copying {src} to {resources_dir / item}", file=sys.stderr)
                        shutil.copytree(src, resources_dir / item, dirs_exist_ok=True)
        
        # Run pyside6-rcc
        from PySide6.scripts import pyside_tool
        
        old_argv = sys.argv
        old_cwd = os.getcwd()
        
        try:
            os.chdir(temp_path)
            sys.argv = ["pyside6-rcc", "source/resources/resources.qrc", "-o", "resources_rc.py"]
            print(f"Running pyside6-rcc in {temp_path}", file=sys.stderr)
            
            try:
                result = pyside_tool.rcc()
                print(f"pyside6-rcc returned: {result}", file=sys.stderr)
            except SystemExit as e:
                print(f"pyside6-rcc exited with code: {e.code}", file=sys.stderr)
                if e.code != 0:
                    sys.exit(1)
            except Exception as e:
                print(f"ERROR running pyside6-rcc: {e}", file=sys.stderr)
                import traceback
                traceback.print_exc(file=sys.stderr)
                sys.exit(1)
            
            # Check if output was created
            output_path = temp_path / "resources_rc.py"
            if not output_path.exists():
                print(f"ERROR: resources_rc.py was not created in {temp_path}", file=sys.stderr)
                print(f"Contents of temp_path:", file=sys.stderr)
                for item in temp_path.rglob("*"):
                    print(f"  {item}", file=sys.stderr)
                sys.exit(1)
            
            # Copy output file
            print(f"Copying {output_path} to {output_file}", file=sys.stderr)
            shutil.copy(output_path, output_file)
            print(f"Successfully generated {output_file}", file=sys.stderr)
            
        finally:
            sys.argv = old_argv
            os.chdir(old_cwd)

if __name__ == "__main__":
    main()
