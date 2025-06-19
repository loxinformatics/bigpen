"""
Django management command for managing npm packages in a vendor directory.

Usage:
    python manage.py npm install
    python manage.py npm install --packages react vue
    python manage.py npm uninstall --packages lodash
    python manage.py npm uninstall --all
    python manage.py npm list
"""

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """Django management command for npm package management."""

    help = "Manage npm packages in a vendor directory"

    # Default packages to install
    DEFAULT_PACKAGES = [
        "bootstrap",
        "bootstrap-icons",
        "aos",
        "htmx.org@2.0.4",
        "glightbox",
        "isotope-layout",
        "imagesloaded",
        "waypoints",
    ]

    def add_arguments(self, parser):
        """Add command line arguments."""
        subparsers = parser.add_subparsers(
            dest="action", help="Available actions", required=True
        )

        # Install command
        install_parser = subparsers.add_parser("install", help="Install npm packages")
        install_parser.add_argument(
            "--packages",
            nargs="+",
            help="Specific packages to install (default: install default packages)",
        )
        install_parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be done without executing",
        )

        # Uninstall command
        uninstall_parser = subparsers.add_parser(
            "uninstall", help="Uninstall npm packages"
        )
        uninstall_parser.add_argument(
            "--packages", nargs="+", help="Specific packages to uninstall"
        )
        uninstall_parser.add_argument(
            "--all",
            action="store_true",
            help="Uninstall all packages (removes vendor directory)",
        )
        uninstall_parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be done without executing",
        )

        # List command
        subparsers.add_parser("list", help="List installed packages")

        # Global options
        parser.add_argument(
            "--vendor-dir",
            default="vendor",
            help="Vendor directory name (default: vendor)",
        )

    def handle(self, *args, **options):
        """Main command handler."""
        self.verbosity = options["verbosity"]
        self.dry_run = options.get("dry_run", False)

        # Set up paths
        current_file = Path(__file__)  # core/management/commands/npm.py
        core_dir = current_file.parent.parent.parent  # Navigate up to core/
        vendor_dir_name = options["vendor_dir"]
        self.vendor_path = core_dir / "static" / "core" / vendor_dir_name
        self.package_json_path = self.vendor_path / "package.json"

        # Find npm executable
        self.npm_cmd = self._find_npm()
        if not self.npm_cmd and not self.dry_run:
            raise CommandError(
                "npm not found. Please install Node.js and npm first, "
                "or ensure npm is in your system PATH."
            )

        # Execute the requested action
        action = options["action"]

        try:
            if action == "install":
                self.handle_install(options)
            elif action == "uninstall":
                self.handle_uninstall(options)
            elif action == "list":
                self.handle_list()
        except Exception as e:
            raise CommandError(f"Error executing {action}: {str(e)}")

    def _find_npm(self):
        """Find npm executable on the system."""
        # First try to find npm using shutil.which
        npm_path = shutil.which("npm")
        if npm_path:
            return npm_path

        # On Windows, also try npm.cmd
        if os.name == "nt":
            npm_cmd_path = shutil.which("npm.cmd")
            if npm_cmd_path:
                return npm_cmd_path

        # Common paths where npm might be installed
        common_paths = []

        if os.name == "nt":  # Windows
            # Check common Windows installation paths
            common_paths = [
                os.path.expanduser("~\\AppData\\Roaming\\npm\\npm.cmd"),
                "C:\\Program Files\\nodejs\\npm.cmd",
                "C:\\Program Files (x86)\\nodejs\\npm.cmd",
            ]
        else:  # Unix-like systems
            common_paths = [
                "/usr/local/bin/npm",
                "/usr/bin/npm",
                os.path.expanduser("~/.nvm/versions/node/*/bin/npm"),
            ]

        for path in common_paths:
            if os.path.exists(path):
                return path

        return None

    def handle_install(self, options):
        """Handle install command."""
        packages = options.get("packages") or self.DEFAULT_PACKAGES

        if self.verbosity >= 1:
            self.stdout.write(f"Installing packages: {', '.join(packages)}")

        self._ensure_vendor_dir()
        self._init_package_json()

        # Install packages
        install_cmd = ["install"] + packages
        success = self._run_npm_command(install_cmd)

        if success and not self.dry_run and self.verbosity >= 1:
            installed = self._get_installed_packages()
            self.stdout.write(
                self.style.SUCCESS(f"Successfully installed {len(installed)} packages:")
            )
            for pkg, version in installed.items():
                self.stdout.write(f"  - {pkg}@{version}")
        elif success and self.dry_run and self.verbosity >= 1:
            self.stdout.write(
                self.style.WARNING("[DRY RUN] Installation completed successfully")
            )

    def handle_uninstall(self, options):
        """Handle uninstall command."""
        if options.get("all"):
            self._uninstall_all()
        elif options.get("packages"):
            self._uninstall_packages(options["packages"])
        else:
            raise CommandError("Must specify either --all or --packages for uninstall")

    def handle_list(self):
        """Handle list command."""
        installed = self._get_installed_packages()

        if not installed:
            if self.verbosity >= 1:
                self.stdout.write("No packages currently installed.")
            return

        if self.verbosity >= 1:
            self.stdout.write(f"Installed packages in {self.vendor_path}:")
            for pkg, version in installed.items():
                self.stdout.write(f"  - {pkg}@{version}")
            self.stdout.write(self.style.SUCCESS(f"Total: {len(installed)} packages"))

    def _ensure_vendor_dir(self):
        """Ensure the vendor directory exists."""
        if not self.dry_run:
            self.vendor_path.mkdir(parents=True, exist_ok=True)
            if self.verbosity >= 2:
                self.stdout.write(f"Ensured vendor directory: {self.vendor_path}")
        else:
            if self.verbosity >= 1:
                self.stdout.write(
                    f"[DRY RUN] Would create directory: {self.vendor_path}"
                )

    def _init_package_json(self):
        """Initialize package.json if it doesn't exist."""
        if not self.package_json_path.exists():
            package_json_content = {
                "name": "vendor-packages",
                "version": "1.0.0",
                "description": "Vendor packages managed by Django npm command",
                "private": True,
                "dependencies": {},
            }

            if not self.dry_run:
                with open(self.package_json_path, "w") as f:
                    json.dump(package_json_content, f, indent=2)
                if self.verbosity >= 1:
                    self.stdout.write(
                        f"Created package.json at {self.package_json_path}"
                    )
            else:
                if self.verbosity >= 1:
                    self.stdout.write(
                        f"[DRY RUN] Would create package.json at {self.package_json_path}"
                    )

    def _run_npm_command(self, cmd: List[str]) -> bool:
        """Run an npm command in the vendor directory."""
        full_cmd = [self.npm_cmd] + cmd

        if self.dry_run:
            if self.verbosity >= 1:
                self.stdout.write(
                    f"[DRY RUN] Would run: {' '.join(full_cmd)} in {self.vendor_path}"
                )
            return True

        try:
            if self.verbosity >= 2:
                self.stdout.write(
                    f"Running: {' '.join(full_cmd)} in {self.vendor_path}"
                )
                self.stdout.write(f"Using npm at: {self.npm_cmd}")

            # On Windows, we need to use shell=True and pass the environment
            env = os.environ.copy()

            result = subprocess.run(
                full_cmd,
                cwd=self.vendor_path,
                capture_output=True,
                text=True,
                check=True,
                shell=os.name == "nt",  # Use shell on Windows
                env=env,
            )

            if result.stdout and self.verbosity >= 2:
                self.stdout.write(result.stdout)

            return True

        except subprocess.CalledProcessError as e:
            self.stderr.write(f"Error running npm command: {e}")
            if e.stderr:
                self.stderr.write(f"Error output: {e.stderr}")
            return False
        except FileNotFoundError:
            raise CommandError(
                f"npm executable not found at {self.npm_cmd}. "
                "Please install Node.js and npm first."
            )

    def _get_installed_packages(self) -> Dict[str, str]:
        """Get currently installed packages from package.json."""
        if not self.package_json_path.exists():
            return {}

        try:
            with open(self.package_json_path, "r") as f:
                package_data = json.load(f)
                return package_data.get("dependencies", {})
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _uninstall_packages(self, packages: List[str]):
        """Uninstall specific npm packages."""
        if not self.vendor_path.exists():
            raise CommandError(f"Vendor directory {self.vendor_path} does not exist.")

        if self.verbosity >= 1:
            self.stdout.write(f"Uninstalling packages: {', '.join(packages)}")

        uninstall_cmd = ["uninstall"] + packages
        success = self._run_npm_command(uninstall_cmd)

        if success and not self.dry_run and self.verbosity >= 1:
            self.stdout.write(
                self.style.SUCCESS(f"Successfully uninstalled: {', '.join(packages)}")
            )
        elif success and self.dry_run and self.verbosity >= 1:
            self.stdout.write(
                self.style.WARNING("[DRY RUN] Uninstall completed successfully")
            )

    def _uninstall_all(self):
        """Uninstall all packages by removing the vendor directory."""
        if not self.vendor_path.exists():
            if self.verbosity >= 1:
                self.stdout.write(
                    f"Vendor directory {self.vendor_path} does not exist."
                )
            return

        if self.dry_run:
            if self.verbosity >= 1:
                self.stdout.write(
                    f"[DRY RUN] Would remove entire vendor directory: {self.vendor_path}"
                )
            return

        try:
            import shutil

            shutil.rmtree(self.vendor_path)
            if self.verbosity >= 1:
                self.stdout.write(
                    self.style.SUCCESS(f"Removed vendor directory: {self.vendor_path}")
                )
        except Exception as e:
            raise CommandError(f"Error removing vendor directory: {e}")
