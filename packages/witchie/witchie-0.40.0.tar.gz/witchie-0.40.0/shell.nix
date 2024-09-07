# SPDX-FileCopyrightText: 2023 Ngô Ngọc Đức Huy <huyngo@disroot.org>
#
# SPDX-License-Identifier: CC0-1.0

{pkgs ? import <nixpkgs> {}
}:
pkgs.mkShell {
  name="python-env";
  buildInputs = with pkgs; [
    python3
  ] ++ (with python3Packages; [
    requests
    # beautifulsoup4
    wcwidth
    urwid
    tomlkit
    # urwidgets
  ]);
  shellHook = ''
    echo "Entering python environment for witchie..."
  '';
}
