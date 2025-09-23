{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs = {
    nixpkgs, ...
  }: let
    applySystems = nixpkgs.lib.genAttrs ["x86_64-linux"];
    forAllSystems = f: applySystems (system: f nixpkgs.legacyPackages.${system});
  in {
    formatter = forAllSystems (pkgs: pkgs.alejandra);

    devShells = forAllSystems (pkgs: {
      default = pkgs.mkShell {
        packages = [
          pkgs.nodejs
          pkgs.pnpm
        ];
      };
    });
  };
}
