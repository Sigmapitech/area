{
  stdenvNoCC,
  nodejs,
  pnpm,
  mode ? "web"
}:
stdenvNoCC.mkDerivation (finalAttrs: {
  pname = "area-front";
  version = "0.0.0";

  src = ./.;

  nativeBuildInputs = [
    nodejs
    pnpm.configHook
  ];

  pnpmDeps = pnpm.fetchDeps {
    inherit (finalAttrs) pname src;
    fetcherVersion = 2;
    hash = "sha256-FSyX00j8Is8P/IHvJ/xL8j3OGVMYevXuMRwYYUs6QiA=";
  };

  # using sass-embedded fails at executing dart-sass from node-modules
  preBuild = ''
    rm -rf node_modules/{.pnpm/,}sass-embedded*
  '';

  buildPhase = ''
    runHook preBuild

    pnpm run build:${mode}

    runHook postBuild
  '';

  installPhase = ''
    runHook preInstall

    cp -r dist/ $out

    runHook postInstall
  '';
})
