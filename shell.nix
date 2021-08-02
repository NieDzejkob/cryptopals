{ pkgs ? import <nixpkgs> {} }:

with pkgs; mkShell {
  nativeBuildInputs = [
    (python3.withPackages (py: [
      py.pycryptodome
      #py.ipython
    ]))
  ];

  shellHook = ''
    export PYTHONPATH="$(pwd)"
  '';
}
