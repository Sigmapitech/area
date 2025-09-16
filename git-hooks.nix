{pkgs}: let
  inherit (pkgs) lib;

  activate = pkgs.lib.foldr (x: prev: prev // {${x}.enable = true;}) {};
in
  {
    biome = {
      enable = true;
      files = "front/browser/.*\\.(ts|tsx|json)$";
      entry = ''
        ${lib.getExe pkgs.biome} format --write ./front
      '';
    };

    isort = {
      enable = true;
      settings.profile = "black";
    };
  }
  // activate [
    "black"
    "convco"
    "trim-trailing-whitespace"
    "alejandra"
    "deadnix"
  ]
