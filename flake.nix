{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

    git-hooks = {
      url = "github:cachix/git-hooks.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = {
    self, nixpkgs, git-hooks
  }: let
    applySystems = nixpkgs.lib.genAttrs ["x86_64-linux"];
    forAllSystems = f: applySystems (system: f nixpkgs.legacyPackages.${system});
  in {
    formatter = forAllSystems (pkgs: pkgs.alejandra);

    checks = forAllSystems (
      pkgs: {
        pre-commit-check = git-hooks.lib.${pkgs.system}.run {
          src = ./.;
          hooks = {
            biome = {
              enable = true;
              name = "biome hook (format only)";
              entry = ''
                ${pkgs.lib.getExe pkgs.biome} format --write ./.
              '';
            };
          }
          // pkgs.lib.genAttrs [
            "convco"
            "trim-trailing-whitespace"
            "deadnix"
          ] (_: {enable = true;});
        };
      }
    );

    devShells = forAllSystems (pkgs: {
      default = pkgs.mkShell {
        inherit (self.checks.${pkgs.system}.pre-commit-check) shellHook;
        packages = with pkgs; [
          biome
          nodejs
          pnpm
        ];
      };
    });
  };
}
