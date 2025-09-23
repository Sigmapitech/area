{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

    git-hooks = {
      url = "github:cachix/git-hooks.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = {
    self,
    nixpkgs,
    git-hooks,
  }: let
    applySystems = nixpkgs.lib.genAttrs ["x86_64-linux"];
    forAllSystems = f: applySystems (system: f nixpkgs.legacyPackages.${system});
  in {
    formatter = forAllSystems (pkgs: pkgs.alejandra);

    checks = forAllSystems (
      pkgs: {
        pre-commit-check = git-hooks.lib.${pkgs.system}.run {
          src = ./.;
          hooks = pkgs.lib.genAttrs [
            "black"
            "isort"
            "trim-trailing-whitespace"
            "deadnix"
          ] (_: {enable = true;});
        };
      }
    );

    devShells = forAllSystems (pkgs: {
      default = let
        py-env = pkgs.python3.withPackages (_:
          with self.packages.${pkgs.system}.back;
            dependencies ++ optional-dependencies.dev
        );
      in
        pkgs.mkShell {
          inherit (self.checks.${pkgs.system}.pre-commit-check) shellHook;

          packages = with pkgs; [
            py-env
            black
            isort
          ];
        };
    });

    packages = forAllSystems (pkgs: {
      back = pkgs.callPackage ./back { };
    });
  };
}
