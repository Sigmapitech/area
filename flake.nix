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
    forAllSystems = f: applySystems (system:
      f (import nixpkgs {
        inherit system;
        config = {
          android_sdk.accept_license = true;
          allowUnfree = true;
        };
      })
    );
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

    devShells = forAllSystems (pkgs: let
      compo = self.packages.${pkgs.system}.android-composition;
    in {
      default = pkgs.mkShell {
        inherit (self.checks.${pkgs.system}.pre-commit-check) shellHook;

        env.ANDROID_SDK_ROOT = "${compo.androidsdk}/libexec/android-sdk";

        packages = with pkgs; [
          biome
          nodejs
          pnpm
          jdk
          gradle
        ] ++ (with compo; [
          androidsdk
          platform-tools
          build-tools
        ]);
      };

      with-emulator = let
        compo' = compo.override {
          includeEmulator = true;
          includeSystemImages = true;
        };
      in pkgs.mkShell {
        inputsFrom = [ self.devShells.${pkgs.system}.default ];

        env.ANDROID_SDK_ROOT = "${compo'.androidsdk}/libexec/android-sdk";

        packages = with compo'; [
          emulator
        ];
      };
    });

    packages = forAllSystems (pkgs: {
      android-composition = pkgs.callPackage ./front/android/composition.nix { };
    });
  };
}
