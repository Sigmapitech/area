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
      sdkArgs = {
        includeNDK = false;
        includeSystemImages = false;
        includeEmulator = false;

        buildToolsVersions = [ "34.0.0" ];
        platformVersions = [ "34" "35" ];

        systemImageTypes = [ "google_apis" ];
        abiVersions = [ "arm64-v8a" "x86_64" ];

        extraLicenses = [
          "android-sdk-preview-license"
          "android-googletv-license"
          "android-sdk-arm-dbt-license"
          "google-gdk-license"
          "intel-android-extra-license"
          "intel-android-sysimage-license"
          "mips-android-sysimage-license"
        ];
      };

      androidComposition = pkgs.androidenv.composeAndroidPackages sdkArgs;
      androidSdk = androidComposition.androidsdk;
    in {
      default = pkgs.mkShell {
        inherit (self.checks.${pkgs.system}.pre-commit-check) shellHook;

        env.ANDROID_SDK_ROOT = "${androidSdk}/libexec/android-sdk";

        packages = with pkgs; [
          biome
          nodejs
          pnpm
          jdk
          gradle
        ] ++ (with androidComposition; [
          androidsdk
          platform-tools
          build-tools
        ]);
      };
    });
  };
}
