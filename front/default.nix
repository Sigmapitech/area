{
  lib,
  stdenvNoCC,
  nodejs,
  pnpm,
  serve,
  mode ? "web",
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
    hash = "sha256-igUdfQtmFH8arU+dpLRBziJZ75108yq0kN5Jqf/Nuew=";
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

    mkdir -p $out/share/area-front
    cp -r dist/* $out/share/area-front/

    mkdir -p $out/bin
    cat > $out/bin/web <<'EOF'
    #!${stdenvNoCC.shell}
    exec ${lib.getExe serve} "$out/share/area-front" -p 8081
    EOF
    chmod +x $out/bin/web

    runHook postInstall
  '';

  meta = {
    description = "Area front-end";
    maintainers = with lib.maintainers; [sigmanificient];
    license = lib.licenses.bsd3;
    mainProgram = "web";
  };
})
