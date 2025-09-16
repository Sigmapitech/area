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
          hooks = import ./git-hooks.nix {inherit pkgs;};
          src = ./.;
        };
      }
    );

    devShells = forAllSystems (pkgs: {
      default = let
        py-env = pkgs.python3.withPackages (p:
          with p;
            [
              aiocache
              aiohttp
              aiosqlite
              bcrypt
              email-validator
              fastapi
              fastapi-cli
              httpx
              passlib
              pydantic
              pydantic-settings
              pyjwt
              python-dotenv
              python-multipart
              sqlmodel
              uvicorn
            ]
            ++ [
              black
              isort
              ruff
            ]);
      in
        pkgs.mkShell {
          inherit (self.checks.${pkgs.system}.pre-commit-check) shellHook;

          packages = let
            front-deps = with pkgs; [
              eslint
              nodejs
              typescript
              biome
              vite
            ];

            back-deps = [
              py-env
              pkgs.pyright
            ];
          in
            front-deps ++ back-deps;
        };
    });
  };
}
